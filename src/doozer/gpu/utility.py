import cupy as cp
import numpy as np
from typing import Dict, Callable, Any, Optional, List, Tuple
import time
import bisect
from collections import OrderedDict

_time_to_cycle_map: OrderedDict = OrderedDict()


def clear_cycle_map():
    global _time_to_cycle_map
    _time_to_cycle_map = OrderedDict()


def get_cycle_map() -> OrderedDict:
    global _time_to_cycle_map
    return _time_to_cycle_map


def save_cycle_map(filename: str):
    global _time_to_cycle_map
    with open(filename, "w") as f:
        for k, v in _time_to_cycle_map.items():
            f.write(f"{k},{v}\n")


def load_cycle_map(filename: str):
    global _time_to_cycle_map
    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line == "":
                continue
            tokens = line.split(",")
            assert len(tokens) == 2
            _time_to_cycle_map[int(tokens[0])] = int(tokens[1])


def _lookup_cycles_for_time(us: int) -> Tuple[int, bool]:
    """
    Find the closest cycle count for a given time.
    """

    # If the time is in the map, return the cycle count
    if us in _time_to_cycle_map:
        return _time_to_cycle_map[us], True

    # If the time is not in the map, find the cycle count for the closest time
    if len(_time_to_cycle_map) > 0:

        seen_times = list(_time_to_cycle_map.keys())
        res = bisect.bisect_left(seen_times, us)

        if res == len(seen_times):
            res = res - 1

        found_time = seen_times[res]
        found_cycles = _time_to_cycle_map[found_time]

        estimate = found_cycles * (us / found_time)
        return estimate, False
    else:
        return 1900000000*(us/1e6), False


def _get_time_for_cycles(sleep_func: Callable, cycles: int, samples=10) -> Tuple[float, float]:
    observed_times = []
    for k in range(samples):
        stream = cp.cuda.get_current_stream()
        start = time.perf_counter()
        sleep_func(0, cycles, stream)
        stream.synchronize()
        end = time.perf_counter()
        elapsed = end - start
        observed_times.append(elapsed)

    times = np.asarray(observed_times)
    return np.mean(times), np.std(times)


def _get_time_for_cycles_event(sleep_func: Callable, cycles: int, samples=10) -> Tuple[float, float]:
    observed_times = []
    for k in range(samples):
        stream = cp.cuda.get_current_stream()
        start_event = cp.cuda.Event()
        end_event = cp.cuda.Event()

        start_event.record(stream)
        sleep_func(0, cycles, stream)
        end_event.record(stream)
        stream.synchronize()
        event_elapsed = cp.cuda.get_elapsed_time(
            start_event, end_event)/1000
        observed_times.append(event_elapsed)

    times = np.asarray(observed_times)
    return np.mean(times), np.std(times)


def estimate_frequency(sleep_func: Callable, samples=30, initial: int = 100000000, target_time=10000, verbose=False, use_event=True, tol=10) -> int:

    target_time = target_time / (1000 * 1000)
    tol = tol / (1000 * 1000)

    ticks = initial * target_time

    if verbose:
        print("Starting GPU Frequency benchmark.")
        print("Target Time: ", target_time, flush=True)

    times = []

    for k in range(samples):

        if use_event:
            mean_time, std_time = _get_time_for_cycles_event(
                sleep_func, ticks, samples=k+10)
        else:
            mean_time, std_time = _get_time_for_cycles(
                sleep_func, ticks, samples=k+10)

        times.append(mean_time)

        # Update Estimate
        ticks = (ticks) * (target_time/times[-1])

        if verbose:
            print(f"Observed Time: {mean_time}, STD: {std_time}", flush=True)
            print(f"Estimated Frequency: {ticks / times[-1]} Hz", flush=True)

        if k > 0:
            diff = np.abs(mean_time - target_time)
            if diff < tol:
                break

    final_estimate = ticks
    return int(final_estimate)
