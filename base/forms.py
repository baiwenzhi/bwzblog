# coding=utf-8
from django import forms

__author__ = 'xiaoj'

class PhotoForm(forms.Form):
    photo=forms.FileField(required=True,error_messages={'required':'请选择图片'})