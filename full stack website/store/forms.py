from django import forms
from django.contrib.auth.models import User
from .models import Order

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Create password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Confirm password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email address'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last name'}),
        }

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return confirm_password

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Password'}))

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'address', 'city', 'postal_code', 'country', 'payment_method']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'John Doe'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'john@example.com'}),
            'address': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '123 Tech Street, Suite 100'}),
            'city': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'San Francisco'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '94107'}),
            'country': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'United States'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('Credit Card', 'Credit / Debit Card'),
                ('PayPal', 'PayPal Instant'),
                ('Apple Pay', 'Apple Pay'),
            ]),
        }
