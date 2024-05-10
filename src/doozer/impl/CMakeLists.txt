file(GLOB IMPL_HDR ${CMAKE_CURRENT_SOURCE_DIR}/include/*.hpp)

if(DOOZER_ENABLE_CUDA)
    message(STATUS "Enabling Doozer CUDA support.")
    enable_language(CUDA)
    find_package(CUDAToolkit REQUIRED)
    message(STATUS "CUDAToolkit_LIBRARY_DIR: " ${CUDAToolkit_LIBRARY_DIR})
    file(GLOB IMPL_SRC "${CMAKE_CURRENT_SOURCE_DIR}/cuda/*")
else()
    file(GLOB IMPL_SRC "${CMAKE_CURRENT_SOURCE_DIR}/none/*")
endif(DOOZER_ENABLE_CUDA)

add_library(doozerimpl SHARED ${IMPL_SRC})
set_target_properties(doozerimpl PROPERTIES PUBLIC_HEADER "${IMPL_HDR}")
set_target_properties(doozerimpl PROPERTIES POSITION_INDEPENDENT_CODE ON)

if(DOOZER_ENABLE_CUDA)
    target_compile_definitions(doozerimpl PUBLIC DOOZER_ENABLE_CUDA)

    set(GPU_ARCH $ENV{CUDA_ARCH})
    if(GPU_ARCH)
        set_target_properties(doozerimpl PROPERTIES CUDA_ARCHITECTURES ${GPU_ARCH})
    else()
        set_target_properties(doozerimpl PROPERTIES CUDA_ARCHITECTURES OFF)
    endif(GPU_ARCH)

    target_link_directories(doozerimpl PUBLIC ${CUDAToolkit_LIBRARY_ROOT})
    set_target_properties(doozerimpl PROPERTIES CUDA_SEPARABLE_COMPILATION ON)
    set_target_properties(doozerimpl PROPERTIES CUDA_RESOLVE_DEVICE_SYMBOLS ON)
    target_compile_options(doozerimpl PRIVATE $<$<COMPILE_LANGUAGE:CUDA>:--expt-extended-lambda -DPROD>)
    target_compile_options(doozerimpl PRIVATE $<$<COMPILE_LANGUAGE:CUDA>:--expt-relaxed-constexpr>)
    target_link_libraries(doozerimpl PUBLIC CUDA::cudart)
endif(DOOZER_ENABLE_CUDA)

if(DOOZER_ENABLE_NVTX)
    message(STATUS "Enabling Doozer NVTX support.")
    target_include_directories(doozerimpl PUBLIC ${NVTX_INCLUDE})
    target_compile_definitions(doozerimpl PUBLIC DOOZER_ENABLE_NVTX)
endif(DOOZER_ENABLE_NVTX)

target_include_directories(doozerimpl PUBLIC ${CUDAToolkit_LIBRARY_DIR})
target_include_directories(doozerimpl PUBLIC ${CUDAToolkit_LIBRARY_ROOT})
target_include_directories(doozerimpl PUBLIC ${CUDAToolkit_INCLUDE_DIRS})
target_include_directories(doozerimpl PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
target_include_directories(doozerimpl PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)

install(
        TARGETS doozerimpl
        EXPORT DoozerBackendTargets
	LIBRARY DESTINATION ${SKBUILD_DATA_DIR}/lib
)
