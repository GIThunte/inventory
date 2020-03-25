"""
The module for run main application
Example for start:
/usr/local/bin/gunicorn --bind 0.0.0.0:5000 wsgi:app
"""
from inventory import app

if __name__ == "__main__":
    app.run()
