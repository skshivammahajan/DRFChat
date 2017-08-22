#!/bin/bash

# Run flake8 and display pep8 errors
flake8 --config=./.flake8 --ignore=F401 experchat/models/__init__.py

# Run isort to print diff
#echo -e "\n---------------------------------------------------------\nISORT\n"
isort -df -q

grep --exclude-dir='env' --exclude-dir='.git' --exclude-dir="scripts" --exclude-dir="config" -rn "print"

grep --exclude-dir='env' --exclude-dir='.git' --exclude-dir="scripts" -rn "pdb"
