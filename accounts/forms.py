from django import forms

class LoginFOrm(forms.Form):
    email=forms.EmailField(max_length=50)
    password=forms.CharField(max_length=30)

