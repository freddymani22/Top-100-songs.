from django import forms
from .models import BillBoard
# from datetime import date

class MyForm(forms.Form):
    # date = forms.DateField()
    date = forms.DateField(input_formats=['%Y-%m-%d'],required=True, widget=forms.TextInput(attrs={'type': 'date'}))



    class Meta:
        model = BillBoard
        fields = ['date']
        # widgets = {
        #     'date': forms.DateInput(attrs={'type': 'date'}),
        # }



class SingerForm(forms.Form):
    artist = forms.CharField(label='Name', max_length=100)



    class Meta:
        model = BillBoard
        fields = ['artist']



class ArtistTopForm(forms.Form):
    artist_top = forms.CharField(label='Name', max_length=100)



  