#!/bin/bash

echo "$TRAVIS_OS_NAME"

if [[ "$TRAVIS_OS_NAME" == "linux" ]]; then 
  docker run -e TWINE_USERNAME -e TWINE_PASSWORD -v `pwd`:`pwd` -w `pwd` $DOCKER_IMAGE `pwd`/build_linux.sh; 
fi

if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then 
  ./build_osx.sh
fi
