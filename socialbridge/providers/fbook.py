import re

import facebook

from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from oauth_access.models import OAuthAssociation

from ..exceptions import BadCredentials
from .abstract import SocialProvider

class Facebook(SocialProvider):
    service_name = 'facebook'

    def __init__(self, anObject):
        access_token = self._get_access_tokens(anObject)
        self._graph = facebook.GraphAPI(access_token)

    def _get_access_tokens(self, anObject):
        content_type = ContentType.objects.get_for_model(anObject)

        assoc = OAuthAssociation.objects.get(service=self.service_name,
                                             content_type=content_type,
                                             object_id=anObject.pk)
        return assoc.token

    def post_message(self, message):
        try:
            self._graph.put_object("me", "feed", message=message)
        except Exception, e:
            return False

        return True





