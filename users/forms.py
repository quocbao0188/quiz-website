from django import forms
# Kiểm tra username có ký tự đặt biệt không
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from phonenumber_field.formfields import PhoneNumberField
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'id':'email'}))

    class Meta:
        model = User
        fields = ['username', 'email','first_name', 'last_name', 'password1', 'password2']

# class UserRegisterForm(forms.Form):
#     username = forms.CharField(label='User Name', max_length=20, help_text='Sort text to login easily')
#     email = forms.EmailField(label='Email')
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput(), help_text='Password must be 8 characters or more and contain at least one letter and at least one digit or punctuation character')
#     password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())

#     def clean_password1(self):
#         password1 = self.cleaned_data['password1']
#         if len(password1) < 8:
#             raise forms.ValidationError('Password too short')
#         # At least one letter and one non-letter
#         first_isalpha = password1[0].isalpha()
#         if all(c.isalpha() == first_isalpha for c in password1):
#             raise forms.ValidationError("The new password must contain at least one letter and at least one digit or" \
#                                         " punctuation character.")
#         return password1

#     def clean_password2(self):
#         if 'password1' in self.cleaned_data:
#             password1 = self.cleaned_data['password1']
#             password2 = self.cleaned_data['password2']

#             if password1 == password2 and password1:
#                 return password2
#         raise forms.ValidationError('Your password incorrect')

#     def clean_username(self):
#         username = self.cleaned_data['username']
#         if not re.search(r'^\w+$', username):
#             raise forms.ValidationError('Your username illegal')
#         try:
#             User.objects.get(username=username)
#         except ObjectDoesNotExist:
#             return username
#         raise forms.ValidationError('Your username is exist')

#     def clean_email(self):
#         email = self.cleaned_data['email']
#         try:
#             User.objects.get(email=email)
#         except ObjectDoesNotExist:
#             return email
#         raise forms.ValidationError('Your email is exist')

#     def save(self):
#         User.objects.create_user(username=self.cleaned_data['username'], email=self.cleaned_data['email'], password=self.cleaned_data['password1'])
#         # User.objects.db_manager('postgresql').create_user(username=self.cleaned_data['username'], email=self.cleaned_data['email'], password=self.cleaned_data['password1'])

class ProfileRegisterForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['student_id', 'phone', 'gender', 'birthday', 'faculty']
        labels = {
        "student_id": "Student ID",
        }
        help_texts = {
            'student_id': 'For example: 1711061***',
            'phone': 'For example: +84 0981029***',
            'faculty': 'For example: Information Technology'
        }
        widgets = {
            'gender': forms.RadioSelect,
            'birthday': forms.DateInput(attrs={'class':'datepicker'}),
        }

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=Profile.GENDER_CHOICES, widget=forms.RadioSelect(attrs={'class': 'radioset'}))
    # birthday = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker'}), input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        model = Profile
        fields = ['student_id','phone', 'gender', 'birthday', 'faculty', 'image']
        labels = {
        "student_id": "Student ID",
        }
        help_texts = {
            'student_id': 'For example: 1711061***',
            'phone': 'For example: +84 0981029***',
            'faculty': 'For example: Information Technology'
        }
        widgets = {
            'birthday': forms.DateInput(attrs={'class':'datepicker'}),
        }
