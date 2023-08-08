# gunicorn_config.py
# Documentation link - https://docs.gunicorn.org/en/latest/design.html

# Number of worker processes. There are 16 CPU cores on my server. Recommendation is (2*cpu+1)
workers = 17  

# Number of threads per worker. Adjust this based on your server's resources and app's behavior.
#threads = 16

# Host and port on which Gunicorn will listen.
bind = '0.0.0.0:8444'

# Log level.
loglevel = 'debug'

# Gunicorn timeout (in seconds) for handling requests. A worker needs maximum 30-60 seconds to process a request. If worker takes longer, Gunicorn will restart it.  
timeout = 90

# errorlog = '/var/log/log_new_orion/gunicorn_error.log'
# accesslog = '/var/log/log_new_orion/gunicorn_access.log'

# Default sync worker does not support persistent connections - each connection is closed after response has been sent even if you manually add Keep-Alive.
worker_class = "gevent"
#worker_class = "sync"
#keepalive = 5

# The WSGI application to be run by Gunicorn.
app = 'app:app'

