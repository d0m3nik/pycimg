set PYTHON_EXE=%PYTHON%/python.exe

call "C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\vcvarsall.bat"

%PYTHON_EXE% -m pip install -r requirements_dev.txt

conan install .

:: Generate .pyx files
%PYTHON_EXE% generate.py 

:: Build extension
::%PYTHON_EXE% setup.py build_ext --inplace

:: Build wheel package
%PYTHON_EXE% setup.py bdist_wheel 

