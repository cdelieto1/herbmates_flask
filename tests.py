from unittest import TestCase
from server import app
from seed_database import example_data
from flask import session

#set our application to testing mode. test_client returns a pretend brwoser. 
#app.testing = True


class TestFlaskLoginRoute(TestCase):
    """Stuff to do before testing"""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True


    def test_index(self):
        result = self.client.get('/login')
        self.assertIn(b'HerbMates Login', result.data)


class TestFlaskHomepageRoute(TestCase):
    """Test Flask routes."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_login(self):
        """Test login page to see if it contains user info + correct HTML."""

        result = self.client.post("/login",
                                  data={"email": "cassie1@gmail.com", "password": "hello"},
                                  follow_redirects=True)

        self.assertIn(b"HerbMates", result.data)


class FlaskTestsLoggedIn(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1
                sess['is_authenticated'] = True

    def test_important_page(self):
        """Test important page."""

        result = self.client.get("/")
        self.assertIn(b'Welcome to Herbmates', result.data)


class StatusCodeForLogin(TestCase):

    def test_home(self):
        client = app.test_client()
        app.config['TESTING'] = True

        result = client.get('/login')
        self.assertEqual(result.status_code, 200)        

#follow redirect = True in order to check in on routes without being in session

if __name__ == '__main__':
    # If called like a script, run our tests
    unittest.main()
         