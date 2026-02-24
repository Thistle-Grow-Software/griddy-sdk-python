"""Cookie parsing and management utilities."""

from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse


class Cookie:
    """Represents a single HTTP cookie."""

    def __init__(
        self,
        domain: str,
        path: str,
        secure: bool,
        expires: int | None,
        name: str,
        value: str,
        http_only: bool = True,
        include_subdomains: bool = False,
    ):
        self.domain = domain
        self.path = path
        self.secure = secure
        self.expires = expires
        self.name = name
        self.value = value
        self.http_only = http_only
        self.include_subdomains = include_subdomains

    @property
    def is_expired(self) -> bool:
        """Check if the cookie is expired."""
        if self.expires is None:
            return False
        return datetime.now().timestamp() > self.expires

    def matches_domain(self, domain: str) -> bool:
        """Check if this cookie matches the given domain."""
        # Remove leading dot from cookie domain for comparison
        cookie_domain = self.domain.lstrip(".")
        target_domain = domain.lower()

        # Exact match
        if cookie_domain.lower() == target_domain:
            return True

        # Subdomain match (if cookie domain starts with .)
        if self.domain.startswith(".") or self.include_subdomains:
            return target_domain.endswith("." + cookie_domain.lower())

        return False

    def matches_path(self, path: str) -> bool:
        """Check if this cookie matches the given path."""
        if self.path == "/":
            return True
        return path.startswith(self.path)

    def to_dict(self) -> dict[str, str]:
        """Convert cookie to dictionary format."""
        return {self.name: self.value}

    def to_header_string(self) -> str:
        """Convert cookie to HTTP header format."""
        return f"{self.name}={self.value}"


def parse_cookies_txt(file_path: str | Path) -> list[Cookie]:
    """
    Parse a cookies.txt file and return a list of Cookie objects.

    Args:
        file_path: Path to the cookies.txt file

    Returns:
        List of Cookie objects

    Raises:
        FileNotFoundError: If the cookies file doesn't exist
        ValueError: If the file format is invalid
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Cookies file not found: {file_path}")

    cookies = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()

                # Skip empty lines and comments
                if not line or line.startswith("#"):
                    continue

                # Parse tab-separated values
                parts = line.split("\t")

                # Netscape cookie format should have 7 fields
                if len(parts) != 7:
                    continue

                try:
                    domain = parts[0]
                    include_subdomains = parts[1].upper() == "TRUE"
                    path = parts[2]
                    secure = parts[3].upper() == "TRUE"
                    expires_str = parts[4]
                    name = parts[5]
                    value = parts[6]

                    # Parse expiration time
                    expires = None
                    if expires_str and expires_str != "0":
                        try:
                            expires = int(expires_str)
                        except ValueError:
                            expires = None

                    cookie = Cookie(
                        domain=domain,
                        path=path,
                        secure=secure,
                        expires=expires,
                        name=name,
                        value=value,
                        include_subdomains=include_subdomains,
                    )

                    cookies.append(cookie)

                except (IndexError, ValueError) as e:
                    # Log the error but continue parsing
                    continue

    except UnicodeDecodeError:
        raise ValueError(f"Invalid file encoding in {file_path}")

    return cookies


def extract_cookies_for_url(
    cookies_file: str | Path, target_url: str, include_expired: bool = False
) -> list[Cookie]:
    """
    Extract cookies that match a specific URL from a cookies.txt file.

    Args:
        cookies_file: Path to the cookies.txt file
        target_url: URL to match cookies against
        include_expired: Whether to include expired cookies

    Returns:
        List of matching Cookie objects

    Raises:
        FileNotFoundError: If the cookies file doesn't exist
        ValueError: If the URL or file format is invalid
    """
    # Parse the target URL
    try:
        parsed_url = urlparse(target_url)
        domain = parsed_url.netloc.lower()
        path = parsed_url.path or "/"
        is_https = parsed_url.scheme.lower() == "https"
    except Exception:
        raise ValueError(f"Invalid URL: {target_url}")

    # Parse all cookies from file
    all_cookies = parse_cookies_txt(cookies_file)

    # Filter cookies that match the URL
    matching_cookies = []

    for cookie in all_cookies:
        # Skip expired cookies unless requested
        if not include_expired and cookie.is_expired:
            continue

        # Skip secure cookies on non-HTTPS URLs
        if cookie.secure and not is_https:
            continue

        # Check domain match
        if not cookie.matches_domain(domain):
            continue

        # Check path match
        if not cookie.matches_path(path):
            continue

        matching_cookies.append(cookie)

    return matching_cookies


def cookies_to_dict(cookies: list[Cookie]) -> dict[str, str]:
    """
    Convert a list of cookies to a dictionary format.

    Args:
        cookies: List of Cookie objects

    Returns:
        Dictionary with cookie names as keys and values as values
    """
    result = {}
    for cookie in cookies:
        result[cookie.name] = cookie.value
    return result


def cookies_to_header(cookies: list[Cookie]) -> str:
    """
    Convert a list of cookies to a Cookie header string.

    Args:
        cookies: List of Cookie objects

    Returns:
        Cookie header string (e.g., "name1=value1; name2=value2")
    """
    if not cookies:
        return ""

    return "; ".join(cookie.to_header_string() for cookie in cookies)


def extract_cookies_as_dict(
    cookies_file: str | Path, target_url: str, include_expired: bool = False
) -> dict[str, str]:
    """
    Extract cookies for a URL and return as a dictionary.

    Args:
        cookies_file: Path to the cookies.txt file
        target_url: URL to match cookies against
        include_expired: Whether to include expired cookies

    Returns:
        Dictionary with cookie names as keys and values as values
    """
    cookies = extract_cookies_for_url(cookies_file, target_url, include_expired)
    return cookies_to_dict(cookies)


def extract_cookies_as_header(
    cookies_file: str | Path, target_url: str, include_expired: bool = False
) -> str:
    """
    Extract cookies for a URL and return as a Cookie header string.

    Args:
        cookies_file: Path to the cookies.txt file
        target_url: URL to match cookies against
        include_expired: Whether to include expired cookies

    Returns:
        Cookie header string suitable for HTTP requests
    """
    cookies = extract_cookies_for_url(cookies_file, target_url, include_expired)
    return cookies_to_header(cookies)
