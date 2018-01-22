from django import forms
from django.forms import ModelForm
from .models import Jpider_response
class UrlForm(forms.Form):
    """
    Url : 网页端传入的Url
    """        
    url = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'URL'}))      
    request_way = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Post/Get'}))
    referer = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Referer'}))
    data = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'data'}))
    cookies = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'cookies'}))


class XpathForm(forms.Form):
    infos = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))         # 核心字段
    info = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    info_zero = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    info_one = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))      # 核心字段的遍历
    info_two = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    info_three = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    info_four = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    info_five = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    info_six = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    info_seven = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    info_eight = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    info_nine = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
