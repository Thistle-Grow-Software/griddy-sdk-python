"""Base HTTP client for all Griddy SDK modules.

This module provides the BaseClient class, which implements common HTTP
functionality including rate limiting, automatic retries, and error handling.

Example:
    >>> from griddy.core import BaseClient
    >>> client = BaseClient(
    ...     base_url="https://api.example.com",
    ...     timeout=30,
    ...     rate_limit_delay=1.0,
    ... )
    >>> response = client.get("/endpoint", params={"key": "value"})
    >>> client.close()
"""

import time
from typing import Any, Dict, List
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .exceptions import APIError, AuthenticationError, NotFoundError, RateLimitError
from .utils.retries import retry_on_rate_limit


class BaseClient:
    """Base HTTP client with common functionality for all data source clients.

    This class provides a foundation for building API clients with built-in
    support for rate limiting, automatic retries on transient failures, and
    consistent error handling.

    Attributes:
        base_url: The base URL for all API requests.
        timeout: Request timeout in seconds.
        rate_limit_delay: Minimum delay between requests in seconds.
        session: The underlying requests Session object.
        cookies_file: Path to a cookies file for authentication.

    Example:
        >>> client = BaseClient(
        ...     base_url="https://api.nfl.com",
        ...     timeout=30,
        ...     max_retries=3,
        ...     rate_limit_delay=1.0,
        ... )
        >>> try:
        ...     data = client.get("/games", params={"season": 2024})
        ... finally:
        ...     client.close()
    """

    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
        max_retries: int = 3,
        rate_limit_delay: float = 1.0,
        headers: Dict[str, str] | None = None,
        cookies_file: str | None = None,
    ) -> None:
        """Initialize the base client.

        Creates an HTTP session with automatic retry capabilities for transient
        errors (429, 500, 502, 503, 504 status codes).

        Args:
            base_url: Base URL for the API (e.g., "https://api.nfl.com").
                Trailing slashes are automatically removed.
            timeout: Request timeout in seconds. Defaults to 30.
            max_retries: Maximum number of retries for failed requests.
                Defaults to 3.
            rate_limit_delay: Minimum delay between requests in seconds
                to avoid rate limiting. Defaults to 1.0.
            headers: Additional headers to include in all requests.
                These are merged with default headers (Accept, Content-Type).
            cookies_file: Path to a Netscape-format cookies file for
                authentication.

        Example:
            >>> client = BaseClient(
            ...     base_url="https://api.example.com",
            ...     timeout=60,
            ...     max_retries=5,
            ...     rate_limit_delay=2.0,
            ...     headers={"Authorization": "Bearer token"},
            ... )
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.rate_limit_delay = rate_limit_delay
        self._last_request_time = 0.0
        self.cookies_file = cookies_file

        # Create session with retry strategy
        self.session = requests.Session()

        # Configure retry strategy
        retry_strategy = Retry(
            total=max_retries,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"],
            backoff_factor=1.0,
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Set default headers
        default_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        if headers:
            default_headers.update(headers)

        self.session.headers.update(default_headers)

    def _enforce_rate_limit(self) -> None:
        """Enforce rate limiting between requests.

        Ensures that requests are spaced at least `rate_limit_delay` seconds
        apart to avoid overwhelming the API server.
        """
        if self.rate_limit_delay > 0:
            time_since_last = time.time() - self._last_request_time
            if time_since_last < self.rate_limit_delay:
                time.sleep(self.rate_limit_delay - time_since_last)
        self._last_request_time = time.time()

    def _handle_response(
        self, response: requests.Response
    ) -> Dict[str, Any] | List[Any]:
        """Handle HTTP response and raise appropriate exceptions.

        Parses the response and raises specific exceptions based on the
        HTTP status code.

        Args:
            response: The HTTP response object from requests.

        Returns:
            Parsed JSON response data as a dictionary or list.

        Raises:
            NotFoundError: When the resource is not found (404).
            AuthenticationError: When authentication fails (401).
            RateLimitError: When rate limit is exceeded (429).
            APIError: For all other error status codes.
        """
        try:
            response_data = response.json() if response.content else {}
        except ValueError:
            response_data = {"message": response.text}

        if response.status_code == 200:
            return response_data
        elif response.status_code == 404:
            raise NotFoundError(
                f"Resource not found: {response.url}",
                status_code=response.status_code,
                response_data=response_data,
            )
        elif response.status_code == 401:
            raise AuthenticationError(
                "Authentication failed",
                status_code=response.status_code,
                response_data=response_data,
            )
        elif response.status_code == 429:
            retry_after = None
            if "Retry-After" in response.headers:
                try:
                    retry_after = int(response.headers["Retry-After"])
                except ValueError:
                    pass

            raise RateLimitError(
                "Rate limit exceeded",
                status_code=response.status_code,
                response_data=response_data,
                retry_after=retry_after,
            )
        else:
            error_message = response_data.get("message", f"HTTP {response.status_code}")
            raise APIError(
                error_message,
                status_code=response.status_code,
                response_data=response_data,
            )

    @retry_on_rate_limit(max_retries=3)
    def get(
        self,
        endpoint: str,
        params: Dict[str, Any] | None = None,
        headers: Dict[str, str] | None = None,
    ) -> Dict[str, Any] | List[Any]:
        """Make a GET request to the API.

        Automatically applies rate limiting and handles errors.

        Args:
            endpoint: API endpoint path (e.g., "/games" or "players/123").
                Leading slashes are handled automatically.
            params: Query parameters to include in the request.
            headers: Additional headers to include in this request only.

        Returns:
            Parsed JSON response data.

        Raises:
            NotFoundError: When the resource is not found (404).
            AuthenticationError: When authentication fails (401).
            RateLimitError: When rate limit is exceeded (429).
            APIError: For all other error status codes.

        Example:
            >>> data = client.get(
            ...     "/games",
            ...     params={"season": 2024, "week": 1},
            ... )
        """
        self._enforce_rate_limit()

        url = urljoin(self.base_url + "/", endpoint.lstrip("/"))

        response = self.session.get(
            url,
            params=params,
            headers=headers,
            timeout=self.timeout,
        )

        return self._handle_response(response)

    @retry_on_rate_limit(max_retries=3)
    def post(
        self,
        endpoint: str,
        data: Dict[str, Any] | None = None,
        json_data: Dict[str, Any] | None = None,
        headers: Dict[str, str] | None = None,
    ) -> Dict[str, Any]:
        """Make a POST request to the API.

        Automatically applies rate limiting and handles errors.

        Args:
            endpoint: API endpoint path.
            data: Form data to send in the request body.
            json_data: JSON data to send in the request body.
            headers: Additional headers to include in this request only.

        Returns:
            Parsed JSON response data.

        Raises:
            NotFoundError: When the resource is not found (404).
            AuthenticationError: When authentication fails (401).
            RateLimitError: When rate limit is exceeded (429).
            APIError: For all other error status codes.

        Example:
            >>> result = client.post(
            ...     "/auth/token",
            ...     json_data={"username": "user", "password": "pass"},
            ... )
        """
        self._enforce_rate_limit()

        url = urljoin(self.base_url + "/", endpoint.lstrip("/"))

        response = self.session.post(
            url,
            data=data,
            json=json_data,
            headers=headers,
            timeout=self.timeout,
        )

        return self._handle_response(response)

    def close(self) -> None:
        """Close the HTTP session and release resources.

        Should be called when the client is no longer needed to properly
        clean up connections.

        Example:
            >>> client = BaseClient(base_url="https://api.example.com")
            >>> try:
            ...     data = client.get("/endpoint")
            ... finally:
            ...     client.close()
        """
        self.session.close()
