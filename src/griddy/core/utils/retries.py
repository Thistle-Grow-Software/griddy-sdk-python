import asyncio
import random
import time
from functools import wraps
from typing import Callable, List, TypeVar

import httpx

T = TypeVar("T")


def retry_on_rate_limit(max_retries: int = 3, backoff_factor: float = 1.0) -> Callable:
    """
    Decorator to retry function calls on rate limit errors.

    Args:
        max_retries: Maximum number of retry attempts
        backoff_factor: Factor for exponential backoff
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            from griddy.core.exceptions import RateLimitError

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except RateLimitError as e:
                    if attempt == max_retries:
                        raise

                    # Calculate backoff time
                    backoff_time = backoff_factor * (2**attempt)
                    if e.retry_after:
                        backoff_time = max(backoff_time, e.retry_after)

                    time.sleep(backoff_time)

            return func(*args, **kwargs)  # This should never be reached

        return wrapper

    return decorator


class BackoffStrategy:
    initial_interval: int
    max_interval: int
    exponent: float
    max_elapsed_time: int

    def __init__(
        self,
        initial_interval: int,
        max_interval: int,
        exponent: float,
        max_elapsed_time: int,
    ):
        self.initial_interval = initial_interval
        self.max_interval = max_interval
        self.exponent = exponent
        self.max_elapsed_time = max_elapsed_time


class RetryConfig:
    strategy: str
    backoff: BackoffStrategy
    retry_connection_errors: bool

    def __init__(
        self, strategy: str, backoff: BackoffStrategy, retry_connection_errors: bool
    ):
        self.strategy = strategy
        self.backoff = backoff
        self.retry_connection_errors = retry_connection_errors


class Retries:
    config: RetryConfig
    status_codes: List[str]

    def __init__(self, config: RetryConfig, status_codes: List[str]):
        self.config = config
        self.status_codes = status_codes


class TemporaryError(Exception):
    response: httpx.Response

    def __init__(self, response: httpx.Response):
        self.response = response


class PermanentError(Exception):
    inner: Exception

    def __init__(self, inner: Exception):
        self.inner = inner


def retry(func, retries: Retries):
    if retries.config.strategy == "backoff":

        def do_request() -> httpx.Response:
            res: httpx.Response
            try:
                res = func()

                for code in retries.status_codes:
                    if "X" in code.upper():
                        code_range = int(code[0])

                        status_major = res.status_code / 100

                        if code_range <= status_major < code_range + 1:
                            raise TemporaryError(res)
                    else:
                        parsed_code = int(code)

                        if res.status_code == parsed_code:
                            raise TemporaryError(res)
            except httpx.ConnectError as exception:
                if retries.config.retry_connection_errors:
                    raise

                raise PermanentError(exception) from exception
            except httpx.TimeoutException as exception:
                if retries.config.retry_connection_errors:
                    raise

                raise PermanentError(exception) from exception
            except TemporaryError:
                raise
            except Exception as exception:
                raise PermanentError(exception) from exception

            return res

        return retry_with_backoff(
            do_request,
            retries.config.backoff.initial_interval,
            retries.config.backoff.max_interval,
            retries.config.backoff.exponent,
            retries.config.backoff.max_elapsed_time,
        )

    return func()


async def retry_async(func, retries: Retries):
    if retries.config.strategy == "backoff":

        async def do_request() -> httpx.Response:
            res: httpx.Response
            try:
                res = await func()

                for code in retries.status_codes:
                    if "X" in code.upper():
                        code_range = int(code[0])

                        status_major = res.status_code / 100

                        if code_range <= status_major < code_range + 1:
                            raise TemporaryError(res)
                    else:
                        parsed_code = int(code)

                        if res.status_code == parsed_code:
                            raise TemporaryError(res)
            except httpx.ConnectError as exception:
                if retries.config.retry_connection_errors:
                    raise

                raise PermanentError(exception) from exception
            except httpx.TimeoutException as exception:
                if retries.config.retry_connection_errors:
                    raise

                raise PermanentError(exception) from exception
            except TemporaryError:
                raise
            except Exception as exception:
                raise PermanentError(exception) from exception

            return res

        return await retry_with_backoff_async(
            do_request,
            retries.config.backoff.initial_interval,
            retries.config.backoff.max_interval,
            retries.config.backoff.exponent,
            retries.config.backoff.max_elapsed_time,
        )

    return await func()


def retry_with_backoff(
    func,
    initial_interval=500,
    max_interval=60000,
    exponent=1.5,
    max_elapsed_time=3600000,
):
    start = round(time.time() * 1000)
    retries = 0

    while True:
        try:
            return func()
        except PermanentError as exception:
            raise exception.inner
        except Exception as exception:  # pylint: disable=broad-exception-caught
            now = round(time.time() * 1000)
            if now - start > max_elapsed_time:
                if isinstance(exception, TemporaryError):
                    return exception.response

                raise
            sleep = (initial_interval / 1000) * exponent**retries + random.uniform(0, 1)
            sleep = min(sleep, max_interval / 1000)
            time.sleep(sleep)
            retries += 1


async def retry_with_backoff_async(
    func,
    initial_interval=500,
    max_interval=60000,
    exponent=1.5,
    max_elapsed_time=3600000,
):
    start = round(time.time() * 1000)
    retries = 0

    while True:
        try:
            return await func()
        except PermanentError as exception:
            raise exception.inner
        except Exception as exception:  # pylint: disable=broad-exception-caught
            now = round(time.time() * 1000)
            if now - start > max_elapsed_time:
                if isinstance(exception, TemporaryError):
                    return exception.response

                raise
            sleep = (initial_interval / 1000) * exponent**retries + random.uniform(0, 1)
            sleep = min(sleep, max_interval / 1000)
            await asyncio.sleep(sleep)
            retries += 1
