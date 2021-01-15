#!/bin/bash
# Start the docker image using nplbam as the volume passed
# in interactive mode
# and expose port 8080 on the local machine to traffic.
mode=-d
# take an -i argument to change the flask runtime mode to interactive for testing.
for arg in "$@"
do
    if [ "$arg" == "-i" ] 
    then
       mode=-it 
    fi
done
sudo docker run $mode --rm --name nplbam \
    -v "$(pwd)/nplbam":/nplbam \
    --network=nplbam-net \
    web_cont
