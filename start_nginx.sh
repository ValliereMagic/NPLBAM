#!/bin/bash
# Start the nginx reverse proxy and static content server
sudo docker run -d --rm -p 127.0.0.1:8080:80 --name nplbam_rp \
    -v "$(pwd)/nginx/nginx.conf":/etc/nginx/nginx.conf:ro \
    -v "$(pwd)/nginx/root":/usr/share/nginx/html:ro \
    --network=nplbam-net \
    nginx
