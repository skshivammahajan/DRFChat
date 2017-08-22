#! /bin/bash

find . -type f -name "*.pyc" | xargs rm -rf
find . -type d -name "__pycache__" | xargs rmdir
