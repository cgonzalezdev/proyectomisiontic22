import os

SECRET_KEY = os.urandom(32)

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Configuration of the server
USE_RELOADER = True
THREADED = False
HOST = "0.0.0.0"
DEBUG = True

# Name database
NAME_DATABASE = "dbECommerce.db"