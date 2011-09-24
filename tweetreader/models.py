from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

class Tweeter(models.Model):
    screen_name = models.CharField(null=False, blank=False, unique=True, max_length=20)
    user_id = models.IntegerField(null=False, blank=False, unique=True)
    profile_image_url = models.URLField(verify_exists=False)
    registered_user = models.ForeignKey(User, null=True, blank=True, to_field='username')
    
    def __unicode__(self):
        return str(self.screen_name)
        
admin.site.register(Tweeter)

class Tweet(models.Model):
    tweet_id = models.IntegerField(null=False, blank=False, unique=True)
    created_at = models.DateTimeField(null=False, blank=False)
    author = models.ForeignKey(Tweeter, to_field='screen_name')
    text = models.CharField(null=False, blank=False, max_length=140)
    
    def __unicode__(self):
        return str(self.tweet_id)  + ' : ' + str(self.text)

admin.site.register(Tweet)