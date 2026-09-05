cmake_minimum_required(VERSION 3.25)

set(TARGET_NAME Calculator)

set(headers
    "${CMAKE_CURRENT_SOURCE_DIR}/include/Calculator/example_calculator.h"
)

set(sources
    "${CMAKE_CURRENT_SOURCE_DIR}/src/example_calculator.cpp"
)

set(include_dirs
    "${CMAKE_CURRENT_SOURCE_DIR}/include"
)

if(UNIT_TEST)
    message(STATUS "Unit tests ENABLED")
endif()

add_library(${TARGET_NAME}_lib STATIC ${sources} ${headers})
target_include_directories(${TARGET_NAME}_lib PUBLIC ${include_dirs})
target_compile_features(${TARGET_NAME}_lib PRIVATE cxx_std_20)
