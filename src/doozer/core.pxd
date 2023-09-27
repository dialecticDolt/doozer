#distutils: language = c++

from libc.stdint cimport intptr_t

cdef extern from "include/sleep.h" nogil:
    cdef int cpu_busy_sleep(unsigned long long milli) except +
    cdef void gpu_busy_sleep(int dev, unsigned long long t, intptr_t stream) except +
