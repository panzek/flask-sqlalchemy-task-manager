# This will make sure to initialize our taskmanager application as a package, 
# allowing us to use our own imports, as well as any standard imports.
import os
import re
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
if os.path.exists("env.py"): 
    import env # noqa
# since we are not pushing the "env.py" file to GitHub, this file will not be visible once deployed to Heroku, and will throw an error.
# This is why we need to only import 'env' if the OS can find an existing file path for the env.py file itself.

# CREATE A FLASK APPLICATION OBJECT
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
if os.environ.get("DEVELOPMENT") == "True":
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL")  # local
else:
    uri = os.environ.get("DATABASE_URL")
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = uri  # heroku
# create an instance of the imported Flask() class, which takes the default 
# Flask __name__ module, and that will be stored in a variable called 'app',
# We specify two app configuration variables, and these will both come from our environment variables.
# app.config SECRET_KEY and app.config SQLALCHEMY_DATABASE_URI, both wrapped in square brackets and quotes.
# Each of these will be set to get their respective environment variable, which is SECRET_KEY,
# and the short and sweet DB_URL for the database location which we'll set up later.

# create an instance of the imported SQLAlchemy() class, which will be
# assigned to a variable of 'db', and set to the instance of our Flask 'app'
db = SQLAlchemy(app)

from taskmanager import routes # noqa for 'No Quality Assurance'
# the linting is complaining about custom import not added at the top of the file with the other imports.
# The reason this is being imported last is because the 'routes' file will rely on using both the 'app' and 'db' variables defined above.
# If we try to import routes before 'app' and 'db' are defined, we'll get "circular-import errors", 
# meaning those variables aren't yet available to use, as they're defined after the routes.
# These linting warnings are technically not accurate, so to stop the warnings, add a comment at the end of each line: # noqa for 'No Quality Assurance'.