import time
import pytest

from doozer.gpu import sleep_cycles
from doozer.gpu import sleep
from doozer.gpu import estimate_frequency

# , sleep_with_gil, estimate_frequency

from common_gpu import verify_sleep, verify_sleep_event, verify_sleep_cycles, verify_sleep_cycles_event

import cupy as cp

CYCLES = 1900000000


@pytest.mark.parametrize("us", [500, 1000, 2000, 5000, 10000, 20000, 50000])
def test_estimate_frequency(us: int):
    cycles = estimate_frequency(sleep_cycles, target_time=us, use_event=False)
    status = verify_sleep_cycles(sleep_cycles, (cycles,), us)
    assert status


@pytest.mark.parametrize("us", [500, 1000, 2000, 5000, 10000, 20000, 50000])
def test_estimate_frequency_event(us: int):
    cycles = estimate_frequency(sleep_cycles, target_time=us, use_event=True)
    status = verify_sleep_cycles_event(sleep_cycles, (cycles,), us)
    assert status


@pytest.mark.parametrize("us", [500, 1000, 2000, 5000, 10000, 20000, 50000])
def test_gpu_sleep(us: int):
    status = verify_sleep(sleep, (us,), us)
    assert status


@pytest.mark.parametrize("us", [500, 1000, 2000, 5000, 10000, 20000, 50000])
def test_gpu_sleep_event(us: int):
    status = verify_sleep_event(sleep, (us,), us)
    assert status
