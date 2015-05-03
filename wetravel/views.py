from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from wetravel.form import *
from wetravel.models import *
from PIL import Image as PImage
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime
import time

import json

import random

def schedule_edit(request,travel_id):   
     
    error_message="" 
    travel=get_object_or_404(Travel,id=travel_id)


    this_user=request.user     
    this_userprofile=get_object_or_404(UserProfile,user=this_user)  
    regions=get_list_or_404(Region)
    this_friends=this_userprofile.friends #check
    #this_groups=get_list_or_404(Group,members=this_userprofile)
    this_groups=Group.objects.filter(members=this_userprofile)    
           
    if request.method == 'POST':
        name1=request.POST.get('name')
        desc1=request.POST.get('desc')
        start_date1=request.POST.get('start_time_0')
        start_time1=request.POST.get('start_time_1')
        end_date1=request.POST.get('end_time_0')
        end_time1=request.POST.get('end_time_1')
        destination1=request.POST.get('destination')        
        members1=request.POST.getlist('members')
        groups1=request.POST.getlist('groups')
        
        if(name1=="" and destination1==""):            
            error_message="Enter the mandatory fields"
        elif(members1==None and groups1==None):
            error_message="Enter the mandatory fields. You must enter atleast one of members or groups."
    
        if error_message=="":
            # save here
            travel.name=name1
            travel.desc =desc1
            
            try:
                start_day=datetime.strptime(start_date1,'%b %d, %Y')
            except ValueError:    
                start_day=datetime.strptime(start_date1,'%Y-%m-%d')
                
            #print start_day, start_day.strftime('%Y-%m-%d')              
            travel.start_date=start_day.strftime('%Y-%m-%d')           
            
            if len(start_time1.split(" "))==1:               
               start_time=time.strptime(start_time1,'%H:%M:%S') 
            else:
                parts=start_time1.split(" ")
                
                timeperiod="AM"
                if parts[1]=="p.m.":
                    timeperiod="PM"
                
                parts2=parts[0].split(":")
                if(len(parts2)==1):
                    start_time=time.strptime(parts[0]+" "+timeperiod,'%I %p')
                else:
                    start_time=time.strptime(parts[0]+" "+timeperiod,'%I:%M %p')
            
                
            #print start_time, time.strftime('%H:%M:%S',start_time)
            travel.start_time=time.strftime('%H:%M:%S',start_time) 
            
            
            try:
                end_day=datetime.strptime(end_date1,'%b %d, %Y')
            except ValueError:    
                end_day=datetime.strptime(end_date1,'%Y-%m-%d')            
            
            travel.end_date=end_day.strftime('%Y-%m-%d')
            
            
            
            if len(end_time1.split(" "))==1:
               end_time=time.strptime(end_time1,'%H:%M:%S') 
            else:
                parts=end_time1.split(" ")
                timeperiod="AM"
                if parts[1]=="p.m.":
                    timeperiod="PM"
                
                parts2=parts[0].split(":")
                if(len(parts2)==1):
                    end_time=time.strptime(parts[0]+" "+timeperiod,'%I %p')
                else:
                    end_time=time.strptime(parts[0]+" "+timeperiod,'%I:%M %p')
                
            #print end_time, time.strftime('%H:%M:%S',end_time)
            travel.end_time=time.strftime('%H:%M:%S',end_time) 
            
            parts=destination1.split("/")
            
            regions =Region.objects.filter(city=parts[0],state=parts[1],country=parts[2])
            if(regions!=None and len(regions)>0):
                travel.destination=regions[0]
                      
            
            travel.members.clear()            
            for member1 in members1:  
                #print member1              
                newuser=User.objects.get(username=member1)
                if newuser!=None:
                    newuserp=UserProfile.objects.filter(user=newuser)
                    if newuserp!=None and len(newuserp)>0:
                        #print newuserp[0]
                        travel.members.add(newuserp[0])
            
            travel.groups.clear()
            for group1 in groups1:
                newgroup=Group.objects.filter(name=group1)
                if newgroup!=None and len(newgroup)>0:
                    #print newgroup[0]
                    travel.groups.add(newgroup[0])
            
            travel.save()
            return HttpResponseRedirect("/wetravel/schedule")
        
        
    
     
    return render(request,'wetravel/schedule_edit.html',{'travel':travel,'regions':regions, 'this_friends':this_friends,'this_groups':this_groups,'error_message':error_message})
    
