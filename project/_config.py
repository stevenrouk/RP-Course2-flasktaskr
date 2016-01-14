# app configuration
# used to separate the app logic from static variables


import os


# grab the folder where this script lives
basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'flasktaskr.db'
WTF_CSRF_ENABLED = True
SECRET_KEY = 'something-no-one-will-ever-guess'

# define the full path for the database
DATABASE_PATH = os.path.join(basedir, DATABASE)

# the database uri
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH