#!/bin/bash

echo "TRAVIS_OS_NAME=${TRAVIS_OS_NAME}"
echo "TRAVIS_TAG=${TRAVIS_TAG}"

if [[ "$TRAVIS_OS_NAME" == "linux" ]]; then 
  docker run -e TWINE_USERNAME -e TWINE_PASSWORD -e TRAVIS_TAG -v `pwd`:`pwd` -w `pwd` $DOCKER_IMAGE `pwd`/build_linux.sh; 
fi

if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then 
  ./build_osx.sh
fi
