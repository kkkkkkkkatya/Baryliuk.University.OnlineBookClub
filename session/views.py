from django.shortcuts import render, redirect,  get_object_or_404

from .models import *
from django.utils import timezone
from main.keeper_service import keeper_service
from user.models import  Profile_user
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from django.http import JsonResponse
import random
import time
from agora_token_builder import RtcTokenBuilder
from .models import RoomMember
import json
from django.views.decorators.csrf import csrf_exempt


def session_list(request):
    sessions_list = Session.objects.order_by('-id')
    author = False

    user = request.user
    user_profile = Profile_user.objects.filter(user_id=user.id)
    if user_profile.exists():
        profile_u = Profile_user.objects.get(user_id=user.id)
        print('profile_u: ', profile_u.is_author)
        if profile_u.is_author == True:
            author = True

    print('author: ', author)
    return render(request, 'session/list.html',
                  {'instance_list':sessions_list, 'author': author})


class SessionCreateView(generic.CreateView):
    model = Session
    fields = '__all__'
    success_url = reverse_lazy("session:list")


def lobby(request):
    return render(request, 'session/lobby.html')


def room(request):
    return render(request, 'session/room.html')


def getToken(request):
    appId = "1205b0a15dfd455da1557447ea57bf21"
    appCertificate = "2d87cdbb981d452396fa24ff2ae60beb"
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid}, safe=False)


@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )

    return JsonResponse({'name':data['name']}, safe=False)


def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({'name':member.name}, safe=False)


@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    member = RoomMember.objects.get(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    member.delete()
    return JsonResponse('Member deleted', safe=False)
