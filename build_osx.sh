#!/bin/bash

brew update
# Install thirdparty requirements
brew install autoconf automake libtool nasm

# Build thirdparty
./build_thirdparty.sh

# Install python3
brew install python3
# Install python dependencies
pip3 install --quiet -r requirements_dev.txt
# Build .whl
python3 generate.py
python3 setup.py bdist_wheel
