from django import forms

class MyForm(forms.Form):
    text = forms.IntegerField(label='')
