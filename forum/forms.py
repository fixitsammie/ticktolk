from django import forms
from .models import Thread,Category,Post

from PIL import Image

class AddThreadForm(forms.ModelForm):
    main_post=forms.CharField(widget=forms.Textarea)
   


    class Meta:
        model=Thread
        fields = ['topic', 'main_post','image']

class DocumentForm(forms.Form):
    docfile=forms.FileField(
        label='Select a file my guy')

class QuoteThreadForm(forms.ModelForm):
    quote=forms.CharField(label='quote', max_length=500)
    def clean(self):
        super(QuoteThreadForm, self).clean()
        cleaned_data = self.cleaned_data
        return cleaned_data
    class Meta:
        model=Post
        fields=['quote']

class EditThreadForm(forms.ModelForm):
    def clean(self):
        super(EditThreadForm, self).clean()
        cleaned_data = self.cleaned_data
        return cleaned_data


    class Meta:
        model=Thread
        fields = ['topic', 'main_post']




class AddCategoryForm(forms.ModelForm):


    class Meta:
        model=Category
        fields = ['name', 'description']

class AddPostForm(forms.ModelForm):
    post=forms.CharField(widget=forms.Textarea)
    class Meta:
        model=Post
        fields=['post']

class SearchForm(forms.Form):
    q=forms.CharField()
