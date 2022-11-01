
import unittest
import json
from app import app, db
from settings.settings import DB_NAME, DB_PASSWORD, DB_USER
from flask_sqlalchemy import SQLAlchemy

class ChirprTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.database_path = "postgresql://{}:{}@{}/{}".format(DB_USER,DB_PASSWORD,'localhost:5432', DB_NAME)
        app.config["SQLALCHEMY_DATABASE_URI"] = self.database_path
        self.new_user = {
            "id": "random_author",
            "name": "Test User",
            "url": "https://demo.jpg",
            "tweets": [],
        }
        self.login_user = {
            "id": "random_author",
            "name": "Test User",
        }
        self.new_tweet = {
        "id": "8xf0y6ziyjabvozdd253ng",
        "text": "Shoutout to all the speakers I know for whom English is not a first language, but can STILL explain a concept well. It's hard enough to give a good talk in your mother tongue!",
        "author": "sarah_edo",
        "timestamp": 1518122597860,
        "likes": [],
        "replies": [],
        "replying_to": "",
        }
        self.new_bookmark = {
        "id": "8xf0y6ziyjabvozdd253ng",
        "text": "Shoutout to all the speakers I know for whom English is not a first language, but can STILL explain a concept well. It's hard enough to give a good talk in your mother tongue!",
        "author": "sarah_edo",
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
        self.search_term = {
            "search_term": "speakers"
        }
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        db.session.rollback()
        pass

    
    def test_hello_world(self):
        res = self.client().get('/')
        data = res.data

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data, b'Hello, World!')
        
    def test_smiley(self):
        res = self.client().get('/smiley')
        data = res.data

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data, b':)')

    def test_get_users(self):
        res = self.client().get('/users')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_users(self):
        res = self.client().post('/users/create', json=self.new_user)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_login_user(self):
        res = self.client().post('/login', json=self.login_user)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_get_user_by_id(self):
        res = self.client().get('/users/{}'.format(self.new_user['id']))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_get_tweets(self):
        res = self.client().get('/tweets')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_create_tweets(self):
        res = self.client().post('/tweets/create', json=self.new_tweet)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_get_tweets_by_id(self):
        res = self.client().get('/tweets/{}'.format(self.new_tweet['id']))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_like_tweets_by_id(self):
        res = self.client().patch('/tweets/{}'.format(self.new_tweet['id']),json=self.like_tweet)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_reply_tweets_by_id(self):
        res = self.client().patch('/tweets/{}'.format(self.new_tweet['id']),json=self.reply_tweet)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_replying_to_tweets_by_id(self):
        res = self.client().patch('/tweets/{}'.format(self.new_tweet['id']),json=self.replying_to)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_create_bookmark(self):
        res = self.client().post('/bookmarks/create', json=self.new_bookmark)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    
    def test_get_bookmark_by_user(self):
        res = self.client().get('/bookmarks/{}'.format(self.new_user['id']))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_bookmark_by_user(self):
        res = self.client().get('/bookmarks/{}'.format(self.new_bookmark['author']))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_bookmark_by_id(self):
        res = self.client().delete('/bookmarks/{}'.format(self.new_bookmark['id']))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_search_bookmark_by_term(self):
        res = self.client().post('/bookmarks/search', json=self.search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()