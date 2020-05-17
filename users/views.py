from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ProfileRegisterForm
from django.contrib.auth.decorators import login_required
import requests
from django.conf import settings

# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, f'Account created for {username}!')
#             return redirect('home')
#     else:
#         form = UserRegisterForm()
#     content = {
#         'title': 'Register',
#         'form': form
#     }
#     return render(request, 'users/register.html', content)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        profile_form = ProfileRegisterForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            ''' End reCAPTCHA validation '''
            if result['success']:
                new_user = form.save()
                profiles = profile_form.save(commit=False)
                profiles.user = new_user
                profiles.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Your account { username } has been create ! You are now able to login')
            else:
                messages.success(request, f'Invalid reCAPTCHA. Please try again.')
                
            return redirect('login')
    else:
        form = UserRegisterForm()
        profile_form = ProfileRegisterForm()

    content = {
        'title': 'Register',
        'form': form,
        'profile_form': profile_form
    }
    return render(request, 'users/register.html', content)

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            username = u_form.cleaned_data.get('username')
            messages.success(request, f'Your account { username } has been updated !')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)
