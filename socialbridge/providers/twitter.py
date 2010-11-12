import re

import tweepy

from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from oauth_access.models import OAuthAssociation

from ..exceptions import BadCredentials
from .abstract import SocialProvider

class Twitter(SocialProvider):
    service_name = 'twitter'

    def __init__(self, anObject):
        self.auth = tweepy.OAuthHandler(settings.OAUTH_ACCESS_SETTINGS[self.service_name]['keys']['KEY'],
                                        settings.OAUTH_ACCESS_SETTINGS[self.service_name]['keys']['SECRET'])

        token, secret_token = self._get_access_tokens(anObject)

        self.auth.set_access_token(token, secret_token)
        self.api = tweepy.API(self.auth)

        if not self.api.verify_credentials():
            raise BadCredentials()

    def _get_access_tokens(self, anObject):
        content_type = ContentType.objects.get_for_model(anObject)

        assoc = OAuthAssociation.objects.get(service=self.service_name,
                                             content_type=content_type,
                                             object_id=anObject.pk)


        res = re.match("oauth_token_secret=(.+)&oauth_token=(.+)", assoc.token)

        return res.group(2), res.group(1)


    def post_message(self, message):
        try:
            self.api.update_status(message)
        except tweepy.TweepError, e:
            return False

        return True





