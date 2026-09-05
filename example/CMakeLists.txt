cmake_minimum_required(VERSION 3.25)
add_subdirectory(Calculator)

find_package(fmt REQUIRED)

add_executable(${PROJECT_NAME})

set(source_files
    "${CMAKE_CURRENT_SOURCE_DIR}/main.cpp"
)

set(libs
  fmt::fmt
  Calculator_lib
)

target_sources(${PROJECT_NAME} PRIVATE ${source_files})
target_link_libraries(${PROJECT_NAME} PRIVATE ${libs})

target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_20)
