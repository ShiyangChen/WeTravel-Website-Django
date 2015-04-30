from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from wetravel.form import *
from wetravel.models import *
from PIL import Image as PImage
from django.core.files.uploadedfile import SimpleUploadedFile

import json

# Create your views here.

def index(request):
    if request.user.is_authenticated():
        #user=request.user

        #recommendation part
        candidates1 = friends_goto_same_place(request.user)
        candidates2 = friends_been_there_before(request.user)
        candidates3 = recommend_new_friend(request.user)

        #posts part
        posts=Post.objects.order_by("-id")
        invi_posts=posts.filter(is_visible=True)
        posts_list=list(posts)
        for invi_post in invi_posts:

            for invi_friend in invi_post.restricted_members.all():
                if invi_friend.user.username==request.user.username:
                    posts_list.remove(invi_post)
                else:
                    continue

        context_dict = {'candidates1' : candidates1, 'candidates2' : candidates2, 'candidates3' : candidates3, 'posts':posts_list}

    else:
        context_dict = {}
    return render(request, 'wetravel/index.html', context_dict)



# recommend friends who share the same travelling wish:
def friends_goto_same_place(user):
    candidates = []
    if user.userprofile:
        for friend in user.userprofile.friends.all():
            if friend and friend.to_visit and user.userprofile.to_visit:
                if friend.to_visit.region == user.userprofile.to_visit.region:
                    candidates.append(friend)
    return tuple(candidates)[:3]

# recommend friends who have been to the place you want to go:
def friends_been_there_before(user):
    candidates = []
    if user.userprofile:
        for friend in user.userprofile.friends.all():
            if friend.visited:
                for visited_place in friend.visited.all():
                    if user.userprofile.to_visit and visited_place.region == user.userprofile.to_visit.region:
                        candidates.append(friend)
                        break
    return tuple(candidates)[:3]

# recommend new friends for you:
def recommend_new_friend(user):
    candidates = []
    if user.userprofile:
        for friend in user.userprofile.friends.all():
            if friend:
                for slfriend in friend.friends.all():
                    if slfriend and slfriend not in candidates and slfriend != user.userprofile:
                        for visited_place in slfriend.visited.all():
                            if user.userprofile.to_visit and visited_place.region == user.userprofile.to_visit.region:
                                candidates.append(slfriend)
                                break
                        if slfriend not in candidates:
                            if slfriend.to_visit:
                                if user.userprofile.to_visit and slfriend.to_visit.region == user.userprofile.to_visit.region:
                                    candidates.append(slfriend)
    return tuple(candidates)[:3]


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

@login_required
def settings(request):
    return render(request, 'wetravel/settings.html')



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


def create_post(request):
    return render(request, 'wetravel/create_post.html')

@login_required
def createpost(request):
    if 'text_message'in request.GET:
        text_message=request.GET['text_message']
        cur_user=request.user.userprofile

        #login_user=UserProfile.objects.get(user=cur_user)
    
        b=Post(text=text_message,publisher=cur_user)#login_user)
        b.save()
        return HttpResponseRedirect('/wetravel/')
        #posts=Post.objects.order_by("-id")
        #return render(request,'wetravel/index.html',{'posts':posts})
        
    else:
        return HttpResponse('submitted a empty form')

@login_required
def profile(request):
    user=request.user   #???
    cur_user=request.user.userprofile
    my_posts=Post.objects.filter(publisher=cur_user)
    my_posts=my_posts.order_by("-id")
    return render(request,'wetravel/profile.html',{'my_posts':my_posts,'user':user})

@login_required
def delete_confirm(request,param1):
    cur_user=request.user.userprofile
    my_posts=Post.objects.filter(publisher=cur_user)
    my_posts=my_posts.order_by("-id")
    return render(request,'wetravel/delete_confirm.html',{'param':param1, 'my_posts':my_posts})




@login_required
def delete(request,param1):
    cur_user=request.user.userprofile
    my_posts=Post.objects.filter(publisher=cur_user)
    my_posts=my_posts.order_by("-id")
    del_post=my_posts.get(id=param1)
    del_post.delete()
    return HttpResponseRedirect('/wetravel/profile/')
    #my_posts=Post.objects.filter(publisher=cur_user)
    #my_posts=my_posts.order_by("-id")
    #return render(request,'wetravel/profile.html',{'my_posts':my_posts})
  
@login_required
def privacy_choose(request,param1):
    cur_user=request.user.userprofile
    my_posts=Post.objects.filter(publisher=cur_user)
    set_post=my_posts.get(id=param1)
    my_friends=cur_user.friends.all()
    namelists=[]
    for friend in my_friends:
        namelists.append(friend.user.username)

    return render(request,'wetravel/privacy_choose.html',{'namelists':namelists,'set_post':set_post})

