from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm, ProfileForm, UserUpdateForm
from blog.models import Post


def register(request):
    if 'POST' == request.method:
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Votre compte a été crée! Vous pouvez maintenant vous connecter')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'account/register.html', {'form': form})


@login_required(login_url='login')
def profile(request):
    user = request.user
    posts = Post.published.filter(author=user)
    return render(request, 'account/profile.html', {'posts': posts})


@login_required(login_url='login')
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your profile wass successsfully updated!')
            return redirect('profile')
        else:
            messages.error(request, f'Please correct the error below.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'account/update_profile.html', {'user_form': user_form, 'profile_form': profile_form})
