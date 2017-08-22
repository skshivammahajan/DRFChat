#!/bin/bash

# Run flake8 and display pep8 errors
flake8 --config=./config/flake8 .

# Run isort to print diff
# echo -e "\n---------------------------------------------------------\nISORT\n"
isort  -df -q

grep --exclude-dir='env' --exclude-dir='.git' --exclude-dir="scripts" --exclude-dir="templates" --exclude-dir="config" -rn "print"

grep --exclude-dir='env' --exclude-dir='.git' --exclude-dir="scripts" -rn "pdb"
