from django import forms
# Kiểm tra username có ký tự đặt biệt không
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from phonenumber_field.formfields import PhoneNumberField
from .models import Profile

# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

# Thêm trường email vào form (sử dụng form của django)
# class UserRegisterForm(UserCreationForm):
#     email = forms.EmailField()

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']

# Sử dụng form tự tạo
class UserRegisterForm(forms.Form):

    # GENDER_CHOICES = [
    #     ('M', 'Male'),
    #     ('F', 'Female'),
    #     ('O', 'Other'),
    # ]

    username = forms.CharField(label='User Name', max_length=20)
    email = forms.EmailField(label='Email')
    # gender = forms.ChoiceField(label='Gender', choices=GENDER_CHOICES)
    #phone = PhoneNumberField(label='Phone number')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())

    # Hàm kiểm tra mật khẩu 2 có trùng với mật khẩu 1 hay không
    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']

            if password1 == password2 and password1:
                return password2
        raise forms.ValidationError('Your password incoress')

    # Hàm kiểm tra username có ký tự đặt biệt hay không
    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Your username illegal')
        # Kiểm tra username có tồn tại hay chưa
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('Your username is exist')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except ObjectDoesNotExist:
            return email
        raise forms.ValidationError('Your email is exist')

    # Hàm lưu vào database
    def save(self):
        User.objects.create_user(username=self.cleaned_data['username'], email=self.cleaned_data['email'], password=self.cleaned_data['password1'])

# Hàm update thông tin user
class UserUpdateForm(forms.ModelForm):
    # Biến cùng tên với các cột trong database
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

# Hàm update thông tin profile (avatar)
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'gender', 'image']
