#!/bin/bash
# Start the nginx reverse proxy and static content server
sudo docker run -d --rm -p 0.0.0.0:80:80 -p 0.0.0.0:443:443 --name nplbam_rp \
    -v "$(pwd)/nginx/nginx.conf":/etc/nginx/nginx.conf:ro \
    -v "$(pwd)/nginx/root":/usr/share/nginx/html:ro \
    -v "$(pwd)/nginx/tls":/etc/nginx/tls:ro \
    --network=nplbam-net \
    nginx
