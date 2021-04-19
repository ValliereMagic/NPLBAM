# Here Lies the No Paw Left Behind Animal Manager Repository

This is an application for managing workflow and inputting animals. 

The underlying technologies are:

- Docker is being used to create a product that will work from any machine.
     - With three docker containers: Postgres container,  Flask container, and NGINX
- NGINX is being used as a reverse proxy and to serve static content and handle TLS in prod. 
- Gunicorn is being used as a Python WSGI HTTP Server for NGINX
- SQLAlchemy and Flask are being used to access the database and dynamically create and route our web pages.
- Postgres is being used as our database. Argon2 password hashing with libsodium.
- Certbot will be used to manage and request TLS certificates from the LetsEncrypt certificate authority.
- Jinja2 Templating of HTML/CSS
- Data Visualization using MatPlotlib.


