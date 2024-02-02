from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from .forms import ProfilePicture, SignUpForm, UserProfileChange

# Create your views here.

def sign_up(request):
    form = SignUpForm()
    registered = False
    if request.method == 'POST':
        form = SignUpForm(data = request.POST)
        if form.is_valid():
            form.save()
            registered = True
    context = {'form':form,'registered':registered}
    return render(request, 'account/signup.html',context=context)

def sign_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
    context = {'form':form}
    return render(request, 'account/signin.html',context=context)

@login_required
def sign_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def user_profile(request):
    return render(request, 'account/profile.html')

@login_required
def update_profile(request):
    current_user = request.user
    form = UserProfileChange(instance = current_user)
    if request.method == 'POST':
        form = UserProfileChange(request.POST, instance = current_user)
        if form.is_valid():
            form.save()
            form = UserProfileChange(instance = current_user)
    return render(request, 'account/update_profile.html', context={'form':form})

@login_required
def pass_change(request):
    current_user = request.user
    changed = False
    form = PasswordChangeForm(current_user)
    if request.method == 'POST':
        form = PasswordChangeForm(current_user , data = request.POST)
        if form.is_valid():
            form.save()
            changed = True
    return render(request, 'account/pass_change.html', context={'form':form, 'changed':changed})


@login_required
def update_profile_picture(request):
    form = ProfilePicture(instance=request.user.userprofile)
    if request.method == 'POST':
        form = ProfilePicture(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('profile'))
    return render(request, 'account/profile_pic.html', context={'form':form})