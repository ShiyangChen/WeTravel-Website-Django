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
from django.http.response import HttpResponseRedirect


def schedule_edit(request,travel_id):   
     
    error_message="" 
    travel=get_object_or_404(Travel,id=travel_id)

#     print travel.name
#     print travel.desc 
#     print travel.start_date
#     print travel.start_time
#     print travel.end_date
#     print travel.end_time
#     print travel.destination
#     print travel.members.all()
#     print travel.groups.all()
    
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
    user=request.user
    posts=Post.objects.order_by("-id")
    invi_posts=posts.filter(is_visible=True)
    posts_list=list(posts)
    for invi_post in invi_posts:

        for invi_friend in invi_post.restricted_members.all():
            if invi_friend.user.username==user.username:
                posts_list.remove(invi_post)
            else:
                continue

    return render(request, 'wetravel/index.html',{'posts':posts_list})

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




   # my_posts=Post.objects.filter(publisher=cur_user)
   # my_posts=my_posts.order_by("-id")
    #return render(request,'wetravel/profile.html',{'my_posts':my_posts})


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
                img = PImage.open(p.avatar.path)
                img.thumbnail((250,250), PImage.ANTIALIAS)
                img.save(img.filename)
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

