# project/test.py


import os
import unittest

from project import app, db
from project._config import basedir
from project.models import Task, User

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

    def test_default_user_role(self):
        db.session.add(
            User(
                "Johnny",
                "john@doe.com",
                "johnny"
            )
        )
        db.session.commit()

        users = db.session.query(User).all()
        for user in users:
            self.assertEqual(user.role, 'user')


if __name__ == '__main__':
    unittest.main()