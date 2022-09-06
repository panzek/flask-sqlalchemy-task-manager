from flask import render_template, request, redirect, url_for
from taskmanager import app, db
from taskmanager.models import Category, Task # "taskmanager.model" - to access model file inside the taskmanager folder


@app.route("/")
def home():
    tasks = list(Task.query.order_by(Task.id).all())
    return render_template("tasks.html", tasks=tasks)
# we create a basic "app route" using the root-level directory of slash
# This will be used to target a function called 'home', which will just 
# return the rendered_template of "base.html" that we will create shortly.
# After creating these, go to base.html and link it to these functions
# Whenever you use the url_for() method on your links, it's important to note 
# that these - add_categories(), categories() - are calling the actual Python functions, 
# not the app.route - /add_categories, even though these are often the same name.

# To view our tasks, we have to extract all of the tasks from our database. 
# Since we've got our tasks listed on the home page, we add a new variable called 'tasks' on the 'home' function. 
# Using the imported Task model, we query all tasks found, and if you wanted to, you could have them ordered by the Task.id as well. 
# The only thing left to do on this file is to pass that list over to the front-end template, which we will also call 'tasks', and set that to our tasks list above.


@app.route("/categories")
def categories():
    categories = list(Category.query.order_by(Category.category_name).all())
    return render_template("categories.html", categories=categories)

# Category.query.all() - query the 'Category' model imported at the top of the file from our models.py file
# Sometimes though, categories might be added at different times, so this would have the
# default method of sorting by the primary key when things get added.
# So, use the .order_by() method and have it sort by the key of 'category_name'.
# We also need to make sure that we tell it the specific model as well: "Category." even though it might seem redundant
# we make sure the quantifier, which is .all() in this case, is at the end of the query, after the .order_by() method.
# By using the .all() method, this is actually what's known as a Cursor Object, which is quite similar to an array or list of records.
# Even if the result comes back with a single record, it's still considered a "Cursor Object",
# and sometimes Cursor Objects can be confusing when using them on front-end templates.
# Thankfully, there's a simple Python method that can easily convert this Cursor Object into a standard Python list, 
# by wrapping the variable inside of 'list()' - list(Category.query.order_by(Category.category_name).all()) 

# we then pass this variable into our rendered template, so that we can use this data to display everything to our users: categories=categories.
# The first declaration of 'categories' is the variable name that we can now use within the HTML template: "/categories".
# The second 'categories', is the variable which is now (set to) a list() within our function above, 
# which is why, once again, it's important to keep your naming convention quite similar.

# now that we have this template variable available to us, we then go back to our categories.html template, to incorporate it into our cards.

@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        category = Category(category_name=request.form.get("category_name"))
        db.session.add(category)
        db.session.commit()
        return redirect(url_for("categories"))
    return render_template("add_category.html")
# we include a list of the two methods: "GET" and "POST",  because we'll be submitting a form to the database.
# When a user clicks to add a new category, it should render the template that contains
# a form, and by displaying the form to users, this uses the "GET" method to 'get' the page.
# However, when a user eventually submits this form, the form will attempt to 'post' the
# data into the database, and this is why we need to specify both methods in the app route.

# to submit the form, and for it to work, we added the POST method functionality for
# users to add a new category to the database.
# If the requested method is equal to POST, then we will create a new variable called
# 'category', which will be set to a new instance of the Category() model imported at the top of the file.
# the 'request' method is an import from Flask at the top here.
# make sure that this Category model uses the same exact keys that the model is
# expecting, so when in doubt, copy from the model directly.

# For this category_name field, we can then use the requested form being posted to retrieve the name-attribute.
# This is why it's important to keep the naming convention consistent, which means our name-attribute (category_name= ) 
# matches that of our database model, the category_name being get from form: request.form.get("category_name").
# Once we've grabbed the form data, we can then 'add' and 'commit' this information to the
# SQLAlchemy database variable of 'db' (imported at the top of the file): db.session.add(category).
# This will use the database sessionmaker instance

# After the form gets submitted, and we're adding and committing the new data to our database,
# we could redirect the user back to the 'categories' page.
# 'redirect' and 'url_for' classes at the top of the file from our flask import.

# so let's quickly recap what's happening here.
# When a user clicks the "Add Category" button, this will use the "GET" method and render the 'add_category' template.
# Once they submit the form, this will call the same function, but will check if the request
# being made is a “POST“ method, which posts data somewhere, such as a database.
# Anything that needs to be handled by the POST method, should be indented properly within this condition.
# By default, the normal method is GET, so it will behave as the 'else' condition since it's not part of the indented POST block.
# Technically, you could separate this into two separate functions, which would handle the GET and POST methods completely apart.
# Also, in a real-world scenario in a production environment, you'd probably want to consider
# adding defensive programming to handle brute-force attacks, along with some error handling.

@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    categories = list(Category.query.order_by(Category.category_name).all())
    if request.method == "POST":
        task = Task(
            task_name=request.form.get("task_name"),
            task_description=request.form.get("task_description"),
            is_urgent=bool(True if request.form.get("is_urgent") else False),
            due_date=request.form.get("due_date"),
            category_id=request.form.get("category_id")
        )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_task.html", categories=categories)
# this function will render a new template for users to add a new Task, and then commit those new tasks to the database if the form is submitted. 
# It's actually quite similar to the 'add_category' function. However, each task actually requires the user to select a category for that task. 
# In order to do that, we first need to extract a list of all of the categories available from the database.
# However, we aren't going to be inserting a new category into the database, but rather a new task.
# From our models.py file, each task must have a few different elements, including a task name, description, due date, category, 
# and whether or not it's urgent. That means we need to update the POST method to reflect each of the fields that will be added from the form

