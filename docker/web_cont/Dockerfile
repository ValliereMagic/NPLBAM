FROM debian:buster-slim
# Add tools required to pull the postgres database packages
RUN apt-get update && apt-get install lsb-release wget gnupg2 -y
# Add the postgresql repository
# Create the file repository configuration:
RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
# Import the repository signing key:
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
# Install required system programs and libraries using the package manager
RUN apt-get update && apt-get install python3 python3-pip libsodium-dev postgresql-client-13 -y
# Install the required python libraries using pip
RUN SODIUM_INSTALL=system pip3 install flask gunicorn pynacl bleach SQLAlchemy psycopg2-binary
# Run the internal webserver gunicorn on port 8080 exposed to the rest of the machine
EXPOSE 8080
# App volume entry point
VOLUME /nplbam
# Command executed upon container execution, which starts the webserver listeining on port 8080
CMD ["gunicorn", "nplbam.app:create_app()", "-b", "0.0.0.0:8080", "-w", "2", "--threads", "2"]
