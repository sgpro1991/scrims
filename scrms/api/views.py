from django.shortcuts import render
from django.http import HttpResponse
from main.views import *
from users.models import User, Message, LastMessage, Membership
from datetime import datetime
from django.utils.dateparse import parse_datetime
from django.db.models import Q
# Create your views here.
from django.utils.html import strip_tags
from bs4 import BeautifulSoup
from sorl.thumbnail import get_thumbnail
import html

crypto = Crypto()


def SendMessage(request):
    auth_user = CheckAuth(request)
    if auth_user == False:
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
        '''
        def last_msg(insert,user,companion,type_msg):
            last_msg = LastMessage.objects.filter(companion_1=int(user.id),companion_2=int(companion)) | LastMessage.objects.filter(companion_1=int(companion),companion_2=int(user.id))
            if not last_msg:
                insert = LastMessage(companion_1=int(user.id),companion_2=int(companion),text=request.POST.get('body',False),type_msg=type_msg,id_msg=insert.id)
                insert.save()
            else:
                last_msg.update(text=request.POST.get('body',False),type_msg=type_msg,id_msg=insert.id)
        '''
        im = get_thumbnail(user.image,"50x50", crop="center")

        if type_msg == "text":
            escape_string = html.escape(request.POST.get('body',False)).replace("&lt;br&gt;","<br>")
            #body = crypto.Encrypt(escape_string)
            body = escape_string
            if request.GET.get('group',False) == '1':
                group = Group.objects.get(pk=companion)
                users = Membership.objects.get(group=group.id)
                users_mass = []
                for i in users.users.all():
                    if int(i.id) != int(auth_user[0]['id']):
                        users_mass.append(i.id)
                insert = Message(group=group,
                                 user=user,
                                 text=body,type_msg='1',
                                 date=date,
                                 img = im.url,
                                 delivered=True)
                companion = users_mass
                group = group.id
            else:
                insert = Message(user=user,
                                 companion=companion,
                                 text=body,type_msg='1',
                                 date=date,
                                 img = im.url,
                                 delivered=True)
                group = ''
            insert.save()
            #last_msg(insert,user,companion,type_msg)
            return HttpResponse('{"group":"'+str(group)+'","user":'+str(user.id)+',"companion":'+str(companion)+',"body":"'+escape_string+'","date":"'+date+'","type":"'+type_msg+'","id_msg":"'+str(insert.id)+'","img":"'+im.url+'"}')



        if type_msg == "file":
            string = request.POST.get('body',False)
            #body = crypto.Encrypt(string)

            body = string

            if request.GET.get('group',False) == '1':
                group = Group.objects.get(pk=companion)
                users = Membership.objects.get(group=group.id)
                users_mass = []
                for i in users.users.all():
                    if int(i.id) != int(auth_user[0]['id']):
                        users_mass.append(i.id)

                insert = Message(group=group,
                                 user=user,
                                 text=body,
                                 type_msg='1',
                                 date=date,
                                 img = im.url,
                                 delivered=True)
                companion = users_mass
                group = group.id
            else:
                insert = Message(user=user,
                                 companion=companion,
                                 text=body,
                                 type_msg='1',
                                 date=date,
                                 img=im.url,
                                 delivered=True)
                group = ''
            insert.save()
            #last_msg(insert,user,companion,type_msg)
            return HttpResponse('{"group":"'+str(group)+'","user":'+str(user.id)+',"companion":'+str(companion)+',"body":"'+string+'","date":"'+date+'","type":"'+type_msg+'","id_msg":"'+str(insert.id)+'","img":"'+im.url+'"}')



    else:
        return HttpResponse(status=404)




def GetStatus(request,id_user):
    if CheckAuth(request) == False:
        return HttpResponse(status=403)
    if id_user:
        if id_user == 'all':
            return HttpResponse('{"status":1}')
        user = User.objects.get(id=int(id_user))
        if user:
            return HttpResponse('{"status":'+str(int(user.status))+'}')




