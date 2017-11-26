#!/bin/bash

# Submodules
git submodule update --init --recursive

# Build thirdparty
./build_thirdparty.sh

#PYTHON_VERSIONS="cp27-cp27m cp27-cp27mu cp33-cp33m cp34-cp34m cp35-cp35m cp36-cp36m" 
mkdir /tmp/test-reports
mkdir /tmp/cover
PYTHON_VERSIONS="cp35-cp35m" 
for PYTHON_VERSION in PYTHON_VERSIONS do
  PYTHON="/opt/local/$PYTHON_VERSION/bin/python"
  PIP="/opt/local/$PYTHON_VERSION/bin/pip"

  echo "Building for python version `$PYTHON --version`"

  $PIP install -r requirements_dev.txt

  # Generate .pyx files
  $PYTHON generate.py 

  # Build package 
  $PYTHON setup.py bdist_wheel 
  cp -r dist /tmp

  # Run tests
  $PYTHON setup.py nosetests
  mkdir /tmp/test-reports/$PYTHON_VERSION
  mkdir /tmp/cover/$PYTHON_VERSION
  cp -r test-reports /tmp/test-reports/$PYTHON_VERSION
  cp -r cover /tmp/cover/$PYTHON_VERSION

done
