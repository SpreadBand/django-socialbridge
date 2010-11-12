from django import forms
from django.utils.translation import ugettext as _

class SocialMessageForm(forms.Form):
    message = forms.CharField(label=_('message'),
                              widget=forms.Textarea)
