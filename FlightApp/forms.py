from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['full_name', 'email', 'mobile_number', 'seats', 'journey_date',
                  'seat_class', 'passenger_names', 'passenger_ages']
        widgets = {
            'journey_date': forms.DateInput(attrs={'type': 'date'}),
            'seat_class': forms.Select(),
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'full_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        full_name = self.cleaned_data['full_name']
        user.first_name = full_name  # Optional: You can split and store last_name
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user