def ReadMsg(request,id_msg):
    if CheckAuth(request) == False:
        return HttpResponse(status=403)

    if id_msg:
        Message.objects.filter(pk=id_msg).update(reading=True)
        return HttpResponse('{"status":"200"}')
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
        json_user = json.loads(crypto.Decrypt(f.read()))
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
    group = request.GET.get('group',False)

    if int(group) == 1:
        count = Message.objects.filter(group=int(companion)).count()
        if (count-int(limit)-10) < 0:
            lim = 0
        else:
            lim = count-int(limit)-10

        if count-int(limit) < 0:
           lim2 = count
        else:
           lim2 = count-int(limit)

        data = Message.objects.filter(group=int(companion)).order_by('date')[lim:lim2]
        print(data)
        return HttpResponse(json.dumps(AsembleHistory(data,companion,True,request)))


    count = Message.objects.filter(Q(user=int(companion),companion=user)|Q(user=user,companion=int(companion))).count()

    if (count-int(limit)-10) < 0:
        lim = 0
    else:
        lim = count-int(limit)-10

    if count-int(limit) < 0:
       lim2 = count
    else:
       lim2 = count-int(limit)

    data = Message.objects.filter(Q(user=int(companion),companion=user)|Q(user=user,companion=int(companion))).order_by('date')[lim:lim2]
    return HttpResponse(json.dumps(AsembleHistory(data,companion,False,request)))







#получить историю в чате
def GetHistory(request):
    if CheckAuth(request) == False:
        return HttpResponse(status=403)
    else:
        pass

    user = CheckAuth(request)[0]['id']
    companion = request.GET.get('companion',False)
    group = request.GET.get('group',False)


    if int(group) == 1:
        count = Message.objects.filter(group=int(companion)).count()
        #not_read = Message.objects.filter(group=int(companion),reading=False)
        #if len(not_read)>0:
        if (count-10) <= 0:
            data = Message.objects.filter(group=int(companion)).order_by('date')
        else:
            data = Message.objects.filter(group=int(companion)).order_by('date')[(count-10):count]
        print(data)
        return HttpResponse(json.dumps(AsembleHistory(data,companion,True,request)))



    if companion == False:
        return HttpResponse(status=404)

    count = Message.objects.filter(Q(user=int(companion),companion=user)|Q(user=user,companion=int(companion))).count()
    not_read = Message.objects.filter(user=companion,companion=user,reading=False)



    if len(not_read)>0:
        if (count-len(not_read)-10) <= 0:
            data = Message.objects.filter(Q(user=int(companion),companion=user)|Q(user=user,companion=int(companion))).order_by('date')
        else:
            data = Message.objects.filter(Q(user=int(companion),companion=user)|Q(user=user,companion=int(companion))).order_by('date')[(count-len(not_read)-10):count]
        mass = []
        print(count-len(not_read))
        for a in not_read:
            print(a)
            mass.append(a.id)
        Message.objects.filter(pk__in=mass).update(reading=True)

    else:
        if count < 10:
            data = Message.objects.filter(Q(user=int(companion),companion=user)|Q(user=user,companion=int(companion))).order_by('date')
        else:
            data = Message.objects.filter(Q(user=int(companion),companion=user)|Q(user=user,companion=int(companion))).order_by('date')[(count-10):count]


    return HttpResponse(json.dumps(AsembleHistory(data,companion,False,request)))






def AsembleHistory(data,companion,group,request):

    mass = []
    for a in data:
        if group == False:
            if int(a.companion) == int(companion):
                message = 'main'
            else:
                message = 'recive'
        else:
            if int(a.user.id) == int(CheckAuth(request)[0]['id']):
                message = 'main'
            else:
                message = 'recive'

        body = a.text

        mass.append({
            'id':a.id,
            'user':a.user.id,
            'body':body,
            'img':a.img,
            'companion':a.companion,
            'message':message,
            'date':str(a.date),
            'delivered':a.delivered,
            'reading':a.reading
        })
    return mass








def GetUsersGroup(request,id_group):
    user = CheckAuth(request)
    if user == False:
        return HttpResponse(status=403)
    else:
        pass

    if id_group == False:
        return HttpResponse(status=404)

    users = Membership.objects.filter(group=int(id_group))

    users_mass = []
    for a in users:
        for i in a.users.all():
            if int(i.id) != int(user[0]['id']):
                users_mass.append(i.id)



    return HttpResponse(json.dumps(users_mass))
