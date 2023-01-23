#!/bin/bash

autopep8 --in-place --aggressive --aggressive ./*.py  ./accounts/*.py ./contactus/*.py ./auth_system/*.py
autoflake --in-place --remove-unused-variables ./*.py ./accounts/*.py ./contactus/*.py ./auth_system/*.py
black ./
isort ./