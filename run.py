# this is the main Python file that will actually run the entire application.
# This file is at the root level of our workspace, not part of the taskmanager package itself.
# Since it will run the whole application, we just call it "run.py".

import os # we import os in order to utilize "environment variables" within this file.
from taskmanager import app # import the 'app' variable that we've created within our taskmanager package 

# defined in the init file. The last step to run our application is to tell our app how and where to run the application.
if __name__ == "__main__": 
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=os.environ.get("DEBUGG")
    )

# checking that the 'name' class is equal to the default 'main' string, wrapped in double underscores
# If it's a match, then we need to have our app running, which will take three arguments: 'host', 'port', and 'debug'.
# Each of these, as you may recall, are stored in the environment variables, so we need to use os.environ.get().
# The host is the IP, the port is PORT, but that needs to be converted into an integer, and then debug is DEBUG.

# GO CREATE TEMPLATES FOLDER & ADD base.html FILE
# we need to render some sort of front-end template to verify that the application is running successfully
# Within our taskmanager package, let's create a new directory called 'templates', which is where Flask looks 
# for any HTML templates to be rendered. Then, within this templates directory, we will create a new file called 
# base.html, which is what will be rendered from our routes.py file.