# Task name will be set to the form's name attribute of 'task_name'.
# Task description will use the form's 'task_description' field
# The 'is_urgent' field will be a Boolean, either true or false, so we'll make it True if the
# form data is toggled on, otherwise it will be set to False by default.
# Due date will of course be the form's 'due_date' input box.
# Tthe last column for each Task will be the selected Category ID, which will be generated as a dropdown list to choose from, using the 'categories' list above.

# Once the form is submitted, we can add that new 'task' variable to the database session, and then immediately commit those changes to the database.
# If successful, then we can redirect the user back to the 'home' page where each task will eventually be displayed.
# That concludes the POST functionality when users add a new Task to the database.

# If, however, the method isn't POST, and a user is trying to add a new task, they need to be displayed with the page that contains the form.
# This should render the template for "add_task.html", and in order for the dropdown list to display each available category, we need to pass that variable into the template.
# As a reminder, the first 'categories' listed is the variable name that we will be able to use on the template itself.
# The second 'categories' is simply the list of categories retrieved from the database defined above.
# That's all we need for the 'add_task' function, which will render the template for new tasks.
# The next thing we need to do is build that template which allows users to add new tasks: "add_task.html"

@app.route("/edit_task/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    categories = list(Category.query.order_by(Category.category_name).all())
    if request.method == "POST":
        task.task_name = request.form.get("task_name")
        task.task_description = request.form.get("task_description")
        task.is_urgent = bool(True if request.form.get("is_urgent") else False)
        task.due_date = request.form.get("due_date")
        task.category_id = request.form.get("category_id")
        db.session.commit()
    return render_template("edit_task.html", task=task, categories=categories)
# when we created the edit_category function, we used the 'get_or_404()' method, which queries the database using that task ID.
# Now, instead of using the Task model, we can simply update each column-header using dot-notation.
# We already have each field here, so we just need to adjust the formatting for Python to remove the original Task() model, and give it proper indentation.
# Do this for each field, adding 'task dot' in front of each column-header, such as 'task.task_name', or 'task.due_date'.
# It's important to do this for all fields, even if the user would only like to update one of them.
# If we don't include all fields, and the user only updates the task_name for example, then the other fields risk being deleted entirely.
# Since we are modifying the specific task here, we don't need to use session.add(), and only session.commit() is required for saving these changes. 
# Finally, we just need to render our new template of 'edit_task.html', and along with the normal 'categories' selection, we need to pass through the task itself.

# Next, open up the tasks.html template because we need a method for users to click a button that opens up this template for editing.

@app.route("/edit_category/<int:category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    if request.method == "POST":
        category.category_name = request.form.get("category_name")
        db.session.commit()
        return redirect(url_for("categories"))
    return render_template("edit_category.html", category=category)

# once we added the primary key of ID into our app.route function, it will now always expect this for any link that calls this function. 
# Let's go back to the edit_category template, and provide the same exact argument of 'category_id' like we did on the href for the Edit button.
# Using the imported Category model from the top of the file, we need to query the database,
# and this time we know a specific record we'd like to retrieve.
# There's a SQLAlchemy method called '.get_or_404()', which takes the argument of 'category_id'.
# What this does is query the database and attempts to find the specified record using the data
# provided, and if no match is found, it will trigger a 404 error page.

@app.route("/delete_category/<int:category_id>")
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for("categories"))

# As is tradition by now, our function name will take the same name, "delete_category"
# First, we need to pass the category ID into our app route and function, and once again, we are casting it as an integer.
# Next, we should attempt to query the Category table using this ID, and store it inside of a variable called 'category'.
# If there isn't a matching record found, then it should automatically return an error 404 page.
# Then, using the database session, we need to perform the .delete() method using that 'category' variable, and then commit the session changes.
# Finally, once that's been deleted and our session has been committed, we can simply redirect the user back to the function above called "categories".

# Then go to the "categories" template to update our href link: {{ url_for('delete_category', category_id=category.id)}}
# As you can see, since we are within the for-loop of all categories, it's using the current
# iteration variable of 'category', and then targeting the key of 'id' from that record.
# The 'category_id' assigned is just the variable name we're passing into the "app.route" function that we just created within the routes.py file.

# Converting Database Queries into actual Python Lists. 
# Whenever you query the database, you actually get something returned called a Cursor Object, sometimes called a QuerySet. 
# In some cases, you can't use a Cursor Object on the front-end, or with some of the Jinja template filters. 
# Oftentimes, it's actually better to convert your queries into Python lists.
# And since we want this to occur only for queries that have more than one result, we focus on any that end with '.all()',
# Thus wrapping any query in a Python list(), which is considered best practice.

# DELETE TASK 
@app.route("/delete_task/<int:task_id>")
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("home"))
# When this function is called, it takes the 'task_id' variable, and tries to query the database to find that particular task.
# It will then remove the task using the .delete() method, and then commit those changes to our database.
# Once the task is deleted, we redirect the user back to the home page where our tasks are displayed.

# DEFENSIVE PROGRAMMING & USER AUTHENTICATION
# In a real world scenario, you should ideally add some DEFENSIVE PROGRAMMING, so that a user must first confirm whether 
# they want to delete the task. Also, having user authentication is quite important, so that way only the user who created 
# that task, should be able to delete that task. You will want your database protected, so that a user can't simply 
# brute-force their way around your application. Currently, these app routes aren't protected, so any visitor to the site 
# can add, edit, or delete any task or category, which is not secure. 