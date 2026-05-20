from django.db import models

# ORM - object relational manager
# the ORM handles all our database interactions so we don't need to write SQL

# a model is considered to be 

# Todo Table

# |   id  |   task_name  |   description   |   completed    |
# |   1   |   laundry    |   "do laundry"  |   True         |

# Todo Model
class Todo(models.Model):

    # columns that are in the table

    task_name = models.CharField(max_length=100) # short string
    description = models.TextField() # long string
    completed = models.BooleanField() # boolean
    # some_number = models.IntegerField() # integer / number

    # Sets the time only once when the object is first created
    created_at = models.DateTimeField(auto_now_add=True)
    # Often used alongside created_at to track last modification
    updated_at = models.DateTimeField(auto_now=True)

    # when looking at the string version of a model the __str__ shows the name
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


# Author
class Author(models.Model):
    name = models.CharField(max_length=100)
    pen_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Genre
class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# Book
class Book(models.Model):
    title = models.CharField(max_length=100)
    # the foreign key tracks the author this book belongs to
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    #                                  on_delete tells the book to get deleted whenever the author gets deleted
    #                                                            related_name has to do with the method we'll 
    #                                                            call when we try to get the books for the author


    # many to many field
    genres = models.ManyToManyField(Genre, blank=True, null=True)
    # books can have many genres && genres can have many books
    # blank=True and null=True mean a book doesn't need to have genres

    def __str__(self):
        return self.title

# has many - belongs to relationship
# Author has many Books
# Book belong to an Author