@login_required
def schedule(request):
     this_user=request.user     
     this_userprofile=get_object_or_404(UserProfile,user=this_user)     
     #this_travels=get_list_or_404(Travel,members=this_userprofile)
     this_travels=Travel.objects.filter(members=this_userprofile)    
     #print this_user, this_userprofile, this_travels
    
     return render(request,'wetravel/schedule.html',{'travels':this_travels})

def index(request):
    if request.user.is_authenticated():

        context_dict = {}

        #posts part
        cur_user=request.user.userprofile
        user_friends=cur_user.friends.all()
      

        posts=Post.objects.order_by("-id")
        posts_list=[]
        userprofile_id=[]
        for post in posts:
            if (post.publisher==cur_user):
                posts_list.append(post)
               # userprofile_id.append(cur_user.id)
            for friend in user_friends:

                if (post.publisher==friend):
                    posts_list.append(post)
                    #userprofile_id.append(friend.id)

        invi_posts=posts.filter(is_visible=True)
        #posts_list=list(posts)
        for invi_post in invi_posts:

            for invi_friend in invi_post.restricted_members.all():
                if invi_friend.user.username==request.user.username:
                    posts_list.remove(invi_post)
                else:
                    continue

         #recommendation part
        candidates1 = friends_goto_same_place(request.user)
        candidates2 = friends_been_there_before(request.user)
        candidates3 = recommend_new_friend(request.user)

        common_friends_all = []
        num_common_friends_all = []

        for recommended_friend in candidates3:
            common_friends = get_common_friends(recommended_friend, request.user.userprofile)
            num_common_friends = len(common_friends)
            common_friends_all.append(common_friends)
            num_common_friends_all.append(num_common_friends)


        var1 = "common_friends_"
        var2 = "num_common_friends_"
        for i in range (len(common_friends_all)):
            new_var1 = var1 + str(i+1)
            new_var2 = var2 + str(i+1)
            context_dict[new_var1] = common_friends_all[i]
            context_dict[new_var2] = num_common_friends_all[i]

        comment_lists=Comment.objects.order_by("-id")

        context_dict.update({
            'candidates1': candidates1,
            'candidates2': candidates2,
            'candidates3': candidates3, 
            'posts':posts_list,
            'comment_lists':comment_lists
        })

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
    random.shuffle(candidates)
    return candidates[:3]

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
    random.shuffle(candidates)
    return candidates[:3]

# recommend new friends for you:
def recommend_new_friend(user):
    candidates = []
    if user.userprofile:
        friends = user.userprofile.friends.all();
        for friend in friends:
            if friend:
                for slfriend in friend.friends.all():
                    if slfriend and slfriend not in candidates and slfriend != user.userprofile and slfriend not in friends:
                        for visited_place in slfriend.visited.all():
                            if user.userprofile.to_visit and visited_place.region == user.userprofile.to_visit.region:
                                candidates.append(slfriend)
                                break
                        if slfriend not in candidates:
                            if slfriend.to_visit:
                                if user.userprofile.to_visit and slfriend.to_visit.region == user.userprofile.to_visit.region:
                                    candidates.append(slfriend)
    random.shuffle(candidates)
    return candidates[:3]

def get_common_friends(user1, user2):
    friends_user1 = user1.friends.all()
    friends_user2 = user2.friends.all()
    common_friends = list(friends_user1 & friends_user2)
    random.shuffle(common_friends)
    return common_friends


def about(request):
    return render(request, 'wetravel/about.html')

def signup(request):
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

            user = authenticate(username=request.POST['username'],
                                password=request.POST['password'])
            login(request, user)

            return HttpResponseRedirect('/wetravel/')
        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
            'wetravel/signup.html',
            {'user_form': user_form, 'profile_form': profile_form})



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
            target_user.userprofile.requests.add(request.user.userprofile)
        except User.DoesNotExist:
            print "User {0} does not exist".format(target_username)
            return HttpResponse("User not found.")
        return HttpResponseRedirect('/wetravel/')
    else:
        return HttpResponseRedirect('/wetravel/friends/')

def friends(request):
    return render(request, 'wetravel/friends.html', {})

def requests(request):
    return render(request, 'wetravel/requests.html', {})

