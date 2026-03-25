r"""Player transaction endpoints (trades, signings, releases, IR designations)."""

from typing import Mapping, Optional

from griddy.core._constants import COLLECTION_ERROR_CODES
from griddy.core.decorators import sdk_endpoints
from griddy.nfl import models, utils
from griddy.nfl.basesdk import EndpointConfig
from griddy.nfl.endpoints.pro import ProSDK
from griddy.nfl.types import UNSET, OptionalNullable


# TODO: A bunch of these endpoints seem to have disappeared since a few weeks ago?
@sdk_endpoints
class Transactions(ProSDK):
    r"""Player transaction endpoints (trades, signings, releases, IR designations)."""

    def _get_transactions_config(
        self,
        *,
        month: int,
        year: int,
        team_id: Optional[str] = None,
        limit: Optional[int] = 20,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Transactions

        Retrieves recent transactions including trades, signings, releases,
        practice squad moves, and injured reserve designations.

        Args:
            month: Month (number) to fetch transactions for.
            year: Year (all four digits as int) to fetch transactions for.
            team_id: Team UUID string.
            limit: Maximum number of results.
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            TransactionsResponse containing recent player transactions
            for the specified period.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/teams/transactions",
            operation_id="getTransactions",
            request=models.GetTransactionsRequest(
                month=month,
                year=year,
                team_id=team_id,
                limit=limit,
            ),
            response_type=models.TransactionsResponse,
            error_status_codes=COLLECTION_ERROR_CODES,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
            return_raw_json=False,
        )
