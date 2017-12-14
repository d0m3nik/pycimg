#!/bin/bash

brew update
# Install thirdparty requirements
brew install autoconf automake libtool nasm

# Build thirdparty
./build_thirdparty.sh

# Install pyenv
brew upgrade pyenv
eval "$(pyenv init -)"

pyenv install --list
case "${PYTHON_VERSION}" in
  # py27)
  #   curl -O https://bootstrap.pypa.io/get-pip.py
  #   python get-pip.py --user
  #   ;;
  # py33)
  #   pyenv install 3.3.6
  #   pyenv global 3.3.6
  #   ;;
  py34)
    pyenv install 3.4.6
    pyenv global 3.4.6
    ;;
  py35)
    pyenv install 3.5.4
    pyenv global 3.5.4
    ;;
  py36)
    pyenv install 3.6.1
    pyenv global 3.6.1
    ;;
esac
pyenv rehash
echo $(python --version)

# Install python dependencies
pip install --quiet -r requirements_dev.txt

# Build .whl
python generate.py
python setup.py bdist_wheel
