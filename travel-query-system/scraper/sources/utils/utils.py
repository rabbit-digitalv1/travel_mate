import logging
import random
import time
import traceback
from typing import Callable


def retry_with_backoff(
    retries: int = 3,
    backoff_factor: float = 0.5,
    allowed_exceptions: tuple = (Exception,),
):
    """
    Decorator to retry a function with exponential backoff in case of failure.
    """
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except allowed_exceptions as e:
                    wait = backoff_factor * (2 ** attempt)
                    logging.warning(
                        f"[Retry Attempt {attempt + 1}/{retries}] {e}. Retrying in {wait:.2f} seconds."
                    )
                    time.sleep(wait)
            logging.error("Maximum retry attempts reached. Traceback:")
            traceback.print_exc()
            return None

        return wrapper

    return decorator
