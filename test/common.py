
import time
from typing import Callable


def verify_time(value, truth, percent=0.1):
    return abs(value - truth) < truth * percent or abs(value - truth) < 1e-4


def verify_sleep(sleep_func: Callable, args, microseconds: int) -> bool:
    start_t = time.time()
    sleep_func(*args)
    end_t = time.time()
    print(
        f"Time taken: {end_t - start_t} seconds. Expected: {microseconds / 1e6} seconds.")
    return abs(end_t - start_t - microseconds / 1e6) < 1e-4
