from flask import Flask, request
import logging
import uuid

class FlaskLogger(logging.LoggerAdapter):
    def __init__(self, logger, extra=None):
        super(FlaskLogger, self).__init__(logger, extra or {})

    def process(self, msg, kwargs):
        """
        Add extra information to the log message.
        """
        kwargs["extra"] = self.extra
        return msg, kwargs

app = Flask(__name__)

# Configuration for logging
app.config["LOG_FILE"] = "log_test.log"
app.config["LOG_LEVEL"] = logging.INFO

def setup_logger():
    logger = logging.getLogger("flask_app")
    logger.setLevel(app.config["LOG_LEVEL"])

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - [%(request_id)s] - [%(user_ip)s] -  %(message)s"
    )

    file_handler = logging.FileHandler(app.config["LOG_FILE"])
    file_handler.setLevel(app.config["LOG_LEVEL"])
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger

# Create an instance of FlaskLogger using the setup logger
flask_logger = FlaskLogger(setup_logger(), extra={"user_ip": "", "request_id": ""})

@app.before_request
def before_request():
    """
    Generate a unique request_id, add session_id, and user_ip to the FlaskLogger extra.
    """
    flask_logger.extra["request_id"] = str(uuid.uuid4())

    # Get the user IP address from the request
    user_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    flask_logger.extra["user_ip"] = user_ip

@app.errorhandler(Exception)
def handle_error(error):
    flask_logger.exception("An unhandled exception occurred.")
    return "An unexpected error occurred.", 500

@app.route("/")
def index():
    flask_logger.info("User accessed the index page.")
    flask_logger.info("An info occurred.")
    return "Hello, world!"

@app.route("/error")
def error():
    flask_logger.info("An info occurred.", exc_info=True)
    try:
        # Some code that raises an exception
        raise ValueError("This is a test error.")
    except Exception as e:
        flask_logger.error("An error occurred.", exc_info=True)
        return "An error occurred."

if __name__ == "__main__":
    app.run(debug=True)
