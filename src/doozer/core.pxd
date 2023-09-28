#distutils: language = c++

from libc.stdint cimport intptr_t
from libc.stdint cimport uint64_t

cdef extern from "include/sleep.h" nogil:
    cdef int cpu_busy_sleep(uint64_t milli) except +
    cdef void gpu_busy_sleep(int dev, uint64_t t, intptr_t stream) except +
