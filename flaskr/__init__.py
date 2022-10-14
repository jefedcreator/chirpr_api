# from sqlalchemy import *
from tkinter.messagebox import NO
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import null
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects.postgresql import BIGINT
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.ext.mutable import Mutable

class MutableList(Mutable, list):
    def append(self, value):
        list.append(self, value)
        self.changed()

    def pop(self, index=0):
        value = list.pop(self, index)
        self.changed()
        return value

    @classmethod
    def coerce(cls, key, value):
        if not isinstance(value, MutableList):
            if isinstance(value, list):
                return MutableList(value)
            return Mutable.coerce(key, value)
        else:
            return value


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:hemid8th@localhost:5432/chirpr'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    avatar_url = db.Column(db.String(), nullable=False)
    tweet_id = db.Column(MutableList.as_mutable(ARRAY(db.String())))
    # tweets = db.relationship('tweets', backref='users', lazy = True)
    # bookmarks = db.relationship('bookmarks', backref='users', lazy = True)

    def __repr__(self):
        return f'<Person ID: {self.id}, name: {self.name}>'

class Tweets(db.Model):
    __tablename__ = 'tweets'
    id = db.Column(db.String(), primary_key=True)
    text = db.Column(db.String(), nullable=False)
    author = db.Column(db.String(), nullable=False)
    timestamp = db.Column(BIGINT, nullable=False)
    likes = db.Column(MutableList.as_mutable(ARRAY(db.String())))
    replies = db.Column(MutableList.as_mutable(ARRAY(db.String())))
    replying_to = db.Column(db.String())
    # user_id = db.Column(db.String(), db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Person ID: {self.id}, name: {self.text}>'

class Bookmarks(db.Model):
    __tablename__ = 'bookmarks'
    id = db.Column(db.String(), primary_key=True)
    text = db.Column(db.String(), nullable=False)
    author = db.Column(db.String(), nullable=False)
    timestamp = db.Column(BIGINT, nullable=False)
    likes = db.Column(MutableList.as_mutable(ARRAY(db.String())))
    replies = db.Column(MutableList.as_mutable(ARRAY(db.String())))
    replying_to = db.Column(db.String())
    # user_id = db.Column(db.String(), db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Person ID: {self.id}, name: {self.text}>'

db.create_all()


# Create and configure the app
# Include the first parameter: Here, __name__is the name of the current Python module.

# Return the app instance
#  return app

@app.after_request
def after_request(response):
    response.headers.add(
        "Access-Control-Allow-Headers", "Content-Type, Authorization"
    )
    response.headers.add(
        "Access-Control-Allow-Headers", "GET, POST, PATCH, DELETE, OPTION"
    )
    return response

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/smiley')
def smiley():
    return ':)'

@app.route('/users')
def users():
    users = Users.query.order_by(Users.id).all()
    print('users', users)
    user_obj = {}
    for user in users:
        user_obj[user.id] = {
            'id':user.id,
            'name':user.name,
            'url':user.avatar_url,
            'tweets':user.tweet_id
        }

    return jsonify(
        {
            "success" : True,
            "users": user_obj
        }
    )

@app.route('/users/create', methods=['POST'])
def add_user():
    body = request.get_json()
    new_id = body.get("id", None)
    new_name = body.get("name", None)
    new_url = body.get("url", None)
    new_tweets = body.get("tweets", [])
    print("details are:", new_id, new_name,new_url,new_tweets)

    try:
        user = Users(id=new_id,name=new_name,avatar_url=new_url,tweet_id=new_tweets)
        db.session.add(user)
        db.session.commit()
        users = Users.query.order_by(Users.id).all()
        print('users', users)
        user_obj = {}
        for user in users:
            user_obj[user.id] = {
                'id':user.id,
                'name':user.name,
                'url':user.avatar_url,
                'tweets':user.tweet_id
            }

        return jsonify(
            {
                "success" : True,
                "users": user_obj
            }
        )

    except:
        abort(422)


@app.route('/users/<user_id>', methods=['PATCH', 'GET'])
def update_user(user_id):
    if request.method == 'PATCH':
        body = request.get_json()
        print("body is:", body)
        try:
            user = Users.query.filter(Users.id==user_id).one_or_none()
            print("tweet is:", user.tweet_id)
            if user is None:
                abort(400)
            
            if "tweets" in body:
                for index in range(len(user.tweet_id)):
                    if user.tweet_id[index] == body.get("tweets"):
                        # print("present",body.get("tweets"))
                        value = user.tweet_id.pop(index)
                        print("value:", value)
                        # user.tweet_id.remove(value)
                        db.session.commit()
                    
                    return jsonify(
                        {
                            "success": True,
                            "likes": user.tweet_id
                        }
                    )

                else:
                    user.tweet_id.append(body.get("tweets"))
                    db.session.commit()
            
                    return jsonify(
                        {
                            "success": True,
                            "likes": user.tweet_id
                        }
                    )

        except:
            abort(404)

    if request.method == 'GET':
        try:
            user = Users.query.filter(Users.id==user_id).one_or_none()
            tweets = Tweets.query.filter(Tweets.author==user_id).all()
            print("tweet is:", user.tweet_id)
            if user is None:
                abort(400)

            tweet_list = []
            
            for tweet in tweets:
                tweet_obj = {
                    "id": tweet.id,
                    "text": tweet.text,
                    "author": tweet.author,
                    "timestamp": tweet.timestamp,
                    "likes": tweet.likes,
                    "replies": tweet.replies,
                    "replying_to": tweet.replying_to
                }
                tweet_list.append(tweet_obj)
            
            user_list = [{
                "id": user.id,
                "name": user.name,
                "avatar_url": user.avatar_url,
                "tweet_id": user.tweet_id,
                "tweets": tweet_list
            }]

            return jsonify({
                "success": True,
                "user" : user_list
            })
            
        
        except:
            abort(404)
        


