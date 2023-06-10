from django import forms
from .models import Category


class CategoryForm(forms.ModelForm):
    category_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    class Meta:
        model = Category
        fields = ['category_name', 'description']