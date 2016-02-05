# project/test.py


import os
import unittest

from views import app, db
from _config import basedir
from models import User

TEST_DB = 'test.db'


class AllTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

    # executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()


    ############################
    ##### helper functions #####
    ############################

    def login(self, name, password):
        return self.app.post('/', data=dict(name=name, password=password), follow_redirects=True)

    def register(self, name, email, password, confirm):
        return self.app.post(
            'register/',
            data=dict(name=name, email=email, password=password, confirm=confirm),
            follow_redirects=True
        )

    def logout(self):
        return self.app.get('logout/', follow_redirects=True)

    def create_user(self, name, email, password):
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

    def create_task(self):
        return self.app.post('add/', data=dict(
                name='Go to the bank',
                due_date='02/05/2014',
                priority='1',
                posted_date='02/04/2014',
                status='1'
            ), follow_redirects=True)


    ############################
    ######## dummy data ########
    ############################

    michael_register = ['Michael', 'michael@realpython.com', 'python', 'python']
    michael_create_user = ['Michael', 'michael@realpython.com', 'python']
    michael_login = ['Michael', 'python']

    fletcher_register = ['Fletcher', 'fletcher@realpython.com', 'python', 'python']
    fletcher_create_user = ['Fletcher', 'fletcher@realpython.com', 'python']
    fletcher_login = ['Fletcher', 'python']


    ############################
    ######### the tests ########
    ############################

    # each test should start with 'test'
    def test_user_setup(self):
        new_user = User("michael", "michael@mherman.org", "michaelherman")
        db.session.add(new_user)
        db.session.commit()
        test = db.session.query(User).all()
        for t in test:
            t.name
        assert t.name == "michael"

    def test_form_is_present_on_login_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<form class="form-signin" role="form" method="post" action="/">', response.data)

    def test_login(self):
        # not registered
        response = self.login('foo', 'bar')
        self.assertIn(b'Invalid username or password.', response.data)
        # registered
        self.register(*self.michael_register)
        response = self.login(*self.michael_login)
        self.assertIn('Welcome!', response.data)

    def test_invalid_form_data(self):
        self.register(*self.michael_register)
        response = self.login('alert("alert box!");', 'foo')
        self.assertIn(b'Invalid username or password.', response.data)

    def test_form_is_present_on_register_page(self):
        response = self.app.get('register/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<form action="/register/" method="post">', response.data)

    def test_user_registration(self):
        self.app.get('register/', follow_redirects=True)
        response = self.register(*self.michael_register)
        self.assertIn(b'Thanks for registering. Please login.', response.data)

    def test_user_registration_user_exists_error(self):
        self.app.get('register/', follow_redirects=True)
        response = self.register(*self.michael_register)
        self.app.get('register/', follow_redirects=True)
        response = self.register(*self.michael_register)
        self.assertIn(b'That username and/or email already exists.', response.data)

    def test_logout(self):
        # not logged in
        response = self.logout()
        self.assertNotIn(b'Goodbye!', response.data)
        # logged in
        self.register(*self.michael_register)
        self.login(*self.michael_login)
        response = self.logout()
        self.assertIn(b'Goodbye!', response.data)

    def test_task_page_access(self):
        # not logged in
        response = self.app.get('tasks/', follow_redirects=True)
        self.assertIn(b'You need to login first.', response.data)
        # logged in
        self.register(*self.michael_register)
        self.login(*self.michael_login)
        response = self.app.get('tasks/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add a new task:', response.data)

    def test_users_can_add_tasks(self):
        self.create_user(*self.michael_create_user)
        self.login(*self.michael_login)
        self.app.get('tasks/', follow_redirects=True)
        response = self.create_task()
        self.assertIn(b'New entry was successfully posted. Thanks!', response.data)

    def test_users_cannot_add_tasks_when_error(self):
        self.create_user(*self.michael_create_user)
        self.login(*self.michael_login)
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.post('add/', data=dict(
            name='Go to the bank',
            due_date='',
            priority='1',
            posted_date='02/05/2014',
            status='1'
        ), follow_redirects=True)
        self.assertIn(b'This field is required.', response.data)

    def test_users_can_complete_tasks(self):
        self.create_user(*self.michael_create_user)
        self.login(*self.michael_login)
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        response = self.app.get('complete/1/', follow_redirects=True)
        self.assertIn(b'The task is complete! Nice.', response.data)

    def test_users_can_delete_tasks(self):
        self.create_user(*self.michael_create_user)
        self.login(*self.michael_login)
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        response = self.app.get('delete/1/', follow_redirects=True)
        self.assertIn(b'The task was deleted.', response.data)

    def test_users_cannot_complete_tasks_not_created_by_them(self):
        self.create_user(*self.michael_create_user)
        self.login(*self.michael_login)
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        self.logout()
        self.create_user(*self.fletcher_create_user)
        self.login(*self.fletcher_login)
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.get('complete/1/', follow_redirects=True)
        self.assertNotIn(b'The task is complete! Nice.', response.data)



if __name__ == '__main__':
    unittest.main()