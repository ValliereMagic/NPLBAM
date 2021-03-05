#!/bin/bash
# Create a local virtual python environment to do development work within
# Install required libraries within the virtual environment.
# This requires python3-pip and python3-venv on debian.
python3 -m venv nplbamNV
source nplbamNV/bin/activate
pip install flask pynacl SQLAlchemy plotnine psycopg2-binary
