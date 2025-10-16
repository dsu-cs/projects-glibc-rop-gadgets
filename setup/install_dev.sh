#!/usr/bin/env bash

#Warning run this script from the setup dir or it will not work

#create a virtual environment for python and load the libraries needed

if [ ! -d "../venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv ../venv
else
    echo "Virtual environment already exists, skipping creation."
fi

source ../venv/bin/activate

pip install -r requirements.txt

# add any other commandline tools or dependencies that need to be added here

# you should install zstd