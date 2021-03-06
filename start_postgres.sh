#!/bin/bash
# Start our postgresql database
sudo docker run -d --rm --name nplbam_db \
    --network=nplbam-net \
    -v "$(pwd)/postgres":/var/lib/postgresql/data \
    -e POSTGRES_PASSWORD="$(cat postgres_root_password.enc)" \
    nplbam_postgres
