cmake_minimum_required(VERSION 3.15)

project(myproject LANGUAGES CXX)

find_package(fmt REQUIRED)

add_executable(myapp
    example/main.cpp
)

target_link_libraries(myapp PRIVATE fmt::fmt)

install(TARGETS myapp)