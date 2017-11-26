#!/bin/bash

# Submodules
git submodule update --init --recursive

# Build thirdparty
./build_thirdparty.sh

for PY_VER in `ls /opt/python/cp* | grep -E "cp2|3.*"`; do 
  PYTHON="/opt/local/$PY_VER/bin/python"
  PIP="/opt/local/$PY_VER/bin/pip"

  echo "Building for python version `$PYTHON --version`"

  $PIP install -r requirements_dev.txt

  # Generate .pyx files
  $PYTHON generate.py 

  # Build package 
  $PYTHON setup.py bdist_wheel 
  cp -r dist /tmp

  # Run tests
  mkdir test-results
  mkdir cover
  $PYTHON setup.py nosetests
  COVERALLS_REPO_TOKEN=VcjHJa4uHN87FO2LAn1Sg5yMH0zB4EXj0 coveralls
  mkdir /tmp/$PYTHON_VERSION
  cp -r test-results /tmp/$PYTHON_VERSION
  cp -r cover /tmp/$PYTHON_VERSION

done
