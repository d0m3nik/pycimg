set PYTHON=python

# Build zlib
call "C:\Program Files\Microsoft Visual Studio 14.0\VC\vcvarsall.bat"
pushd .\thirdparty\zlib-1.2.11\contrib\vstudio\vc14
msbuild zlibvc.sln /p:Configuration=Release
popd

# Generate .pyx files
%PYTHON% generate.py 

# Build extension
%PYTHON% setup.py build_ext --inplace
