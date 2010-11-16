import re

import facebook

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

from oauth_access.models import OAuthAssociation

from ..exceptions import BadCredentials, NotAssociatedException
from .abstract import SocialProvider

class Facebook(SocialProvider):
    service_name = 'facebook'

    def __init__(self, request, anObject):
        self.request = request
        self.object = anObject

        access_token = self._get_access_tokens(anObject)
        self._graph = facebook.GraphAPI(access_token)

    def _get_access_tokens(self, anObject):
        content_type = ContentType.objects.get_for_model(anObject)

        try:
            assoc = OAuthAssociation.objects.get(service=self.service_name,
                                                 content_type=content_type,
                                                 object_id=anObject.pk)
        except OAuthAssociation.DoesNotExist:
            # Redirect to association page if none exist
            association_url = reverse('oauth_access_login', args=[self.service_name])
            raise NotAssociatedException(next_url=association_url + "?next=%s" % self.request.path)

        return assoc.token

    def post_message(self, message):
        try:
            self._graph.put_object("me", "feed", message=message)
        except Exception, e:
            return False

        return True





