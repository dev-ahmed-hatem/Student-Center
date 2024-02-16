from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class UserRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ["name", 'username', "phone", "password1", "password2"]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            self.add_error("username", f"Username {username} exists")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password1"))

        user.save()
        UserProfile.objects.create(
            name=self.cleaned_data.get("name"),
            user=user,
            phone=self.cleaned_data.get("phone"))
        return user
