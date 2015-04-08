from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from wetravel.form import UserForm, UserProfileForm
from wetravel.models import *

# Create your views here.

def index(request):
    return render(request, 'wetravel/index.html')

def about(request):
    return render(request, 'wetravel/about.html')

def signup(request):
    signed_up = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            signed_up = True

        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
            'wetravel/signup.html',
            {'user_form': user_form, 'profile_form': profile_form, 'signed_up': signed_up})

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/wetravel/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'wetravel/login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/wetravel/')

def send_friend_request(request):
    if request.method == 'POST':
        target_username = request.POST.get('username')
        try:
            target_user = User.objects.get(username=target_username)
        except User.DoesNotExist:
            print "User {0} does not exist".format(target_username)
            return HttpResponse("User not found.")
        target_user.userprofile.requests.add(request.user.userprofile)
        return HttpResponseRedirect('/wetravel/')
    else:
        return HttpResponseRedirect('/wetravel/friends/')

def friends(request):
    return render(request, 'wetravel/friends.html', {})

def requests(request):
    return render(request, 'wetravel/requests.html', {})

def add_place(request):
    return render(request, 'wetravel/addplace.html', {})

def show_profile(request):
    posts = Post.objects.filter(publisher=request.user.userprofile)
    return render(request, 'wetravel/profile.html', {'posts': posts})
