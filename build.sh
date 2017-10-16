PYTHON=python3

# Build zlib
ZLIB_BUILD_DIR=./thirdparty/zlib-1.2.11/build
mkdir $ZLIB_BUILD_DIR 
WD=`pwd` 
cd $ZLIB_BUILD_DIR
cmake .. && make
cp zconf.h ..
cd $WD

# Generate .pyx files
$PYTHON generate.py 

# Build extension
$PYTHON setup.py build_ext --inplace
