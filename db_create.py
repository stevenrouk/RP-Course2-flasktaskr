# project/db_create.py


from views import db
from models import Task
from datetime import date


# create the database and the db table
db.create_all()

# insert dummy data
#db.session.add(Task("Finish this tutorial", date(2016, 1, 13), 10, 1))
#db.session.add(Task("Finish RP Course 2", date(2016, 2, 1), 7, 1))

# commit the changes
db.session.commit()