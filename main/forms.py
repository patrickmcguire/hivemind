from django import forms


class ZeitgeistForm(forms.Form):
    term1 = forms.CharField()
    term2 = forms.CharField()
    term3 = forms.CharField()
    term4 = forms.CharField()
