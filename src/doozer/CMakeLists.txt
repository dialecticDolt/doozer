if (PARLA_ENABLE_CUDA)
    find_package(CUDAToolkit REQUIRED)
endif()

set(PYX_FILES 
    core.pyx
)

set(FILE_MAP
    "core.pxd"
)

set(index 0)
foreach(PYX_FILE DEPEND_STRING IN ZIP_LISTS PYX_FILES FILE_MAP)
    get_filename_component(CY_NAME ${PYX_FILE} NAME_WE)

    if (PYX_FILE STREQUAL "")
        break()
    endif()

    if (DEPEND_STRING STREQUAL "")
        set(DEPEND_NAMES "")
    else()
        string(REPLACE " " ";" DEPEND_FILES ${DEPEND_STRING})
        set(DEPEND_NAMES "")
        foreach(DEPEND_FILE ${DEPEND_FILES})
            set(DEPEND_NAME "${CMAKE_CURRENT_SOURCE_DIR}/${DEPEND_FILE}")
            list(APPEND DEPEND_NAMES ${DEPEND_NAME})
        endforeach()
    endif()

    set(CPP_FILE "${CMAKE_CURRENT_BINARY_DIR}/${CY_NAME}.cpp")
    set(CY_FILE "${CMAKE_CURRENT_SOURCE_DIR}/${CY_NAME}.pyx")

    add_custom_command(
        OUTPUT ${CPP_FILE}
        DEPENDS ${CY_FILE} ${DEPEND_NAMES}
        VERBATIM
        COMMAND ${CYTHON} ${CY_FILE} ${CYTHON_FLAGS} --include-dir ${CMAKE_CURRENT_SOURCE_DIR} --include-dir ${PROJECT_SOURCE_DIR}/src/doozer/impl -o ${CPP_FILE}
        COMMENT "Cythonizing ${PYX_FILE}..."
    )

    python_add_library(${CY_NAME} MODULE "${CPP_FILE}" WITH_SOABI)
    target_link_libraries(${CY_NAME} PRIVATE doozerimpl)
    target_link_directories(${CY_NAME} PRIVATE ${CMAKE_CURRENT_BINARY_DIR})

    target_include_directories(${CY_NAME} PRIVATE ${PROJECT_SOURCE_DIR}/src/doozer)
    target_include_directories(${CY_NAME} PRIVATE ${PROJECT_SOURCE_DIR}/src/doozer/impl)
    target_include_directories(${CY_NAME} PRIVATE ${NumPy_INCLUDE_DIRS})
    target_include_directories(${CY_NAME} PRIVATE ${PYTHON_INCLUDE_DIRS})
    target_include_directories(${CY_NAME} PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
    target_include_directories(${CY_NAME} PRIVATE ${CMAKE_CURRENT_BINARY_DIR})
    if(DOOZER_ENABLE_CUDA)
        target_link_libraries(${CY_NAME} PRIVATE CUDA::cudart CUDA::cublas CUDA::nvToolsExt CUDA::cublasLt)
    endif(DOOZER_ENABLE_CUDA)
    install(TARGETS ${CY_NAME} DESTINATION ${CMAKE_PROJECT_NAME})
endforeach()
