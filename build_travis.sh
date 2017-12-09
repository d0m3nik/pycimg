#!/bin/bash

if [[ "$TRAVIS_OS_NAME" == "linux" ]]; then 
  docker run -v `pwd`:`pwd` -w `pwd` $DOCKER_IMAGE `pwd`/build_linux.sh; 
fi

if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then 
  ./build_osx.sh
fi
