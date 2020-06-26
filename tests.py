import unittest
import json
#from model import *
from server import *

# set our application to testing mode
app.testing = True


class TestFlaskRoutes(unittest.TestCase):
    """Test Flask routes."""

    def test_index(self):
        """Make sure index page returns correct HTML."""

        # Create a test client
        client = app.test_client()

        # Use the test client to make requests
        result = client.get('/login')

        # Compare result.data with assert method
        self.assertIn(b'<h1>', result.data)

    # def test_favorite_color_form(self):
    #     """Test that /fav-color route processes form data correctly."""

    #     client = app.test_client()
    #     result = client.post('/fav-color', data={'color': 'blue'})

    #     self.assertIn(b'Woah! I like blue, too', result.data)


class MyAppIntegrationTestCase2(unittest.TestCase):
    """Examples of integration tests: testing Flask server."""

    def setUp(self):
        # print("(setUp ran)")
        self.client = app.test_client()
        app.config['TESTING'] = True

    def tearDown(self):
        # We don't need to do anything here; we could just
        # not define this method at all, but we have a stub
        # here as an example.
        # print("(tearDown ran)")
        return

    def test_index(self):
        result = self.client.get('/login')
        self.assertIn(b'<h1>intentional error', result.data)

    # def test_favorite_color_form(self):
    #     result = self.client.post('/fav-color', data={'color': 'blue'})
    #     self.assertIn(b'Woah! I like blue, too', result.data)


class MyTest(unittest.TestCase):

    def test_home(self):
        client = app.test_client()
        app.config['TESTING'] = True

        result = client.get('/login')
        self.assertEqual(result.status_code, 200)        


if __name__ == '__main__':
    # If called like a script, run our tests
    unittest.main()
         