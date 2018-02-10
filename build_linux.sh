#!/bin/bash

# Build thirdparty
./build_thirdparty.sh

mkdir test-results
mkdir cover
for PY_VER in `ls -d /opt/python/cp* | grep -E "cp34|35|36.*"`; do 
  PYTHON="$PY_VER/bin/python"
  PIP="$PY_VER/bin/pip"
  COVERALLS="$PY_VER/bin/coveralls"

  echo "Building for python version `$PYTHON --version`"

  $PIP install --quiet -r requirements_dev.txt
  $PIP install auditwheel

  # Generate .pyx files
  $PYTHON generate.py 

  # Build package 
  $PYTHON setup.py bdist_wheel 

  # Run tests
  $PYTHON setup.py nosetests
  COVERALLS_REPO_TOKEN=VcjHJa4uHN87FO2LAn1Sg5yMH0zB4EXj0 $COVERALLS
  mkdir /tmp/$PYTHON_VER
  cp -r test-results /tmp/$PYTHON_VER
  cp -r cover /tmp/$PYTHON_VER

  echo "TRAVIS_TAG=${TRAVIS_TAG}"
  if [[ -n $TRAVIS_TAG ]]; then
    $PYTHON -m auditwheel repair dist/*.whl 
    $PYTHON -m twine upload wheelhouse/*.whl
    rm wheelhouse/*.whl
  fi

  rm dist/*.whl

done
