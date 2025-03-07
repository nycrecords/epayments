import unittest
from flask import current_app, url_for
from app import create_app, db


class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        # Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):  # Test the Home page, that Epayments comes up
        response = self.client.get(url_for('main.index'))
        self.assertTrue(b'Epayments' in response.data)

