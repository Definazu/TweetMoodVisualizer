from models import Tweet
# from database import Session

class TweetRepository:
    def __init__(self, session):
        self.session = session
    
    def add_tweet(self, tweet_data: dict):
        try:
            tweet = Tweet(**tweet_data)
            self.session.add(tweet)
        except Exception as e:
            self.session.rollback()
            raise
    
    def commit(self):
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise
