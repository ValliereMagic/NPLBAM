#!/bin/bash
# Connect to the database container from the nplbam container
sudo docker exec -it nplbam bash -c "PGPASSWORD=\"$(cat postgres_password.enc)\" psql -h nplbam_db -U postgres"