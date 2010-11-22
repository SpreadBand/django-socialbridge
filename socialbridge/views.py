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
from .forms import SocialMessageForm, SocialBroadcastMessageForm

from .models import SERVICES

@login_required
def post_message(request, anObject, service):
    """
    Post a message on the given social network
    """
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



def broadcast_message(request, anObject):
    """
    Broadcast a message on many social networks
    """
    providers = {}
    for service_name, provider_class in SERVICES.iteritems():
        # Check if we have an association with this service
        try:
            providers[service_name] = provider_class(request, anObject)
        except NotAssociatedException, e:
            pass

    message_form = SocialBroadcastMessageForm(request.POST or None)

    if request.method == 'POST':
        if message_form.is_valid():
            # Get and post message
            message = message_form.cleaned_data.get('message')

            all_published = True
            for service_name, provider in providers.items():
                if message_form.cleaned_data.get('publish_on_%s' % service_name, False) is True:
                    published = provider.post_message(message)
                    all_published &= published
                    if not published:
                        messages.error(request,
                                       _("Your message couldn't be published on %s" % service_name)
                                       )
            
            if all_published:
                messages.success(request,
                                 _("Your message was successfully broadcasted")
                                 )
            else:
                messages.warning(request,
                                 _("Your message was partially published")
                                 )

            return redirect(anObject)

    context = {'available_services': SERVICES,
               'object': anObject,
               'message_form': message_form,
               'providers': providers}

    return render_to_response(template_name='socialbridge/broadcast_message.html',
                              context_instance=RequestContext(request, context)
                              )
    
