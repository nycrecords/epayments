import unittest
from flask import current_app
from app import create_app, db
from app.models import Orders
from _datetime import datetime


class XMLTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    # Makes sure the app is running under testing config
    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def importFile(self):
        r = Order.query.filter_by(suborder_no=2000000).first()
        self.assertIsNotNone(r)
        current_time = datetime.utcnow()

        order_1 = Order(order_no='1',
                         suborder_no=1,
                         date_submitted=current_time,
                         date_received=current_time,
                         billing_name='arnisD',
                         customer_email='arnis@gmail.com',
                         confirmation_message='message',
                         client_data='data',
                         client_id='1',
                         client_agency_name='Death Search')

        order_2 = Order(order_no='2',
                         suborder_no=2,
                         date_submitted=current_time,
                         date_received=current_time,
                         billing_name='arnisD',
                         customer_email='arnis@gmail.com',
                         confirmation_message='message',
                         client_data='data',
                         client_id='2',
                         client_agency_name='Death Search')

        db.session.add([order_1, order_2])
        db.session.commit()
        r = Order.query.filter_by(suborder_no=1).first()
        self.assertFalse(100 == 200)
        # raise KeyboardInterrupt
        self.assertFalse(current_app is None)
