from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import *
from main.keeper_service import keeper_service
from .forms import *
from main.views import index
from django.conf import settings
import os
from group.models import RelGroupUser, Group
from session.models import Session

# Create your views here.

def user_list(request):
    users_list = User.objects.order_by('-id')
    return render(request, 'user/list.html', {'instance_list':users_list})

### show profile ###
def show(request, id):
    #print(f"=== user, action: show === ")
    #print(f"id: ", id)
    action= "show"
    error = keeper_service.pop("error")
    user_profile = []
    image_profile = os.path.join(settings.MEDIA_URL, 'images', 'user_profile.jpg')

    user = get_object_or_404(User, id=id)
    groups_list = ''

    user_profile = Profile_user.objects.filter(user_id=id)
    #print(f"user_profile: ", user_profile)

    if user_profile.exists():
        profile_u = Profile_user.objects.get(user_id=id)
        #print(f"profile_u ", profile_u)
        session = Session.objects.filter(author=id).values_list('room_name', flat=True).first()

        member = RelGroupUser.objects.filter(user_id=id)
        if member.exists():
            sql = f"""select g.id , g.topic, r.id as rel_id
                        from group_relgroupuser r
                             join group_group g on g.id = r.group_id
                             where r.user_id = {id}"""
            groups_list = RelGroupUser.objects.raw(sql)
            #print(f" groups_list", groups_list)


    else:
        profile_u = Profile_user()
        profile_u.user = user
        profile_u.save()

    return render(request, 'user/show.html',
                  { 'error':error, 'id':id, 'image_profile':image_profile,
                   'profile_u':profile_u, 'groups_list':groups_list, 'session':session })


### edit user ###
def edit(request, id):
    print(f"=== user, action: edit === ")
    print(f"id: ", id)
    print(f"method: ", request.method)
    error = ''
    cur_action = "edit"

    user = get_object_or_404(User, id=id)
    profile_u = None
    image_url = ""

    profile_u = Profile_user.objects.get(user_id=id)
    print(f"profile_u ", profile_u)
    if profile_u.images:
        print(f"image.url: {profile_u.images.url}")
        image_url = profile_u.images.url

    ### update profile
    if request.method == 'POST':
        form = ProfileUserForm(request.POST, request.FILES, instance=profile_u)
        if form.is_valid():
            form.save()
            return redirect('user:show', id=id)  # Redirect to profile detail view
        else:
            error = 'Помилки при заповненні форми'
            print('Помилки при заповненні форми')
    ### open form for updating
    else:
        form = ProfileUserForm(instance=profile_u)



    return render(request, 'user/edit.html',
                  {'form': form, 'error': error, 'id': id,
                   'image_url': image_url, 'cur_action': cur_action})

### delete user ###
def delete(request, id):
    print(f"=== user, action: delete === ")
    print(f"id: ", id)
    user = request.user

    try:
        obj = None
        user = get_object_or_404(User, id=id)
        obj = Profile_user.objects.get(user_id=id)
        print(f"obj: {obj}")
        obj.delete()
        user.delete()
    except (Exception) as e:
        keeper_service.push("error", str(e))
        print(f"Error: {e}")
    if user.is_staff:
        redirect('manager:users_list')

    return redirect('main:home')