@login_required
def privacy(request,param1):
    user=request.user
    exc_inc=request.POST.get('ex_in')

    set_friends_username=request.POST.getlist("set_friends")
    cur_user=request.user.userprofile
    my_posts=Post.objects.filter(publisher=cur_user)
    set_post=my_posts.get(id=param1)
    my_friends=cur_user.friends.all()
    if exc_inc=="exclude":
        
        for friend_username in set_friends_username:
            for friend in my_friends:
                if friend.user.username == friend_username :
                    set_post.restricted_members.add(friend)
                    set_post.is_visible=True
                    set_post.save()
                else:
                    continue
    else:
        restricted_members=my_friends
        restrict_list=list(restricted_members)
        for friend in my_friends:
            for friend_username in set_friends_username:
                if friend.user.username == friend_username :
                    restrict_list.remove(friend)
                else:
                    continue;
        for restrict_friend in restrict_list:

            set_post.restricted_members.add(restrict_friend)
            set_post.is_visible=True
            set_post.save()
    return HttpResponseRedirect('/wetravel/profile/')

def resize_and_crop(img_path, size, crop_type='middle'):
    """
    Resize and crop an image to fit the specified size.

    args:
    img_path: path for the image to resize.
    modified_path: path to store the modified image.
    size: `(width, height)` tuple.
    crop_type: can be 'top', 'middle' or 'bottom', depending on this
    value, the image will cropped getting the 'top/left', 'middle' or
    'bottom/right' of the image to fit the size.
    raises:
    Exception: if can not open the file in img_path of there is problems
    to save the image.
    ValueError: if an invalid `crop_type` is provided.
    """
    # If height is higher we resize vertically, if not we resize horizontally
    img = PImage.open(img_path)
    # Get current and desired ratio for the images
    img_ratio = img.size[0] / float(img.size[1])
    ratio = size[0] / float(size[1])
    #The image is scaled/cropped vertically or horizontally depending on the ratio
    if ratio > img_ratio:
        img = img.resize((size[0], int(round(size[0] * img.size[1] / img.size[0]))),
            PImage.ANTIALIAS)
        # Crop in the top, middle or bottom
        if crop_type == 'top':
            box = (0, 0, img.size[0], size[1])
        elif crop_type == 'middle':
            box = (0, int(round((img.size[1] - size[1]) / 2)), img.size[0],
                int(round((img.size[1] + size[1]) / 2)))
        elif crop_type == 'bottom':
            box = (0, img.size[1] - size[1], img.size[0], img.size[1])
        else :
            raise ValueError('ERROR: invalid value for crop_type')
        img = img.crop(box)
    elif ratio < img_ratio:
        img = img.resize((int(round(size[1] * img.size[0] / img.size[1])), size[1]),
            PImage.ANTIALIAS)
        # Crop in the top, middle or bottom
        if crop_type == 'top':
            box = (0, 0, size[0], img.size[1])
        elif crop_type == 'middle':
            box = (int(round((img.size[0] - size[0]) / 2)), 0,
                int(round((img.size[0] + size[0]) / 2)), img.size[1])
        elif crop_type == 'bottom':
            box = (img.size[0] - size[0], 0, img.size[0], img.size[1])
        else :
            raise ValueError('ERROR: invalid value for crop_type')
        img = img.crop(box)
    else :
        img = img.resize((size[0], size[1]),
            PImage.ANTIALIAS)
    # If the scale is the same, we do not need to crop
    img.save(img_path)
@login_required
def change_profile_image(request):
    user = request.user
    p = user.userprofile
    if request.method == 'POST':
        form = ProfileImageForm(request.POST, request.FILES)
        if form.is_valid():
            old = p.avatar
            if old:
                old.delete()
            p.avatar = form.cleaned_data['image']
            p.save()
            user.save()

            if p.avatar:
                resize_and_crop(p.avatar.path, (250, 250))

        else:
            print form.errors

    return HttpResponseRedirect('/wetravel/settings/')


@login_required
def change_password(request):
    user = request.user
    response_data = {}
    if request.method == 'POST':
        password = request.POST['password']
        user.set_password(password);
        user.save();
        response_data['result'] = 'Information updated successfully!'
    
    else:
        response_data['result'] = 'Update failed'

    return HttpResponse(json.dumps(response_data),content_type="application/json")


@login_required
def change_address(request): 
    user = request.user
    response_data = {}
    if request.method == 'POST':
        p = user.userprofile
        r = p.region
        r.country = request.POST['country']
        r.state = request.POST['state']
        r.city = request.POST['city']
        r.save()
        p.save()
        user.save()

        country = user.userprofile.region.country;
        state = user.userprofile.region.state;
        city = user.userprofile.region.city;

        response_data['country'] = country;
        response_data['state'] = state;
        response_data['city'] = city;
        response_data['result'] = 'Information updated successfully!'
    
    else:
        response_data['result'] = 'Update failed'

    return HttpResponse(json.dumps(response_data),content_type="application/json")

