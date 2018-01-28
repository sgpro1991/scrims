from django.shortcuts import render
from django.http import HttpResponse
from main.views import *
from users.models import User, Message
from datetime import datetime
from django.utils.dateparse import parse_datetime
from django.db.models import Q
# Create your views here.


def SendMessage(request):
    if CheckAuth(request) == False:
        return HttpResponse(status=403)
    user = User.objects.get(pk=CheckAuth(request)[0]['id'])
    companion = request.POST.get('companion',False)
    type_msg = request.POST.get('type',False)
    date = request.POST.get('date',False)

    if companion and type_msg and date:
        if companion == "NaN":
            return HttpResponse(status=400)
        else:
            pass
        if type_msg == "text":
            body = Crypto().Encrypt(request.POST.get('body',False))
            insert = Message(user=user,companion=companion,text=body,type_msg='1',date=date)
            insert.save()
            return HttpResponse(insert.id)
    else:
        return HttpResponse(status=404)










def SetStatus(request):
    token = request.GET.get('token',False)
    status = request.GET.get('status',False)
    if token and status:
        pass
    else:
        return HttpResponse(status=404)

    check = os.path.exists(BASE_DIR+'/sessions/'+token)
    if check == True:
        f = open(BASE_DIR+'/sessions/'+token, encoding='utf-8')
        json_user = json.loads(Crypto().Decrypt(f.read()))
        if status == 'on':
            User.objects.filter(id=json_user[0]['id']).update(status=True)
        if status == 'off':
            User.objects.filter(id=json_user[0]['id']).update(status=False)
        return HttpResponse(json_user[0]['id'])
    else:
        return HttpResponse(status=403)





def GetHistoryAbout(request):
    if CheckAuth(request) == False:
        return HttpResponse(status=403)
    else:
        pass

    user = CheckAuth(request)[0]['id']
    companion = request.GET.get('companion',False)
    limit = request.GET.get('limit',False)

    count = Message.objects.filter(Q(user=int(companion),companion=user)|Q(user=user,companion=int(companion))).count()
    if count < (count-int(limit)-10):
        data = Message.objects.filter(Q(user=int(companion),companion=user)|Q(user=user,companion=int(companion))).order_by('date')
    else:
        print(count-int(limit)-10,count-int(limit))
        data = Message.objects.filter(Q(user=int(companion),companion=user)|Q(user=user,companion=int(companion))).order_by('date')[count-int(limit)-10:count-int(limit)]


    mass = []
    for a in data:
        if int(a.companion) == int(companion):
            message = 'main'
        else:
            message = 'recive'

        mass.append({
            'id':a.id,
            'user':a.user.id,
            'body':Crypto().Decrypt(a.text),
            'companion':a.companion,
            'message':message,
            'date':str(a.date)
        })

    return HttpResponse(json.dumps(mass))







#получить историю в чате
def GetHistory(request):
    if CheckAuth(request) == False:
        return HttpResponse(status=403)
    else:
        pass

    user = CheckAuth(request)[0]['id']
    companion = request.GET.get('companion',False)

    if companion == False:
        return HttpResponse(status=404)


    count = Message.objects.filter(Q(user=int(companion),companion=user)|Q(user=user,companion=int(companion))).count()

    if count < 10:
        data = Message.objects.filter(Q(user=int(companion),companion=user)|Q(user=user,companion=int(companion))).order_by('date')
    else:
        data = Message.objects.filter(Q(user=int(companion),companion=user)|Q(user=user,companion=int(companion))).order_by('date')[(count-10):count]




    mass = []
    for a in data:
        if int(a.companion) == int(companion):
            message = 'main'
        else:
            message = 'recive'

        mass.append({
            'id':a.id,
            'user':a.user.id,
            'body':Crypto().Decrypt(a.text),
            'companion':a.companion,
            'message':message,
            'date':str(a.date)
        })

    return HttpResponse(json.dumps(mass))
