from ..core import gpu_sleep, gpu_sleep_with_gil
import cupy as cp

from .utility import load_cycle_map, save_cycle_map, _time_to_cycle_map
from .utility import _lookup_cycles_for_time, estimate_frequency

sleep_cycles = gpu_sleep
sleep_with_gil_cycles = gpu_sleep_with_gil


def lookup_cycles_for_time(us: int, compute_on_miss=True) -> int:

    cycles, found = _lookup_cycles_for_time(us)

    if found:
        return cycles

    if compute_on_miss:
        # Compute the cycle count for the given time
        cycles = estimate_frequency(
            sleep_cycles, initial=cycles, samples=10, target_time=us, use_event=True)
        _time_to_cycle_map[us] = cycles
        return cycles
    else:
        return cycles


def sleep(us: int, device: int = None, stream: cp.cuda.Stream | None = None, compute_on_miss=True):
    if stream is None:
        stream = cp.cuda.get_current_stream()

    if device is None:
        device = cp.cuda.runtime.getDevice()

    cycles = lookup_cycles_for_time(us, compute_on_miss=compute_on_miss)

    sleep_cycles(device, cycles, stream)


def sleep_with_gil(us: int, device: int = None, stream: cp.cuda.Stream | None = None, compute_on_miss=True):
    if stream is None:
        stream = cp.cuda.get_current_stream()

    if device is None:
        device = cp.cuda.runtime.getDevice()

    cycles = lookup_cycles_for_time(us, compute_on_miss=compute_on_miss)
    sleep_with_gil_cycles(device, cycles, stream)


__all__ = ["sleep_cycles", "sleep_with_gil_cycles", "sleep",
           "sleep_with_gil", "estimate_frequency", "load_cycle_map", "save_cycle_map"]
