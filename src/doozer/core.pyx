from .core cimport cpu_busy_sleep, gpu_busy_sleep
from libc.stdint cimport intptr_t
import time 

from .utility import NVTXTracer
nvtx = NVTXTracer()
nvtx.initialize()


cpdef cpu_sleep(unsigned long long microseconds):
    cdef unsigned long long c_t = microseconds
    nvtx.push_range(message="py::cpu_busy_sleep", domain="Python", color="blue")
    with nogil:
        cpu_busy_sleep(c_t)
    nvtx.pop_range(domain="Python")

cpdef cpu_sleep_with_gil(unsigned long long microseconds):
    cdef unsigned long long c_t = microseconds
    nvtx.push_range(message="py::cpu_busy_sleep_gil", domain="Python", color="blue")
    cpu_busy_sleep(c_t)
    nvtx.pop_range(domain="Python")

def gpu_sleep(int dev, unsigned long long t, stream):
    cdef int c_dev = dev
    cdef unsigned long long c_t = t
    cdef intptr_t c_stream = stream.ptr
    nvtx.push_range(message="py::gpu_busy_sleep", domain="Python", color="blue")
    with nogil:
        gpu_busy_sleep(c_dev, c_t, c_stream)
    nvtx.pop_range(domain="Python")

def gpu_sleep_with_gil(int dev, unsigned long long t, stream):
    cdef int c_dev = dev
    cdef unsigned long long c_t = t
    cdef intptr_t c_stream = stream.ptr
    nvtx.push_range(message="py::gpu_busy_sleep_gil", domain="Python", color="blue")
    gpu_busy_sleep(c_dev, c_t, c_stream)
    nvtx.pop_range(domain="Python")
    
