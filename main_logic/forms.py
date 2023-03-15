from django import forms


class UploadFileForm(forms.Form):
    catagory = forms.CharField()
    file = forms.FileField()
