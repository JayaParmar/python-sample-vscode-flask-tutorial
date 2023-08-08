# gunicorn_config.py

# Number of worker processes. Adjust this based on your server's resources.
workers = 3

# Number of threads per worker. Adjust this based on your server's resources and app's behavior.
threads = 2

# Host and port on which Gunicorn will listen.
bind = '0.0.0.0:5555'

# Log level.
loglevel = 'debug'

# Gunicorn timeout (in seconds) for handling requests.
timeout = 3600

# The WSGI application to be run by Gunicorn.
# Replace 'app' with the actual name of your Flask app object.
app = 'test_tools_worker:app'
