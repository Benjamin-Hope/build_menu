Message(STATUS "Building Project:")

function(SET_IF_NOT_DEFINED var value)
  if(NOT DEFINED ${var})
    set(${var} ${value} PARENT_SCOPE)
  endif()
endfunction()

if (WIN32 OR MINGW)
  SET_IF_NOT_DEFINED(OS_WINDOWS 1)
  Message(STATUS "Building for Windows")
elseif (UNIX)
  SET_IF_NOT_DEFINED(OS_LINUX 1)
  Message(STATUS "Building for Linux")
  endif()

SET_IF_NOT_DEFINED(OS_LINUX 0)
SET_IF_NOT_DEFINED(OS_WINDOWS 0)

SET_IF_NOT_DEFINED(UNIT_TEST 0)

add_compile_definitions(OS_LINUX=${OS_LINUX})
add_compile_definitions(OS_WINDOWS=${OS_WINDOWS})

add_compile_definitions(UNIT_TEST=${UNIT_TEST})
