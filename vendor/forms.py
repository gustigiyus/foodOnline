from django import forms
from .models import Vendor
from accounts.validators import allow_only_images_validator

class VendorForm(forms.ModelForm):
    # NOTE: ImageField didn't support custom validator *
    # NOTE: FileField support custom validator images/docs and anything file upload

    vendor_license = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license']