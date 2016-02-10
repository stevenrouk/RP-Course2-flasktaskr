# db_create.py


from datetime import date

from project import db
from project.models import Task, User


# create the database and the db table
db.create_all()

# insert dummy data
#db.session.add(User('admin', 'ad@min.com', 'admin', 'admin'))
#db.session.add(Task("Finish this tutorial", date(2016, 1, 13), 10, date(2016, 2, 10), 1, 1))
#db.session.add(Task("Finish RP Course 2", date(2016, 2, 1), 7, date(2016, 2, 10), 1, 1))

# commit the changes
db.session.commit()