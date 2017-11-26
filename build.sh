#!/bin/bash

PYTHON=python3

# Submodules
git submodule update --init --recursive

# Build thirdparty
./build_thirdparty.sh

# Generate .pyx files
$PYTHON generate.py 

# Build extension 
$PYTHON setup.py build_ext --inplace
