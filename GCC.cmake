if(WIN32)
    set(GNU_HOME "$ENV{CONDA_PREFIX}/Library")
    set(TOOLCHAIN_EXE ".exe")
else()
    set(GNU_HOME "/usr")
    set(TOOLCHAIN_EXE "")
endif()

set(CMAKE_C_COMPILER
    "${GNU_HOME}/bin/gcc${TOOLCHAIN_EXE}"
)

set(CMAKE_CXX_COMPILER
    "${GNU_HOME}/bin/g++${TOOLCHAIN_EXE}"
)

set(CMAKE_AR
    "${GNU_HOME}/bin/x86_64-w64-mingw32-ar${TOOLCHAIN_EXE}"
)

set(CMAKE_RANLIB
    "${GNU_HOME}/bin/x86_64-w64-mingw32-ranlib${TOOLCHAIN_EXE}"
)