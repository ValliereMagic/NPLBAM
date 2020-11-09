FROM debian:buster-slim

# Install required system programs and libraries using the package manager
RUN apt-get update && apt-get install python3 python3-pip libsodium-dev -y
# Install the required python libraries using pip
RUN SODIUM_INSTALL=system pip3 install fastapi uvicorn jinja2 pynacl bleach psycopg2-binary
# Run the internal webserver uvicorn on port 8080 exposed to the rest of the machine
EXPOSE 8080
# App volume entry point
VOLUME /nplbam
# Command executed upon container execution, which starts the webserver listeining on port 8080
CMD ["uvicorn", "nplbam.app.main:nplbam", "--host", "0.0.0.0", "--port", "8080", "--workers", "2"]
