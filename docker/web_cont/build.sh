#!/bin/bash
# Build the docker image, call it web_cont, and remove all intermediary
# containers created from the build process
sudo docker build -t web_cont --rm .