set PYTHON_EXE=%PYTHON%/python.exe

call "C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\vcvarsall.bat"

:: Build zlib
pushd .\thirdparty\zlib
md build
pushd build
cmake -g "Visual Studio 14 2015 Win64" -A x64 -DCMAKE_C_FLAGS="/MD" -DCMAKE_BUILD_TYPE=Release ..
msbuild zlib.sln /p:Configuration=Release /p:Platform="x64"
copy zconf.h ..
popd
popd

:: Build libjpeg-turbo
pushd .\thirdparty\libjpeg-turbo
md build
pushd build
cmake -g "Visual Studio 14 2015 Win64" -A x64 -DCMAKE_C_FLAGS="/MD" -DCMAKE_BUILD_TYPE=Release .. -DNASM="C:\Program Files\yasm\yasm-1.3.0-win64.exe"
msbuild libjpeg-turbo.sln /p:Configuration=Release /p:Platform="x64"
copy jconfig.h ..
popd
popd

:: Build libpng
pushd .\thirdparty\libpng
md build
pushd build
cmake -g "Visual Studio 14 2015 Win64" -A x64 -DCMAKE_C_FLAGS="/MD" -DCMAKE_BUILD_TYPE=Release -DZLIB_LIBRARY=..\..\zlib\build\Release\zlibstatic.lib -DZLIB_INCLUDE_DIR=..\..\zlib ..
msbuild libpng.sln /p:Configuration=Release /p:Platform="x64"
copy pnglibconf.h ..
popd
popd

:: Generate .pyx files
%PYTHON_EXE% generate.py 

:: Build extension
::%PYTHON_EXE% setup.py build_ext --inplace

:: Build wheel package
%PYTHON_EXE% setup.py bdist_wheel 

