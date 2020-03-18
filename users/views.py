from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
# Create your views here.

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
        if form.is_valid(): #is_valid phải viết hàm clean_name-method thì nó mới hiểu
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account { username } has been create ! You are now able to login')
            return redirect('login')
    else:
        form = UserRegisterForm()
    content = {
        'title': 'Register',
        'form': form
    }
    return render(request, 'users/register.html', content)

#Khi đã đăng xuất, sẽ không thể vào lại trang profile
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST ,instance=request.user)
        p_form = ProfileUpdateForm(request.POST , request.FILES,instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid(): #is_valid phải viết hàm clean_name-method thì nó mới hiểu
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
