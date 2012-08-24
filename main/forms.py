from django import forms

class ZeitgeistForm(forms.Form):
    term1 = forms.CharField()
    term2 = forms.CharField()
