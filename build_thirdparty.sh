#!/bin/bash

CMAKE_C_FLAGS="-fPIC"
CMAKE_MODULE_LINKER_FLAGS=""
if [[ $OSTYPE == Darwin* ]]; then
  CMAKE_C_FLAGS+=" -mmacosx-version-min=10.7"
  CMAKE_MODULE_LINKER_FLAGS+=" -macosx-version-min=10.7"
fi

# Build zlib
pushd ./thirdparty/zlib
mkdir build
pushd build
cmake -g "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_FLAGS=$CMAKE_C_FLAGS -DCMAKE_MODULE_LINKER_FLAGS=$CMAKE_MODULE_LINKER_FLAGS .. 
make
cp zconf.h ..
popd
popd

# Build libjpeg-turbo
pushd ./thirdparty/libjpeg-turbo
autoreconf -fiv
mkdir build
pushd build
if [[ $OSTYPE == Darwin* ]]
then
  sh ../configure --host x86_64-apple-darwin\
    CFLAGS="-mmacosx-version-min=10.7 -O3 -fPIC"\
    LDFLAGS="-mmacosx-version-min=10.7"\ 
    NASM=/usr/local/bin/nasm
else
  sh ../configure CFLAGS="-fPIC"
fi
make
cp jconfig.h ..
popd
popd

# Build libpng
pushd ./thirdparty/libpng
mkdir build
pushd build
cmake -g "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release -DPNG_BUILD_ZLIB=ON -DZLIB_LIBRARY=`pwd`/../../zlib/build/libz.a -DZLIB_INCLUDE_DIR=`pwd`/../../zlib -DPNG_SHARED=OFF -DCMAKE_C_FLAGS=$CMAKE_C_FLAGS -DCMAKE_MODULE_LINKER_FLAGS=$CMAKE_MODULE_LINKER_FLAGS ..
make
cp pnglibconf.h ..
popd
popd

# Build libtiff
pushd ./thirdparty/libtiff
pushd build
cmake -g "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=OFF -DZLIB_LIBRARY=`pwd`/../../zlib/build/libz.a -DZLIB_INCLUDE_DIR=`pwd`/../../zlib -DCMAKE_C_FLAGS=$CMAKE_C_FLAGS -DCMAKE_MODULE_LINKER_FLAGS=$CMAKE_MODULE_LINKER_FLAGS ..
make
cp libtiff/tiffconf.h ../libtiff
popd
popd

