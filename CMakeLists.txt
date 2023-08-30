cmake_minimum_required(VERSION 3.14)

project(vcpkg-export)

find_package(Python3 COMPONENTS Interpreter)
if(NOT Python3_Interpreter_FOUND)
	message(FATAL_ERROR "Python not found !")
endif()

set(SRCS CMakeLists.txt vcpkg_export.py readme.md vcpkg.json)

# add custom target to pack the vcpkg ports
add_custom_target(vcpkg-export ALL SOURCES ${SRCS}
    COMMAND "${Python3_EXECUTABLE}" "vcpkg_export.py"
    --vcpkg-installed-dir "${CMAKE_CURRENT_BINARY_DIR}/vcpkg_installed"
    --vcpkg-root "${Z_VCPKG_ROOT_DIR}"

    WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
    VERBATIM
    COMMENT "Export vcpkg packages"
)