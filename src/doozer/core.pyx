from .core cimport cpu_busy_sleep, gpu_busy_sleep
from libc.stdint cimport intptr_t
import time 

from .utility import NVTXTracer
nvtx = NVTXTracer()
nvtx.initialize()

from libc.stdint cimport uint64_t

cpdef cpu_sleep(uint64_t microseconds):
    cdef uint64_t c_t = microseconds
    nvtx.push_range(message="py::cpu_busy_sleep", domain="Python", color="blue")
    with nogil:
        cpu_busy_sleep(c_t)
    nvtx.pop_range(domain="Python")

cpdef cpu_sleep_with_gil(uint64_t microseconds):
    cdef uint64_t c_t = microseconds
    nvtx.push_range(message="py::cpu_busy_sleep_gil", domain="Python", color="blue")
    cpu_busy_sleep(c_t)
    nvtx.pop_range(domain="Python")

def gpu_sleep(int dev, uint64_t t, stream):
    cdef int c_dev = dev
    cdef uint64_t c_t = t
    cdef intptr_t c_stream = stream.ptr
    nvtx.push_range(message="py::gpu_busy_sleep", domain="Python", color="blue")
    with nogil:
        gpu_busy_sleep(c_dev, c_t, c_stream)
    nvtx.pop_range(domain="Python")

def gpu_sleep_with_gil(int dev, uint64_t t, stream):
    cdef int c_dev = dev
    cdef uint64_t c_t = t
    cdef intptr_t c_stream = stream.ptr
    nvtx.push_range(message="py::gpu_busy_sleep_gil", domain="Python", color="blue")
    gpu_busy_sleep(c_dev, c_t, c_stream)
    nvtx.pop_range(domain="Python")
    
