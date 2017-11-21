import unittest
import json
import re
from base64 import b64encode
from flask import url_for, current_app
from app import create_app, db
from app.models import Order, Customer, BirthSearch, BirthCertificate, MarriageSearch, MarriageCertificate, \
                     DeathSearch, DeathCertificate, PhotoGallery, PhotoTax, PropertyCard
from datetime import datetime


class APITestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        # Order.suborder_no()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    #  Test the import file function in utils
    # Need to test that if a correct XML file came in, and it was ripped of correctly
    # that everything will get inputed into the tables
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

        raise KeyboardInterrupt







    # def test_get_orders_by_fields(self):

    # def test_posts(self):
    #     # add a user
    #     r = Role.query.filter_by(name='User').first()
    #     self.assertIsNotNone(r)
    #     u = User(email='john@example.com', password='cat', confirmed=True,
    #              role=r)
    #     db.session.add(u)
    #     db.session.commit()
    #
    #     # write an empty post
    #     response = self.client.post(
    #         url_for('api.new_post'),
    #         headers=self.get_api_headers('john@example.com', 'cat'),
    #         data=json.dumps({'body': ''}))
    #     self.assertTrue(response.status_code == 400)
    #
    #     # write a post
    #     response = self.client.post(
    #         url_for('api.new_post'),
    #         headers=self.get_api_headers('john@example.com', 'cat'),
    #         data=json.dumps({'body': 'body of the *blog* post'}))
    #     self.assertTrue(response.status_code == 201)
    #     url = response.headers.get('Location')
    #     self.assertIsNotNone(url)
    #
    #     # get the new post
    #     response = self.client.get(
    #         url,
    #         headers=self.get_api_headers('john@example.com', 'cat'))
    #     self.assertTrue(response.status_code == 200)
    #     json_response = json.loads(response.data.decode('utf-8'))
    #     self.assertTrue(json_response['url'] == url)
    #     self.assertTrue(json_response['body'] == 'body of the *blog* post')
    #     self.assertTrue(json_response['body_html'] ==
    #                     '<p>body of the <em>blog</em> post</p>')
    #     json_post = json_response
    #
    #     # get the post from the user
    #     response = self.client.get(
    #         url_for('api.get_user_posts', id=u.id),
    #         headers=self.get_api_headers('john@example.com', 'cat'))
    #     self.assertTrue(response.status_code == 200)
    #     json_response = json.loads(response.data.decode('utf-8'))
    #     self.assertIsNotNone(json_response.get('posts'))
    #     self.assertTrue(json_response.get('count', 0) == 1)
    #     self.assertTrue(json_response['posts'][0] == json_post)
    #
    #     # get the post from the user as a follower
    #     response = self.client.get(
    #         url_for('api.get_user_followed_posts', id=u.id),
    #         headers=self.get_api_headers('john@example.com', 'cat'))
    #     self.assertTrue(response.status_code == 200)
    #     json_response = json.loads(response.data.decode('utf-8'))
    #     self.assertIsNotNone(json_response.get('posts'))
    #     self.assertTrue(json_response.get('count', 0) == 1)
    #     self.assertTrue(json_response['posts'][0] == json_post)
    #
    #     # edit post
    #     response = self.client.put(
    #         url,
    #         headers=self.get_api_headers('john@example.com', 'cat'),
    #         data=json.dumps({'body': 'updated body'}))
    #     self.assertTrue(response.status_code == 200)
    #     json_response = json.loads(response.data.decode('utf-8'))
    #     self.assertTrue(json_response['url'] == url)
    #     self.assertTrue(json_response['body'] == 'updated body')
    #     self.assertTrue(json_response['body_html'] == '<p>updated body</p>')
    #
    # def test_users(self):
    #     # add two users
    #     r = Role.query.filter_by(name='User').first()
    #     self.assertIsNotNone(r)
    #     u1 = User(email='john@example.com', username='john',
    #               password='cat', confirmed=True, role=r)
    #     u2 = User(email='susan@example.com', username='susan',
    #               password='dog', confirmed=True, role=r)
    #     db.session.add_all([u1, u2])
    #     db.session.commit()
    #
    #     # get users
    #     response = self.client.get(
    #         url_for('api.get_user', id=u1.id),
    #         headers=self.get_api_headers('susan@example.com', 'dog'))
    #     self.assertTrue(response.status_code == 200)
    #     json_response = json.loads(response.data.decode('utf-8'))
    #     self.assertTrue(json_response['username'] == 'john')
    #     response = self.client.get(
    #         url_for('api.get_user', id=u2.id),
    #         headers=self.get_api_headers('susan@example.com', 'dog'))
    #     self.assertTrue(response.status_code == 200)
    #     json_response = json.loads(response.data.decode('utf-8'))
    #     self.assertTrue(json_response['username'] == 'susan')
    #
    # def test_comments(self):
    #     # add two users
    #     r = Role.query.filter_by(name='User').first()
    #     self.assertIsNotNone(r)
    #     u1 = User(email='john@example.com', username='john',
    #               password='cat', confirmed=True, role=r)
    #     u2 = User(email='susan@example.com', username='susan',
    #               password='dog', confirmed=True, role=r)
    #     db.session.add_all([u1, u2])
    #     db.session.commit()
    #
    #     # add a post
    #     post = Post(body='body of the post', author=u1)
    #     db.session.add(post)
    #     db.session.commit()
    #
    #     # write a comment
    #     response = self.client.post(
    #         url_for('api.new_post_comment', id=post.id),
    #         headers=self.get_api_headers('susan@example.com', 'dog'),
    #         data=json.dumps({'body': 'Good [post](http://example.com)!'}))
    #     self.assertTrue(response.status_code == 201)
    #     json_response = json.loads(response.data.decode('utf-8'))
    #     url = response.headers.get('Location')
    #     self.assertIsNotNone(url)
    #     self.assertTrue(json_response['body'] ==
    #                     'Good [post](http://example.com)!')
    #     self.assertTrue(
    #         re.sub('<.*?>', '', json_response['body_html']) == 'Good post!')
    #
    #     # get the new comment
    #     response = self.client.get(
    #         url,
    #         headers=self.get_api_headers('john@example.com', 'cat'))
    #     self.assertTrue(response.status_code == 200)
    #     json_response = json.loads(response.data.decode('utf-8'))
    #     self.assertTrue(json_response['url'] == url)
    #     self.assertTrue(json_response['body'] ==
    #                     'Good [post](http://example.com)!')
    #
    #     # add another comment
    #     comment = Comment(body='Thank you!', author=u1, post=post)
    #     db.session.add(comment)
    #     db.session.commit()
    #
    #     # get the two comments from the post
    #     response = self.client.get(
    #         url_for('api.get_post_comments', id=post.id),
    #         headers=self.get_api_headers('susan@example.com', 'dog'))
    #     self.assertTrue(response.status_code == 200)
    #     json_response = json.loads(response.data.decode('utf-8'))
    #     self.assertIsNotNone(json_response.get('comments'))
    #     self.assertTrue(json_response.get('count', 0) == 2)
    #
    #     # get all the comments
    #     response = self.client.get(
    #         url_for('api.get_comments', id=post.id),
    #         headers=self.get_api_headers('susan@example.com', 'dog'))
    #     self.assertTrue(response.status_code == 200)
    #     json_response = json.loads(response.data.decode('utf-8'))
    #     self.assertIsNotNone(json_response.get('comments'))
    #     self.assertTrue(json_response.get('count', 0) == 2)
