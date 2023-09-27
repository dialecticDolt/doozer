import time
import pytest

from doozer.cpu import sleep, sleep_with_gil
from common import verify_sleep


@pytest.mark.parametrize("us", [500, 1000, 2000, 5000, 10000, 20000, 50000])
def test_cpu_sleep(us: int):
    status = verify_sleep(sleep, (us,), us)
    assert status


@pytest.mark.parametrize("us", [500, 1000, 2000, 5000, 10000, 20000, 50000])
def test_cpu_sleep_with_gil(us: int):
    status = verify_sleep(sleep_with_gil, (us,), us)
    assert status
