from django.db import models

# ORM - object relational manager
# the ORM handles all our database interactions so we don't need to write SQL

# a model is considered to be 

# User Table

# |   id  |   first_name  |   last_name   |   email           |
# |   1   |   Chett       |   Tiller      |   chett@chett.net |
# |   2   |   Octavia     |   BaseExcepti |   octavia@octavia |

# Todo Model
class Todo(models.Model):

    # columns that are in the table

    task_name = models.CharField(max_length=100) # short string
    description = models.TextField() # long string
    completed = models.BooleanField() # boolean
    # some_number = models.IntegerField() # integer / number

    def __str__(self):
        return self.task_name

# making a migration means building the blueprint for the db
# committing the migration means using the blueprint to build the db

# CRUD - CREATE - READ - UPDATE - DELETE

# READ

# Todo.objects.all() --> get all the todo items
# Todo.objects.first() --> get the first item

# primary key --> the id / unique identifier for an item
# Todo.objects.get(pk=1) --> get the item with an id of 1

# CREATE

# todo1 = Todo(task_name="Learn Django", description="YOu gotta learn it", completed=False)
# todo1.save()

# UPDATE

# yoga = Todo.objects.get(pk=5)
# yoga.completed = True
# yoga.save()

# DELETE
# yoga.delete()