from ..core import cpu_sleep, cpu_sleep_with_gil

sleep = cpu_sleep
sleep_with_gil = cpu_sleep_with_gil

__all__ = ["sleep", "sleep_with_gil"]
