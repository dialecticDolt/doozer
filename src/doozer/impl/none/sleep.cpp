#include "sleep.h"
#include <chrono>
#include <cstdint>
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

void gpu_busy_sleep(const int device, const uint64_t t, intptr_t stream_ptr) {
#ifdef DOOZER_ENABLE_NVTX
  nvtx3::scoped_range r{"cpp::gpu_busy_sleep"};
#endif

  printf(
      "Warning: Attempting to use GPU sleep on a non-GPU build of Doozer.\n");
}
