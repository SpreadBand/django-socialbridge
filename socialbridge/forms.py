from django import forms
from django.utils.translation import ugettext as _

from .models import SERVICES

class SocialMessageForm(forms.Form):
    message = forms.CharField(label=_('message'),
                              widget=forms.Textarea)

class SocialBroadcastMessageForm(SocialMessageForm):
    def __init__(self, *args, **kwargs):
        SocialMessageForm.__init__(self, *args, **kwargs)

        for service in SERVICES.keys():
            self.fields["publish_on_%s" % service.lower()] = forms.BooleanField(label=service,
                                                                                required=False)
        
    @property
    def services(self):
        for service in SERVICES.keys():
            yield service, self["publish_on_%s" % service.lower()]

    def clean(self):
        at_least_one_service = False
        for service in self.services:
            publish = (self.cleaned_data.get("publish_on_%s" % service[0]) == True)
            at_least_one_service |= publish

        if not at_least_one_service:
            raise forms.ValidationError(_("You must select at least one service"))

        return self.cleaned_data
