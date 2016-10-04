"""
    This runs the main server if it's started from the
    commandline or run in an IDE (PyCharm)
"""
from app import app
if __name__ == "__main__":
    if "SSL_CRT" in app.config and "SSL_KEY" in app.config:
        context=(app.config['SSL_CRT'], app.config['SSL_KEY'])
        app.run(ssl_context=context, port=app.config['PORT'], debug=app.config['DEBUG'])
    else:
        app.run(port=app.config['PORT'], debug=app.config['DEBUG'])
