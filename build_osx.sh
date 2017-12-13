#!/bin/bash

brew update
# Install thirdparty requirements
brew install autoconf automake libtool nasm

# Build thirdparty
./build_thirdparty.sh

# Install python dependencies
pip install --quiet -r requirements_dev.txt

# Build .whl
python generate.py
python setup.py bdist_wheel