def process_request(request):
    # import pdb; pdb.set_trace()
    if 'accept' in request.POST:
        userprofile = request.user.userprofile
        requester_username = request.POST.get('requester_username')
        requesterprofile = User.objects.get(username=requester_username).userprofile
        userprofile.friends.add(requesterprofile)
    userprofile.requests.remove(requesterprofile)
    return HttpResponseRedirect('/wetravel/friends')


def places(request):

    return render(request, 'wetravel/addplace.html', {})

def add_to_visit(request):
    if 'submit' in request.POST:
        userprofile = request.user.userprofile
        place = Place.objects.filter(address=request.POST.get('address'))
        if place:
            userprofile.to_visit = place[0]

    return HttpResponseRedirect('/wetravel/places')

def add_visited(request):
    if 'submit1' in request.POST:
        userprofile = request.user.userprofile
        place = Place.objects.filter(address=request.POST.get('address1'))
        comment = request.POST.get('comment')
        if place:
            if comment:
                place_comment = PlaceComment(text=comment)
                place_comment.place = place[0]
                place_comment.save()
            userprofile.visited.add(place[0])

    return HttpResponseRedirect('/wetravel/places')


def show_profile(request):
    posts = Post.objects.filter(publisher=request.user.userprofile)
    return render(request, 'wetravel/profile.html', {'posts': posts})


def create_post(request):
    return render(request, 'wetravel/create_post.html')

@login_required
def createpost(request):
    if 'text_message' in request.GET:
        text_message=request.GET['text_message']
      
        cur_user=request.user.userprofile
    
        b=Post(text=text_message,publisher=cur_user)#login_user)
        b.save()
        set_post=Post.objects.get(text=text_message,publisher=cur_user)
        return HttpResponseRedirect('/wetravel/privacy_choose/{}/'.format(set_post.id))  ##
        #return HttpResponseRedirect('/wetravel/')

    else:
        return HttpResponse('submitted a empty form')

@login_required
def profile(request,param1):
    user=request.user   #???
    cur_user=request.user.userprofile
    check_user=UserProfile.objects.get(id=param1)
    my_posts=Post.objects.filter(publisher=check_user)
    my_posts=my_posts.order_by("-id")
    return render(request,'wetravel/profile.html',{'my_posts':my_posts,'user':user})

@login_required
def delete_confirm(request,param1):
    cur_user=request.user.userprofile
    my_posts=Post.objects.filter(publisher=cur_user)
    my_posts=my_posts.order_by("-id")
    param2=cur_user.id
    return render(request,'wetravel/delete_confirm.html',{'param':param1, 'my_posts':my_posts,'param2':param2})




@login_required
def delete(request,param1):
    cur_user=request.user.userprofile
    my_posts=Post.objects.filter(publisher=cur_user)
 
    del_post=my_posts.get(id=param1)
    del_post.delete()
    my_posts=Post.objects.filter(publisher=cur_user)
    my_posts=my_posts.order_by("-id")
    
    return render(request,'wetravel/profile.html',{'my_posts':my_posts})
    #return HttpResponseRedirect('/wetravel/profile/{}'.format(cur_user.id))
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
    set_post.is_visible=False   # initialize as false every time
    set_post.save()
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
    elif exc_inc=="include":

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
    else:
        return HttpResponseRedirect("/wetravel/")
    return HttpResponseRedirect("/wetravel/profile/{}/".format(cur_user.id))

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
            #if old:
                #old.delete()
            p.avatar = form.cleaned_data['image']
            p.save()
            user.save()

            if p.avatar:
                resize_and_crop(p.avatar.path, (900, 600))

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


def comment_upload(request,param1):
    user=request.user
    cur_user=user.userprofile

    if request.method == 'POST':

        comment_info=request.POST['comment']
        #response_data = {}
        #response_data['comment_value']=comment_info
        #return HttpResponse(json.dumps(response_data),content_type="application/json")
        comment_post=Post.objects.get(id=param1)
        c=Comment(login_user=user,text=comment_info,to_post=comment_post)
        c.save()
        return HttpResponseRedirect('/wetravel/')
        

        # print "it's a test"
        #print request.POST['comment']
        #return HttpResponse("successfully")

    else:  
        return HttpResponse("<h1>test</h1>") 

