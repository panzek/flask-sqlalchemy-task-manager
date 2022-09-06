# Since we will be defining the database, we obviously need to import db from the main taskmanager package.
from taskmanager import db
# In the SQLAlchemy CRUD sample, we imported each column type at the top of the file.
# However, with Flask-SQLAlchemy, the 'db' variable contains each of those already, and we can
# simply use dot-notation to specify the data-type for our columns.

# CREATE two separate tables, which will be represented by class-based models using SQLAlchemy's ORM.
# 1st table will be for various categories
class Category(db.Model): # using the default db.Model
    # Schema for the Category Model
    id = db.Column(db.Integer, primary_key=True) # with primary_key set to True, which will auto-increment each new record added to the database
    category_name = db.Column(db.String(25), unique=True, nullable=False) 
    # string, with a maximum character count of 25
    # and each new Category added to the database should be unique, why we set that to True
    # nullable=False - to make sure it's not empty or blank, this enforces that it's a required field
    tasks = db.relationship("Task", backref="category", cascade="all, delete", lazy=True)
    # We'll call this variable 'tasks' plural, not to be confused with the main Task class, and for this one, 
    # we need to use db.relationship instead of db.Column. Since we aren't using db.Column, this will not be 
    # visible on the database itself like the other columns, as it's just to reference the one-to-many relationship.
    # To link them, we need to specify which table is being targeted, which is "Task" in quotes.
    # We use 'backref' and the 'ondelete' cascade to create a relationship between the Category and Task models 
    # in this one-to-many connection, meaning it sort of reverses and becomes many-to-one.
    # It needs to back-reference itself, but in quotes and lowercase, so backref="category".
    # 'cascade' parameter set to 'all, delete', which means it will find all related tasks and delete them.
    # The last parameter here is lazy=True, which means that when we query the database for
    # categories, it can simultaneously identify any task linked to the categories.
       # (See ondelete="CASCADE" EXPLAINED below)

    # For each model, we also need to create a function called __repr__ that takes 
    # itself as the argument, similar to the 'this' keyword in JavaScript.
    def __repr__(self):
        # __repr__ to represent (the class object) itself in the form of a string 
        # Another function that you might see out there, is the __str__ function that behaves quite similar, and either should be suitable to use.
        return self.category_name


# 2nd table will be for each task created
class Task(db.Model): # using the default db.Model
    # Schema for the Task Model
    id = db.Column(db.Integer, primary_key=True) # with primary_key set to True, which will auto-increment each new record added to the database
    task_name = db.Column(db.String(50), unique=True, nullable=False) 
    task_description = db.Column(db.Text, nullable=False) # allows longer strings to be used, similar to textareas versus inputs
    is_urgent = db.Column(db.Boolean, default=False, nullable=False)
    due_date = db.Column(db.Date, nullable=False) # if you need to include time on your database, then db.DateTime or db.Time are suitable
    # you can see a full list of column and data types from the SQLAlchemy docs, which include Integer, Float, Text, String, Date, Boolean, etc.
    category_id = db.Column(db.Integer, db.ForeignKey("category.id", ondelete="CASCADE"), nullable=False) 
    # The value of foreign key will point to the ID from our Category class, and therefore we need to use lowercase 'category.id' in quotes.
    def __repr__(self): # __repr__ to represent (the class object) itself in the form of a string 
        return "#{0} - Task: {1} | Urgent: {2}".format(
            self.id, self.task_name, self.is_urgent
        )
        # ALTERNATIVE RETURN: return f"#{self.id} - Task:{self.task_name} | Urgent:{self.is_urgent}" 
    # We could simply return self.task_name, but let's utilize some of Python's formatting to include different columns.
    # We'll use placeholders of {0}, {1}, and {2}, and then the Python .format() method to specify
    # that these equate to self.id, self.task_name, and self.is_urgent.

# ondelete="CASCADE" EXPLAINED
# In addition to this, we are going to apply something called ondelete="CASCADE" for this foreign key.
# Since each of our tasks need a category selected, this is what's known as a one-to-many relationship.
# One category can be applied to many different tasks, but one task cannot have many categories.
# If we were to apply many categories to a single task, this would be known as a many-to-many relationship.
# Let's assume that we have 10 tasks on our database, and 2 categories, with these two categories being assigned to 5 tasks each.
# Later, we decide to delete 1 of those categories, so any of the 5 tasks that have this specific
# category linked as a foreign key, will throw an error, since this ID is no longer available.
# This is where the ondelete="CASCADE" comes into play, and essentially means that once
# a category is deleted, it will perform a cascading effect and also delete any task linked to it.
# If these aren't deleted, and a task contains an invalid foreign key, then you will get errors.
# In order to properly link our foreign key and cascade deletion, we add "tasks" field to the Category table.