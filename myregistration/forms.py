from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from django.contrib.auth.models import User
from django import forms

from django.core.exceptions import ValidationError
from django.utils.html import strip_tags

class RegistrationForm(UserCreationForm):
    username = forms.RegexField(regex=r'^[\w.@+-]+$',
                                max_length=30,
                                label=(u'Username'),
                                error_messages={'invalid':
                                    ('This value may contain only letters, numbers and @/./+/-/_ characters.'),})
    
    email=forms.EmailField(label=(u'Email Address'))
    password1=forms.CharField(min_length=8,label=(u'Password'),widget=forms.PasswordInput(render_value=False))
    password2=forms.CharField(min_length=8,label=(u'Verify Password'),widget=forms.PasswordInput(render_value=False))
    
    """	
    def is_valid(self):
        form = super(RegistrationForm, self).is_valid()
        for f, error in self.errors.iteritems():
            if f != '__all_':
                self.fields[f].widget.attrs.update({'class': 'error', 'value': strip_tags(error)})
        return form
    """
    
    def clean_password(self):
        password1=self.cleaned_data['password1']
        password2=self.cleaned_data['password2']
        
        if password1!=password2:
            raise forms.ValidationError('The passwords did not match. Please try again.')
        return password1
    
    def clean_email(self):
        email=self.cleaned_data['email']
        if User.objects.filter(email__iexact=email):
            raise forms.ValidationError("The email address '%s' is already in use. Please supply a different email address."%email)
        return email


    def clean_username(self):
        username=self.cleaned_data['username']
        if User.objects.filter(username__iexact=username):
            raise forms.ValidationError("A user with the username '%s' already exists."%username)
        else:
            return username
    class Meta:
        fields = [ 'username', 'email', 'password1',
                  'password2']
        model = User



class LoginForm(forms.Form):
    username=forms.CharField(label=(u'Username'))
    password=forms.CharField(label=(u'Password'),widget=forms.PasswordInput(render_value=False))
    
    
    def clean_username(self):
        query=self.cleaned_data['username']
        if User.objects.filter(username__iexact=query):
            username=query
            return username
        elif User.objects.filter(email__iexact=query):
            username=User.objects.get(email=query)
            return username
            
        else:
            raise forms.ValidationError("There is no user with the username '%s' you can register a new account with it"% query) 



   
