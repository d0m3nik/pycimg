#!/bin/bash

# Submodules
git submodule update --init --recursive

# Build thirdparty
./build_thirdparty.sh

mkdir test-results
mkdir cover
for PY_VER in `ls -d /opt/python/cp* | grep -E "cp34|35|36.*"`; do 
  PYTHON="$PY_VER/bin/python"
  PIP="$PY_VER/bin/pip"
  COVERALLS="$PY_VER/bin/coveralls"

  echo "Building for python version `$PYTHON --version`"

  $PIP install -r requirements_dev.txt

  # Generate .pyx files
  $PYTHON generate.py 

  # Build package 
  $PYTHON setup.py bdist_wheel 
  cp -r dist /tmp

  # Run tests
  $PYTHON setup.py nosetests
  COVERALLS_REPO_TOKEN=VcjHJa4uHN87FO2LAn1Sg5yMH0zB4EXj0 $COVERALLS
  mkdir /tmp/$PYTHON_VERSION
  cp -r test-results /tmp/$PYTHON_VERSION
  cp -r cover /tmp/$PYTHON_VERSION

done
