import tweepy

from django.conf import settings
from django.http import HttpResponseNotFound

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from band.models import Band

from .providers.twitter import Twitter
from .providers.fbook import Facebook

SERVICES = {'twitter': Twitter,
            'facebook': Facebook}

@login_required
def post_message(request, service, anObject, message):
    try:
        provider_class = SERVICES[service]
    except KeyError:
        return HttpResponseNotFound()
    
    provider = provider_class(anObject)
    provider.post_message(message)


