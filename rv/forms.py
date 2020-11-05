from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *
from django.contrib.auth import authenticate, login
import datetime

from ze.shit import *

from django.contrib import messages
from my_users.models import *

from django.utils.translation import gettext_lazy as _


class form_validationn(forms.Form):


    def clean_doc_name(self):
        name = self.cleaned_data["doc_name"]
        try:
            n = doctor.objects.get(username=name)
            msg = f'doctor {name} was found'
            from_me_to_me(msg=msg)
        except doctor.DoesNotExist:
            msg = 'doctor u looking for is not here'
            from_me_to_me(msg=msg)
            raise forms.ValidationError(msg)
        return name


class rv_form_dt(forms.ModelForm, form_validationn):

    year = forms.CharField(label='year', widget=forms.TextInput(attrs={'class':'input is-medium is-black', 'placeholder':'year'}))
    month = forms.CharField(label='month', widget=forms.TextInput(attrs={'class':'input is-medium is-black', 'placeholder':'month'}))
    day = forms.CharField(label='day', widget=forms.TextInput(attrs={'class':'input is-medium is-black', 'placeholder':'day'}))
    hour = forms.CharField(label='hour', widget=forms.TextInput(attrs={'class':'input is-medium is-black', 'placeholder':'hour'}))




    class Meta:
        model = rv
        fields = ['doc_name','name', 'phone_num', 'cmnt'
                  #'year', 'mounth', 'day', 'hour',

                 ]
        widgets = {
                   'name': forms.TextInput(attrs={'class':'input is-black is-medium', 'placeholder':'name'}),
                   'doc_name': forms.TextInput(attrs={'class':'input is-black is-medium', 'placeholder':'doc name'}),
                   'phone_num': forms.TextInput(attrs={'class':'input is-black is-medium', 'placeholder':'phone'}),
                   'cmnt': forms.Textarea(attrs={'class':'textarea is-black is-medium', 'placeholder':'comment', 'rows' :'1'}),

                   #'year': forms.TextInput(attrs={'class':'input is-primary is-medium', 'placeholder':'genre_visite'}),
                   #'month': forms.TextInput(attrs={'class':'input is-primary is-medium', 'placeholder':'montant a payer'}),
                   #'day': forms.TextInput(attrs={'class':'input is-primary is-medium', 'placeholder':'montant paye'}),
                   #'hour': forms.TextInput(attrs={'class':'textarea is-primary is-medium', 'placeholder':'commentaire'}),
        }

class rv_form_tmrw(forms.ModelForm, form_validationn):


    class Meta:
        model = rv
        fields = ['doc_name','name', 'phone_num', 'cmnt'
                  #'year', 'mounth', 'day', 'hour',

                ]
        widgets = {
                   'name': forms.TextInput(attrs={'class':'input is-black is-medium', 'placeholder':'name'}),
                   'doc_name': forms.TextInput(attrs={'class':'input is-black is-medium', 'placeholder':'doc name'}),
                   'phone_num': forms.TextInput(attrs={'class':'input is-black is-medium', 'placeholder':'phone'}),
                   'cmnt': forms.Textarea(attrs={'class':'textarea is-black is-medium', 'placeholder':'comment', 'rows' :'1'}),

                   #'year': forms.TextInput(attrs={'class':'input is-primary is-medium', 'placeholder':'genre_visite'}),
                   #'month': forms.TextInput(attrs={'class':'input is-primary is-medium', 'placeholder':'montant a payer'}),
                   #'day': forms.TextInput(attrs={'class':'input is-primary is-medium', 'placeholder':'montant paye'}),
                   #'hour': forms.TextInput(attrs={'class':'textarea is-primary is-medium', 'placeholder':'commentaire'}),
        }
