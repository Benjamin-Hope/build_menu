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

    find_package(GTest CONFIG REQUIRED)

    add_executable(Calculator_tests
        test/test_example_calculator.cpp
    )

    target_link_libraries(Calculator_tests PRIVATE
        Calculator_lib
        GTest::gtest_main
    )

    target_compile_features(Calculator_tests PRIVATE cxx_std_20)

    if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
        target_compile_options(Calculator_tests PRIVATE --coverage)
        target_link_options(Calculator_tests PRIVATE --coverage)
    endif()    

    add_test(NAME Calculator_tests COMMAND Calculator_tests)
endif()

add_library(${TARGET_NAME}_lib STATIC ${sources} ${headers})
target_include_directories(${TARGET_NAME}_lib PUBLIC ${include_dirs})
target_compile_features(${TARGET_NAME}_lib PRIVATE cxx_std_20)
