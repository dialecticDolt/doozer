
import time
from typing import Callable
import cupy as cp
import numpy as np

from common import verify_time


def verify_sleep_cycles(sleep_func: Callable, args, microseconds: int, samples: int = 10) -> bool:
    assert (cp.cuda.runtime.getDevice() == 0)

    stream = cp.cuda.get_current_stream()
    sleep_func(0, *args, stream)
    stream.synchronize()

    times = []
    for l in range(samples):
        start_t = time.time()
        sleep_func(0, *args, stream)
        stream.synchronize()
        end_t = time.time()
        times.append(end_t - start_t)
    elapsed = np.mean(np.asarray(times))

    print(
        f"Time taken: {elapsed} seconds. Expected: {microseconds / 1e6} seconds.")
    return verify_time(elapsed, microseconds / 1e6)


def verify_sleep(sleep_func: Callable, args, microseconds: int, samples: int = 10) -> bool:
    assert (cp.cuda.runtime.getDevice() == 0)

    stream = cp.cuda.get_current_stream()
    sleep_func(*args, device=0, stream=stream, compute_on_miss=True)
    stream.synchronize()

    times = []
    for l in range(samples):
        start_t = time.time()
        sleep_func(*args, device=0, stream=stream, compute_on_miss=True)
        stream.synchronize()
        end_t = time.time()
        times.append(end_t - start_t)
    elapsed = np.mean(np.asarray(times))

    print(
        f"Time taken: {elapsed} seconds. Expected: {microseconds / 1e6} seconds.")
    return verify_time(elapsed, microseconds / 1e6)


def verify_sleep_cycles_event(sleep_func: Callable, args, microseconds: int, samples: int = 10) -> bool:
    assert (cp.cuda.runtime.getDevice() == 0)

    stream = cp.cuda.get_current_stream()
    sleep_func(0, *args, stream)
    stream.synchronize()

    times = []
    for l in range(samples):
        start_event = cp.cuda.Event()
        end_event = cp.cuda.Event()

        start_event.record(stream)
        sleep_func(0, *args, stream)
        end_event.record(stream)
        stream.synchronize()
        elapsed = cp.cuda.get_elapsed_time(
            start_event, end_event)/1000
        times.append(elapsed)

    elapsed = np.mean(np.asarray(times))
    print(
        f"Time taken: {elapsed} seconds. Expected: {microseconds / 1e6} seconds.")
    return verify_time(elapsed, microseconds / 1e6)


def verify_sleep_event(sleep_func: Callable, args, microseconds: int, samples: int = 10) -> bool:
    assert (cp.cuda.runtime.getDevice() == 0)

    stream = cp.cuda.get_current_stream()
    sleep_func(*args, device=0, stream=stream, compute_on_miss=True)
    stream.synchronize()

    times = []
    for l in range(samples):
        start_event = cp.cuda.Event()
        end_event = cp.cuda.Event()

        start_event.record(stream)
        sleep_func(*args, device=0, stream=stream, compute_on_miss=True)
        end_event.record(stream)
        stream.synchronize()
        elapsed = cp.cuda.get_elapsed_time(
            start_event, end_event)/1000
        times.append(elapsed)

    elapsed = np.mean(np.asarray(times))
    print(
        f"Time taken: {elapsed} seconds. Expected: {microseconds / 1e6} seconds.")
    return verify_time(elapsed, microseconds / 1e6)
