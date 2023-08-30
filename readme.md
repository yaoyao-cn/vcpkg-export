# vcpkg-export
- export built packages from the installed directory to a standalone directory in manifest mode which are not supported by vcpkg
- the directory hierarchy is same as directory exported by 'vcpkg export --raw' command
- see [vcpkg export](https://learn.microsoft.com/en-us/vcpkg/commands/export#description)

# usage
1. edit vcpkg.json to add your packages
1. generate build files
    ```cmake
    cmake -B build -S . -DCMAKE_TOOLCHAIN_FILE=<vcpkg root dir>/scripts/buildsystems/vcpkg.cmake
    ```
1. export packages
    ```cmake
    cmake --build build
    ```

# useful links
- [vcpkg](https://github.com/microsoft/vcpkg)
- [vcpkg manifest mode](https://learn.microsoft.com/en-us/vcpkg/users/manifests)
- [vcpkg versioning](https://learn.microsoft.com/en-us/vcpkg/users/versioning)

