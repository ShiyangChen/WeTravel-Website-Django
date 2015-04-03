from django.shortcuts import render
from django.http import HttpResponse
from wetravel.form import UserForm, UserProfileForm

# Create your views here.

def index(request):
    return render(request, 'wetravel/index.html')

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
