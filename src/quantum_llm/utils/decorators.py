"""Useful decorators for QuantumLLM."""

import time
import functools
from typing import Callable, Any
import logging


logger = logging.getLogger(__name__)


def timeit(func: Callable) -> Callable:
    """Decorator to measure function execution time.

    Example:
        @timeit
        def my_function():
            pass
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start_time
        logger.info(f"{func.__name__} took {elapsed:.4f} seconds")
        return result

    return wrapper


def retry(max_attempts: int = 3, delay: float = 1.0):
    """Decorator to retry a function on failure.

    Args:
        max_attempts: Maximum number of attempts
        delay: Delay between attempts in seconds

    Example:
        @retry(max_attempts=3, delay=0.5)
        def flaky_function():
            pass
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    logger.warning(
                        f"{func.__name__} failed (attempt {attempt + 1}/{max_attempts}). "
                        f"Retrying in {delay}s... Error: {e}"
                    )
                    time.sleep(delay)

        return wrapper

    return decorator


def log_execution(level: str = "INFO"):
    """Decorator to log function execution.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)

    Example:
        @log_execution(level="DEBUG")
        def my_function():
            pass
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            log_level = getattr(logging, level.upper())
            logger.log(log_level, f"Executing {func.__name__}...")
            result = func(*args, **kwargs)
            logger.log(log_level, f"{func.__name__} completed")
            return result

        return wrapper

    return decorator


def cache_result(func: Callable) -> Callable:
    """Decorator to cache function results.

    Example:
        @cache_result
        def expensive_computation(x):
            return x ** 2
    """
    cache = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return wrapper
