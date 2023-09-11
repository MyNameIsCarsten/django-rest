from django import forms

class TodoForm(forms.Form):
    task = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Enter your task'}))