@app.route('/tweets')
def tweets():
    tweets = Tweets.query.all()
    all_tweets = {}
    for tweet in tweets:
        all_tweets[tweet.id] = {
            'id': tweet.id,
            'text': tweet.text,
            'author': tweet.author,
            'timestamp': tweet.timestamp,
            'likes': tweet.likes,
            'replies': tweet.replies,
            'replying_to': tweet.replying_to
        }
    
    return jsonify({
        "success" : True,
        "tweets": all_tweets
    })

@app.route('/tweets/create', methods=['POST'])
def add_tweet():
    body = request.get_json()
    print("body is:", body)
    new_id = body.get("id", None)
    new_text = body.get("text", None)
    new_author = body.get("author", None)
    new_timestamp = body.get("timestamp", None)
    new_likes = body.get("likes", None)
    new_replies = body.get("replies", None)
    new_replying_to = body.get("replying_to", None)
    try:
        tweet = Tweets(id=new_id,text=new_text,author=new_author,timestamp=new_timestamp,likes=new_likes,replies=new_replies,replying_to=new_replying_to)
        db.session.add(tweet)
        db.session.commit()
        tweets = Tweets.query.order_by(Tweets.id).all()
        all_tweets = {}
        for tweet in tweets:
            all_tweets[tweet.id] = {
                'id': tweet.id,
                'text': tweet.text,
                'author': tweet.author,
                'timestamp': tweet.timestamp,
                'likes': tweet.likes,
                'replies': tweet.replies,
                'replying_to': tweet.replying_to
            }

        return jsonify({
        "success" : True,
        "tweets": all_tweets
        })
    
    except:
        abort(422)

@app.route('/tweets/<tweet_id>', methods=['PATCH', 'GET'])
def update_tweet(tweet_id):
    if request.method == 'PATCH':
        body = request.get_json()
        print("body is:", body)
        try:
            tweet = Tweets.query.filter(Tweets.id==tweet_id).one_or_none()
            print("tweet is:", tweet.likes)
            if tweet is None:
                abort(400)
            
            if "likes" in body:
                for index in range(len(tweet.likes)):
                    if tweet.likes[index] == body.get("likes"):
                        # print("present",body.get("tweets"))
                        value = tweet.likes.pop(index)
                        print("value:", value)
                        # user.tweet_id.remove(value)
                        db.session.commit()
                    
                        return jsonify(
                            {
                                "success": True,
                                "likes": tweet.likes
                            }
                        )
                
                else:
                    tweet.likes.append(body.get("likes"))
                    db.session.commit()
            

                    print("tweet is:", body.get("likes"))
                    print("likes are:", tweet.likes)
                    return jsonify(
                        {
                            "success": True,
                            "likes": tweet.likes
                        }
                    )
            
            if "replies" in body:
                for index in range(len(tweet.replies)):
                    if tweet.replies[index] == body.get("replies"):
                        # print("present",body.get("tweets"))
                        value = tweet.replies.pop(index)
                        print("value:", value)
                        # user.tweet_id.remove(value)
                        db.session.commit()
                    
                        return jsonify(
                            {
                                "success": True,
                                "replies": tweet.replies
                            }
                        )
                
                else:
                    tweet.replies.append(body.get("replies"))
                    db.session.commit()
            

                    print("tweet is:", body.get("replies"))
                    print("replies are:", tweet.replies)
                    return jsonify(
                        {
                            "success": True,
                            "replies": tweet.replies
                        }
                    )
            
            if "replying_to" in body:
                tweet.replying_to = body.get("replying_to")
                db.session.commit()

                return jsonify(
                        {
                            "success": True,
                            "replies": tweet.replying_to
                        }
                    )

        except:
            abort(404)

    if request.method == 'GET':
        try:
            tweets = Tweets.query.filter_by(id=tweet_id).all()
            tweet_list = []
            
            for tweet in tweets:
                tweet_obj = {
                    "id": tweet.id,
                    "text": tweet.text,
                    "author": tweet.author,
                    "timestamp": tweet.timestamp,
                    "likes": tweet.likes,
                    "replies": tweet.replies,
                    "replying_to": tweet.replying_to
                }
                tweet_list.append(tweet_obj)

            return jsonify(
                {
                    "success": True,
                    "tweets": tweet_list
                }
            )
        
        except:
            abort(404)





#always include this at the bottom of your code
if __name__ == '__main__':
   app.run(host="0.0.0.0", port=3000) 