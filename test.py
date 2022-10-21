import os
import unittest
import json
from flaskr import create_app
from models import setup_db, Users, Tweets,Bookmarks, db
from settings import DB_NAME, DB_PASSWORD, DB_USER
# from settings import DB_NAME, DB_USER, DB_PASSWORD

class ChirprTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        # self.database_name = "test_db"
        self.database_path = "postgresql://{}:{}@{}/{}".format(DB_USER,DB_PASSWORD,'localhost:5432', DB_NAME)
        setup_db(self.app, self.database_path)
        self.new_user = {
            "id": "random_author_1",
            "name": "Test User",
            "url": "https://demo.jpg",
            "tweets": [],
        }
        self.new_tweet = {
        "id": "8xf0y6ziyjabvozdd253ne",
        "text": "Shoutout to all the speakers I know for whom English is not a first language, but can STILL explain a concept well. It's hard enough to give a good talk in your mother tongue!",
        "author": "random_author_1",
        "timestamp": 1518122597860,
        "likes": [],
        "replies": [],
        "replying_to": "",
        }
        self.new_bookmark = {
        "id": "8xf0y6ziyjabvozdd253ne",
        "text": "Shoutout to all the speakers I know for whom English is not a first language, but can STILL explain a concept well. It's hard enough to give a good talk in your mother tongue!",
        "author": "random_author_1",
        "timestamp": 1518122597860,
        "likes": [],
        "replies": [],
        "replying_to": "",
        }
        self.like_tweet = {
            "likes": "random_user"
        }
        self.reply_tweet = {
            "replies": "random_tweet_id"
        }
        self.replying_to = {
            "replying_to": "parent_tweet_id"
        }
        # self.search = {"searchTerm": "title"}
        # self.new_quiz_wrong = {'question': []}
        # self.new_quiz = {'previous_questions': [18,20,21],'quiz_category': {'type': 'play', 'id': 5}}
        # binds the app to the current context
        # with self.app.app_context():
        #     self.db = SQLAlchemy()
        #     self.db.init_app(self.app)
        #     # create all tables
        #     self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        db.session.rollback()
        pass

    
    def test_hello_world(self):
        res = self.client().get('/')
        data = res.data

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data, b'Hello, World!')
        # self.assertEqual(len(data['categories']),6)
        
    def test_smiley(self):
        res = self.client().get('/smiley')
        data = res.data

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data, b':)')
        # self.assertEqual(len(data['categories']),6)

    def test_get_users(self):
        res = self.client().get('/users')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # self.assertEqual(len(data['categories']),6)

    def test_create_users(self):
        res = self.client().post('/users/create', json=self.new_user)
        # db.session.flush()
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # db.session.rollback()

        # self.assertEqual(len(data['categories']),6)

    def test_get_user_by_id(self):
        res = self.client().get('/users/{}'.format(self.new_user['id']))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # self.assertEqual(len(data['categories']),6)
    
    def test_get_tweets(self):
        res = self.client().get('/tweets')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # self.assertEqual(len(data['categories']),6)
    
    def test_create_tweets(self):
        res = self.client().post('/tweets/create', json=self.new_tweet)
        # db.session.flush()
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # db.session.rollback()

        # self.assertEqual(len(data['categories']),6)

    def test_get_tweets_by_id(self):
        res = self.client().get('/tweets/{}'.format(self.new_tweet['id']))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # self.assertEqual(len(data['categories']),6)

    def test_like_tweets_by_id(self):
        res = self.client().patch('/tweets/{}'.format(self.new_tweet['id']),json=self.like_tweet)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # self.assertEqual(len(data['categories']),6)

    def test_reply_tweets_by_id(self):
        res = self.client().patch('/tweets/{}'.format(self.new_tweet['id']),json=self.reply_tweet)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # self.assertEqual(len(data['categories']),6)

    def test_replying_to_tweets_by_id(self):
        res = self.client().patch('/tweets/{}'.format(self.new_tweet['id']),json=self.replying_to)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # self.assertEqual(len(data['categories']),6)
    
    def test_create_bookmark(self):
        res = self.client().post('/bookmarks/create', json=self.new_bookmark)
        # db.session.flush()
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    
    def test_get_bookmark_by_user(self):
        res = self.client().get('/bookmarks/{}'.format(self.new_user['id']))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # self.assertEqual(len(data['categories']),6)

    def test_get_bookmark_by_id(self):
        res = self.client().get('/bookmarks/{}'.format(self.new_bookmark['id']))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # self.assertEqual(len(data['categories']),6)

    def test_get_bookmark_by_id(self):
        res = self.client().delete('/bookmarks/{}'.format(self.new_bookmark['id']))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # self.assertEqual(len(data['categories']),6)

    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()