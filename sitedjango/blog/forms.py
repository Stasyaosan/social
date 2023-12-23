from django import forms
from .models import *

c = []

cats = Category.objects.all()
for cat in cats:
    c.append((cat.id, cat.title))

class ContactForm(forms.Form):
    name = forms.CharField(min_length=5, widget=forms.TextInput(attrs={'name':'name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'name': 'email'}))
    message = forms.CharField(min_length=20, widget=forms.Textarea(attrs={'name': 'message', 'cols': 30, 'rows': 9}))


class AddArticle(forms.Form):
    title = forms.CharField(min_length=5, widget=forms.TextInput(attrs={'name':'title'}))
    description = forms.EmailField(widget=forms.TextInput(attrs={'name': 'description'}))
    fulltext = forms.CharField(min_length=20, widget=forms.Textarea(attrs={'name': 'fulltext', 'cols': 30, 'rows': 9}))
    img = forms.ImageField(widget=forms.FileInput(attrs={'name': 'img'}))
    cat = forms.ChoiceField(choices=c)

class SearchForm(forms.Form):
    query = forms.CharField(label='Поиск', max_length=100)

class Page(forms.Form):
    class Meta:
        model = MyPage
        fields = ['text', 'image', 'vidio']