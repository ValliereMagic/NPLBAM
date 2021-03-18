#!/bin/bash
sudo docker run --rm --name nplbam_certbot \
	-v "$(pwd)/nginx/tls":/etc/letsencrypt \
	-v "$(pwd)/nginx/tls":/var/lib/letsencrypt \
	-v "$(pwd)/nginx/root":/webroot \
	certbot/certbot certonly
