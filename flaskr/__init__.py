import sys
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from models import setup_db, Users, Tweets,Bookmarks,db

# Create and configure the app
# Include the first parameter: Here, __name__is the name of the current Python module.

def create_app(test_config=None):
    app = Flask(__name__)
    with app.app_context():
    # db = SQLAlchemy(app)
        setup_db(app)
        CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Headers", "GET, POST, PATCH, DELETE, OPTION")
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
        new_tweets = body.get("tweets", None)
        
        try:
            user = Users(id=new_id,name=new_name,avatar_url=new_url,tweet_id=new_tweets)
            db.session.add(user)
            db.session.commit()
            users = Users.query.order_by(Users.id).all()
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
            db.session.rollback()
            print(sys.exc_info())
            abort(422)

        finally:
            db.session.close()


    @app.route('/users/<user_id>', methods=['GET'])
    def get_user(user_id):
        try:
            user = Users.query.filter(Users.id==user_id).one_or_none()
            tweets = Tweets.query.filter(Tweets.author==user_id).all()

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
            print(sys.exc_info())
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
        new_id = body.get("id", None)
        new_text = body.get("text", None)
        new_author = body.get("author", None)
        new_timestamp = body.get("timestamp", None)
        new_likes = body.get("likes", None)
        new_replies = body.get("replies", None)
        new_replying_to = body.get("replying_to", None)
        try:
            tweet = Tweets(id=new_id,text=new_text,author=new_author,timestamp=new_timestamp,likes=new_likes,replies=new_replies,replying_to=new_replying_to)
            user = Users.query.filter(Users.id==new_author).one_or_none()
            db.session.add(tweet)
            user.tweet_id.append(new_id)
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
            db.session.rollback()
            print(sys.exc_info())
            abort(422)
        
        finally:
            db.session.close()


    @app.route('/tweets/<tweet_id>', methods=['PATCH', 'GET'])
    def update_tweet(tweet_id):
        if request.method == 'PATCH':
            body = request.get_json()
            try:
                tweet = Tweets.query.filter(Tweets.id==tweet_id).one_or_none()

                if tweet is None:
                    abort(400)

                if "likes" in body:
                    for index in range(len(tweet.likes)):
                        if tweet.likes[index] == body.get("likes"):
                            # print("present",body.get("tweets"))
                            value = tweet.likes.pop(index)
                            # user.tweet_id.remove(value)
                            db.session.commit()
                        
                            return jsonify(
                                {
                                    "success": True,
                                    "likes": tweet.likes,
                                    "likes_len":len(tweet.likes)
                                }
                            )
                    
                    else:
                        tweet.likes.append(body.get("likes"))
                        db.session.commit()
                
                        return jsonify(
                            {
                                "success": True,
                                "likes": tweet.likes,
                                "likes_len":len(tweet.likes)
                            }
                        )
                
                if "replies" in body:
                    for index in range(len(tweet.replies)):
                        if tweet.replies[index] == body.get("replies"):
                            # print("present",body.get("tweets"))
                            tweet.replies.pop(index)
                            # user.tweet_id.remove(value)
                            db.session.commit()
                        
                            return jsonify(
                                {
                                    "success": True,
                                    "replies": tweet.replies,
                                    "replies_len": len(tweet.replies)
                                }
                            )
                    
                    else:
                        tweet.replies.append(body.get("replies"))
                        db.session.commit()

                        return jsonify(
                            {
                                "success": True,
                                "replies": tweet.replies,
                                "replies_len": len(tweet.replies)
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
                db.session.rollback()
                print(sys.exc_info())
                abort(404)
            
            finally:
                db.session.close()

        if request.method == 'GET':
            try:
                tweet = Tweets.query.filter(Tweets.id==tweet_id).one_or_none()
            
                if tweets is not None: 
                    tweet_list = []  
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
                print(sys.exc_info())
                abort(404)


    @app.route('/bookmarks/<user_id>')
    def bookmarks(user_id):
        bookmarks = Bookmarks.query.filter(Bookmarks.author==user_id).all()
        all_bookmarks = {}
        for bookmark in bookmarks:
            all_bookmarks[bookmark.id] = {
                'id': bookmark.id,
                'text': bookmark.text,
                'author': bookmark.author,
                'timestamp': bookmark.timestamp,
                'likes': bookmark.likes,
                'replies': bookmark.replies,
                'replying_to': bookmark.replying_to
            }
        
        return jsonify({
            "success" : True,
            "tweets": all_bookmarks
        })

    @app.route('/bookmarks/create', methods=['POST'])
    def add_bookmark():
        body = request.get_json()
        bookmark_id = body.get("id", None)
        bookmark_text = body.get("text", None)
        bookmark_author = body.get("author", None)
        bookmark_timestamp = body.get("timestamp", None)
        bookmark_likes = body.get("likes", None)
        bookmark_replies = body.get("replies", None)
        bookmark_replying_to = body.get("replying_to", None)
        try:
            bookmark = Bookmarks(id=bookmark_id,text=bookmark_text,author=bookmark_author,timestamp=bookmark_timestamp,likes=bookmark_likes,replies=bookmark_replies,replying_to=bookmark_replying_to)
            db.session.add(bookmark)
            db.session.commit()
            bookmarks = Bookmarks.query.order_by(Bookmarks.id).all()
            all_bookmarks = {}
            for bookmark in bookmarks:
                all_bookmarks[bookmark.id] = {
                    'id': bookmark.id,
                    'text': bookmark.text,
                    'author': bookmark.author,
                    'timestamp': bookmark.timestamp,
                    'likes': bookmark.likes,
                    'replies': bookmark.replies,
                    'replying_to': bookmark.replying_to
                }

            return jsonify({
            "success" : True,
            "tweets": all_bookmarks
            })
        
        except:
            db.session.rollback()
            print(sys.exc_info())
            abort(422)
        
        finally:
            db.session.close()

    @app.route('/bookmarks/<bookmark_id>', methods=['GET', 'DELETE'])
    def update_bookmark(bookmark_id):
        if request.method == 'GET':
            try:
                bookmark = Bookmarks.query.filter(Bookmarks.id==bookmark_id).one_or_none()

                if bookmark is not None: 
                    bookmark_list = []          
                    tweet_obj = {
                        "id": bookmark.id,
                        "text": bookmark.text,
                        "author": bookmark.author,
                        "timestamp": bookmark.timestamp,
                        "likes": bookmark.likes,
                        "replies": bookmark.replies,
                        "replying_to": bookmark.replying_to
                    }
                    bookmark_list.append(tweet_obj)

                    return jsonify(
                        {
                            "success": True,
                            "tweets": bookmark_list
                        }
                    )

                else:
                    abort(400)
            
            except:
                print(sys.exc_info())
                abort(404)
        
        if request.method == 'DELETE':
            try:
                Bookmarks.query.filter(Bookmarks.id==bookmark_id).delete()
                db.session.commit()

                return jsonify({"success": True})
            except:
                db.session.rollback()
                print(sys.exc_info())
                abort(404)
            
            finally:
                db.session.close()

    @app.route('/bookmarks/search', methods=['POST'])
    def search_bookmarks():
        try:
            body = request.get_json()
            search_term = body.get('search_term')
            search = "%{}%".format(search_term.replace(" ", "\ "))
            
            search_results = Bookmarks.query.filter(Bookmarks.text.match(search)).all()
            
            bookmarks = []

            for result in search_results:
                bookmarks.append(
                   {
                    "id": result.id,
                    "text": result.text
                   }
                )

            return jsonify({
                'success': True,
                'bookmarks': bookmarks
            })

        except:
            db.session.rollback()
            print(sys.exc_info())
            abort(404)
            
        finally:
            db.session.close()

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 400, "message": "bad request"}), 
            400
        )

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}),
            405,
        )

    #always include this at the bottom of your code
    if __name__ == '__main__':
        app.run(host="0.0.0.0", port=3000) 

    return app