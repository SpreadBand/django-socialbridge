import tweepy

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_POST
from django.utils.translation import ugettext as _

from band.models import Band

from .exceptions import NotAssociatedException
from .providers.twitter import Twitter
from .providers.fbook import Facebook
from .forms import SocialMessageForm

SERVICES = {'twitter': Twitter,
            'facebook': Facebook}

@login_required
def post_message(request, anObject, service):
    # Check if we know this service
    try:
        provider_class = SERVICES[service]
    except KeyError:
        return HttpResponseNotFound()

    # Check if we have an association with this service
    try:
        provider = provider_class(request, anObject)
    except NotAssociatedException, e:
        provider = None

    message_form = SocialMessageForm(request.POST or None)

    if request.method == 'POST':
        if message_form.is_valid():
            # Get and post message
            message = message_form.cleaned_data.get('message')
    
            provider.post_message(message)
            
            messages.success(request,
                             _("Your message was successfully posted to %s" % service)
                             )

            return redirect(anObject)

    context = {'service': service,
               'object': anObject,
               'message_form': message_form,
               'provider': provider}

    return render_to_response(template_name='socialbridge/post_message.html',
                              context_instance=RequestContext(request, context)
                              )




