cmake_minimum_required(VERSION 3.25)

project(
    BuildExample
    VERSION 1.0.0
    LANGUAGES CXX
)

set(PROJECT_TARGET ${PROJECT_NAME})

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
# Useful for clangd and other tools
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

include(configurations.cmake)

if (WIN32 OR MINGW)
  message(STATUS "NOTE: Activating windows large path support")
  # set(CMAKE_SOURCE_DIR "\\?\\${CMAKE_SOURCE_DIR}")
endif()

add_subdirectory(./example)

message(STATUS "Show configuration settings:")

# Print build type
if(CMAKE_BUILD_TYPE)
  message(STATUS "  Build type: ${CMAKE_BUILD_TYPE}")
else()
  message(STATUS "  Build type: Not defined")
endif()

function(get_compile_definitions)
  get_directory_property(compile_definitions COMPILE_DEFINITIONS)
  foreach(compile_definition ${compile_definitions})
    message(STATUS "  ${compile_definition}")
  endforeach()
endfunction()

get_compile_definitions()
