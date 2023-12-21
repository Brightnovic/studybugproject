from django.shortcuts import render
from django.http import JsonResponse
import random
import time
from django.contrib.auth.decorators import login_required
from agora_token_builder import RtcTokenBuilder
from .models import RoomMember
import json
from django.views.decorators.csrf import csrf_exempt
from base.models import User



# Create your views here.
@login_required(login_url='login')
def lobby(request, pk):
   title = "video call form"
   user = User.objects.get(id=pk)
   context = {'user': user, 'title': title}
   return render(request, 'videocall/lobby.html',context )





@login_required(login_url='login')
def room(request):
    title = "fun room"
    context = {'title': title}
    return render(request, 'videocall/room.html')


def getToken(request):
    appId = "0249efe355bd44ee881471d2359afc77"
    appCertificate = "281107a42c584fa7bd34d3bcd4cc2c8a"
    channelName = request.GET.get('channel')
    print(appId,appCertificate,channelName)
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