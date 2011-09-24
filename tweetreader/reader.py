import tweetstream
import settings
from datetime import datetime
import simplejson as json

from django.contrib.auth.models import User
from django.db import transaction

from tweetreader.models import Tweeter, Tweet

DATETIME_STRING_FORMAT = '%a %b %d %H:%M:%S +0000 %Y'

words=['$GOOG', '$AAPL', '$MSFT', '$AMZN']


def monitor_tweetstream():
    try:
        stream = tweetstream.FilterStream(settings.TWITTER_USER, settings.TWITTER_PASSWORD, track=words)
        for tweet in stream:
            
            print str(tweet['id']) + ' : ' + str(tweet['user']['screen_name']) + ' : ' + str(tweet['text'])
            print json.dumps(tweet, sort_keys=True, indent=4)
            insert_tweet_to_db(tweet)
    
    except tweetstream.ConnectionError, e:
        print "Disconnected from twitter. Reason:", e.reason

@transaction.commit_on_success
def insert_tweet_to_db(tweet):
    
    tweet_author, created = Tweeter.objects.get_or_create(user_id=tweet['user']['id'],
                                                          screen_name=tweet['user']['screen_name']
                                                          )
    if created is True:
        tweet_author.profile_image_url = tweet['user']['profile_image_url']
        
        registered_users = User.objects.filter(username=tweet['user']['screen_name'])
        if len(registered_users) == 1:
            tweet_author.registered_user = registered_users[0]
        
        tweet_author.save()
    
    print tweet_author.screen_name
    
    new_tweet, created = Tweet.objects.get_or_create(
                                    tweet_id=tweet['id'],
                                    author=tweet_author,
                                    created_at=datetime.strptime(tweet['created_at'], DATETIME_STRING_FORMAT),
                                    text = tweet['text']
                                    )
    
    if created is True:
        new_tweet.save()
    else:
        print "DUPE!"
        print json.dumps(tweet, sort_keys=True, indent=4)
        # We want to log these tweets to find out why we are getting the same ID twice
        
    return new_tweet