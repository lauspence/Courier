from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Job,Customer,CourierProfile

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['item_type', 'pickup_lat', 'pickup_lng', 'delivery_lat', 'delivery_lng']
        widgets = {
            'item_type': forms.Select(attrs={'class': 'form-control'}),
            'pickup_lat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Pickup Latitude'}),
            'pickup_lng': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Pickup Longitude'}),
            'pickup_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pickup Address'}),
            'delivery_lat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Delivery Latitude'}),
            'delivery_lng': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Delivery Longitude'}),
            'delivery_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Delivery Address'}),

        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone', 'address']  # You can add more fields here if necessary
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your address'}),
        }

class CourierProfileForm(forms.ModelForm):
    class Meta:
        model = CourierProfile
        fields = ['phone', 'address', 'vehicle_type', 'profile_picture']  # Removed license_number and added profile_picture
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your address'}),
            'vehicle_type': forms.Select(attrs={'class': 'form-control'}),  # Assuming vehicle_type is a choice field in the model
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),  # Added profile picture field
        }


class CourierRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15)  # Assuming a phone field
    # You can add more fields as needed

    class Meta:
        model = User  # Or use a custom model if you have one
        fields = ['username', 'email', 'phone', 'password1', 'password2']
