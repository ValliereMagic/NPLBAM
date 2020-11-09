#!/bin/bash
# Start the docker image using nplbam as the volume passed
# in interactive mode
# and expose port 8080 on the local machine to traffic.
sudo docker run -d --rm --name nplbam \
    -v "$(pwd)/nplbam":/nplbam \
    --network=nplbam-net \
    web_cont
