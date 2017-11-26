#!/bin/bash

# Build zlib
pushd ./thirdparty/zlib
mkdir build
pushd build
cmake -g "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_FLAGS=-fPIC ..
make
cp zconf.h ..
popd
popd

# Build libjpeg-turbo
pushd ./thirdparty/libjpeg-turbo
autoreconf -fiv
mkdir build
pushd build
sh ../configure CFLAGS="-fPIC"
make
cp jconfig.h ..
popd
popd

# Build libpng
pushd ./thirdparty/libpng
mkdir build
pushd build
cmake -g "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release -DPNG_BUILD_ZLIB=ON -DZLIB_LIBRARY=`pwd`/../../zlib/build/libz.a -DZLIB_INCLUDE_DIR=`pwd`/../../zlib -DPNG_SHARED=OFF -DCMAKE_C_FLAGS=-fPIC ..
make
cp pnglibconf.h ..
popd
popd

