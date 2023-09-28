#include "sleep.h"
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cuda.h>
#include <cuda_runtime_api.h>
#include <stdio.h>
#include <sys/time.h>
#include <unistd.h>

#ifdef DOOZER_ENABLE_NVTX
#include <nvtx3/nvtx3.hpp>
#endif

using namespace std;
using namespace chrono;

#include <cstdint>

__device__ void gpu_sleep_impl(uint64_t sleep_cycles) {
  unsigned long start = clock64();
  unsigned long cycles_elapsed;
  do {
    cycles_elapsed = clock64() - start;
  } while (cycles_elapsed < sleep_cycles);
}

__global__ void gpu_sleep_kernel(clock_t clock_count) {
  gpu_sleep_impl(clock_count);
}

void gpu_busy_sleep(const int device, const uint64_t cycles,
                    intptr_t stream_ptr) {
#ifdef DOOZER_ENABLE_NVTX
  nvtx3::scoped_range r{"cpp::gpu_busy_sleep"};
#endif
  cudaSetDevice(device);
  cudaStream_t stream = reinterpret_cast<cudaStream_t>(stream_ptr);
  gpu_sleep_kernel<<<1, 1, 0, stream>>>(cycles);
}
