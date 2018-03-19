from django.shortcuts import render
from django.http import HttpResponse
from main.views import *
from users.models import User, Message, LastMessage, Membership, Group
from datetime import datetime
from django.utils.dateparse import parse_datetime
from django.db.models import Q
# Create your views here.
from django.utils.html import strip_tags
from bs4 import BeautifulSoup
from sorl.thumbnail import get_thumbnail
import html
from django.utils.crypto import get_random_string
from django.db import IntegrityError
from sorl.thumbnail import get_thumbnail
from django.contrib.postgres.search import SearchVector

crypto = Crypto()


def CreateGroup(request):
    auth_user = CheckAuth(request)
    if auth_user == False:
        return HttpResponse(status=403)

    name = request.POST.get('name', False)
    users_group = request.POST.get('users',False)

    user_admin = User.objects.get(init=auth_user[0]['id'])

    #### CREATE GROUP #####
    init = get_random_string(length=32)
    key = get_random_string(length=32)
    try:
        insert = Group(init=init,admin=user_admin.id,name=name,date_create=datetime.now(),public_key=key)
        insert.save()
    except IntegrityError as e:
        return HttpResponse('{"status":"error","reason":"name exist"}')
    #### /CREATE GROUP #####

    users_in_group = User.objects.filter(init__in= users_group.split(','))
    a = list(users_in_group)

    for i in users_in_group:
        usr = User.objects.get(id=i.id)
        usr.group.add(insert.id)

    insert_membership = Membership(group=init)
    insert_membership.save()
    member = Membership.objects.get(group=init)
    member.users.add(*a)

    return HttpResponse('{"status":"success","init":"'+init+'","name":"'+name+'"}')




def GetUsers(request):
    user = CheckAuth(request)
    if user == False:
        return HttpResponse(status=403)


    user_data = User.objects.get(init=user[0]['id'])
    users = User.objects.all().exclude(init=user[0]['id']).order_by('-status')


    ids = []
    for i in user_data.group.all():
        ids.append(i.id)

    group = Group.objects.filter(pk__in=ids) # получаем группы в которых состоит юзер

    group_mass = []
    for a in group:
        count = Message.objects.filter(group=a.init,reading_group=user_data).count()

        if a.image.name != None:
            img = get_thumbnail(a.image, "50x50", crop="center")
        else:
            img = ''
        group_mass.append({
            "search":a.name,
            "id":a.init,
            "name":a.name,
            "count_msg":str(count),
            "img":img,
            "status":True,
            #"users_group":
            "last_msg":"",
            "last_msg_type":"",
            "public_key":a.public_key,
        })


    user_mass = []
    for a in users:
        count = Message.objects.filter(user=a.init,companion=user[0]['id'],reading=False).count()
        last_message = LastMessage.objects.filter(companion_1=a.init,companion_2=user[0]['id']) | LastMessage.objects.filter(companion_1=user[0]['id'],companion_2=a.init)
        m = []
        for i in group:
            m.append(i.name)

        if a.image.name != None:
            img = get_thumbnail(a.image, "50x50", crop="center")
        else:
            img = ''
        user_mass.append({
            "group":m,
            "search":a.name.split(" "),
            "id":a.init,
            "name":a.name,
            "count_msg":str(count),
            "img":img.url,
            "status":a.status,
            "last_msg":'',#last_message,
            "last_msg_type":'',
            "public_key":a.public_key_user,
        })
    common_mass = user_mass+group_mass
    #print(common_mass)

    return HttpResponse(json.dumps(common_mass))






















def SearchUsers(request,word):
    user = CheckAuth(request)
    if user == False:
        return HttpResponse(status=403)

    user_data = User.objects.get(init=user[0]['id'])

    if word != 'all':
        group = Group.objects.annotate(
                search=SearchVector('name'),
        ).filter(search=word)

        users = User.objects.annotate(
                search=SearchVector('name','dep__name','email'),
        ).filter(search=word).exclude(init=user[0]['id'])
    else:
        group = Group.objects.all()
        users = User.objects.all().exclude(init=user[0]['id']).order_by('-status')


    group_mass = []
    for a in group:
        count = Message.objects.filter(group=a.init,reading_group=user_data).count()

        if a.image.name != None:
            img = get_thumbnail(a.image, "50x50", crop="center")
        else:
            img = ''
        group_mass.append({
            "search":a.name,
            "id":a.init,
            "name":a.name,
            "count_msg":str(count),
            "img":img,
            "status":True,
            #"users_group":
            "last_msg":"",
            "last_msg_type":"",
            "public_key":a.public_key,
            "group":True,
        })




    #users = User.objects.filter(name__search)


    user_mass = []
    for a in users:
        count = Message.objects.filter(user=a.init,companion=user[0]['id'],reading=False).count()
        last_message = LastMessage.objects.filter(companion_1=a.init,companion_2=user[0]['id']) | LastMessage.objects.filter(companion_1=user[0]['id'],companion_2=a.init)
        m = []
        for i in group:
            m.append(i.name)

        if a.image.name != None:
            img = get_thumbnail(a.image, "50x50", crop="center")
        else:
            img = ''
        user_mass.append({
            "group":False,
            "search":a.name.split(" "),
            "id":a.init,
            "name":a.name,
            "count_msg":str(count),
            "img":img.url,
            "status":a.status,
            "last_msg":'',#last_message,
            "last_msg_type":'',
            "public_key":a.public_key_user,
        })
    common_mass = user_mass+group_mass


    return HttpResponse(json.dumps(common_mass))



def SendMessage(request):
    auth_user = CheckAuth(request)
    if auth_user == False:
        return HttpResponse(status=403)

    user = User.objects.get(init=CheckAuth(request)[0]['id'])
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

        ###################
        # IF TEXT MESSAGE
        ##################
        if type_msg == "text":
            escape_string = html.escape(request.POST.get('body',False)).replace("&lt;br&gt;","<br>")
            #body = crypto.Encrypt(escape_string)
            body = escape_string
            ###### IF GROUP #####
            if request.GET.get('group',False) == '1':
                group = Group.objects.get(init=companion)
                users = Membership.objects.get(group=group.init)
                users_mass = []
                for i in users.users.all():
                    if i.init != auth_user[0]['id']:
                        users_mass.append(i.init)

                insert = Message(group=group.init,
                                 user=user.init,
                                 text=body,
                                 type_msg='1',
                                 date=date,
                                 img = im.url,
                                 delivered=True)
                companion = users_mass
                group = group.init
                insert.save()
                for a in users_mass:
                    usr = User.objects.get(init=a)
                    insert.reading_group.add(usr)
            else:
                insert = Message(user=user.init,
                                 companion=companion,
                                 text=body,
                                 type_msg='1',
                                 date=date,
                                 img = im.url,
                                 delivered=True)
                group = ''
                insert.save()

            #last_msg(insert,user,companion,type_msg)
            json_resp = {"group":str(group),
                    "user":str(user.init),
                    "companion":str(companion),
                    "body":escape_string,
                    "date":date,
                    "type":type_msg,
                    "id_msg":str(insert.id),
                    "img":im.url,
                    }
            return HttpResponse(json.dumps(json_resp))

        ###################
        # IF FILE MESSAGE
        ##################
        if type_msg == "file":
            string = request.POST.get('body',False)
            #body = crypto.Encrypt(string)

            body = string
            if request.GET.get('group',False) == '1':
                group = Group.objects.get(init=companion)
                users = Membership.objects.get(group=group.init)
                users_mass = []
                for i in users.users.all():
                    if i.init != auth_user[0]['id']:
                        users_mass.append(i.init)

                insert = Message(group=group.init,
                                 user=user.init,
                                 text=body,
                                 type_msg='2',
                                 date=date,
                                 img = im.url,
                                 delivered=True)
                companion = users_mass
                group = group.init
                insert.save()
                for a in users_mass:
                    usr = User.objects.get(init=a)
                    insert.reading_group.add(usr)
            else:
                insert = Message(user=user.init,
                                 companion=companion,
                                 text=body,
                                 type_msg='2',
                                 date=date,
                                 img=im.url,
                                 delivered=True)
                group = ''
                insert.save()
            #last_msg(insert,user,companion,type_msg)
            json_resp = {"group":str(group),
                        "user":str(user.init),
                        "companion":str(companion),
                        "body":body,
                        "date":date,
                        "type":type_msg,
                        "id_msg":str(insert.id),
                        "img":im.url
                        }
            return HttpResponse(json.dumps(json_resp))


            #return HttpResponse('{"group":"'+str(group)+'","user":'+str(user.id)+',"companion":'+str(companion)+',"body":"'+string+'","date":"'+date+'","type":"'+type_msg+'","id_msg":"'+str(insert.id)+'","img":"'+im.url+'"}')

    else:
        return HttpResponse(status=404)




def GetStatus(request,id_user):
    if CheckAuth(request) == False:
        return HttpResponse(status=403)
    if id_user:
        if id_user == 'all':
            return HttpResponse('{"status":1}')
        user = User.objects.get(init=id_user)
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
            User.objects.filter(init=json_user[0]['id']).update(status=True)
        if status == 'off':
            User.objects.filter(init=json_user[0]['id']).update(status=False)
        return HttpResponse(json_user[0]['id'])
    else:
        return HttpResponse(status=403)




def GetHistoryAbout(request):
    user_auth = CheckAuth(request)
    if user_auth == False:
        return HttpResponse(status=403)
    else:
        pass

    user = CheckAuth(request)[0]['id']
    companion = request.GET.get('companion',False)
    limit = request.GET.get('limit',False)
    group = request.GET.get('group',False)

    if int(group) == 1:
        count = Message.objects.filter(group=companion).count()
        if (count-int(limit)-10) < 0:
            lim = 0
        else:
            lim = count-int(limit)-10

        if count-int(limit) < 0:
           lim2 = count
        else:
           lim2 = count-int(limit)

        data = Message.objects.filter(group=companion).order_by('date')[lim:lim2]
        print(data)
        try:
            data.update(reading=True)
        except:
            pass

        for a in data:
            usr = User.objects.get(init=user)
            a.reading_group.remove(usr)
        return HttpResponse(json.dumps(AsembleHistory(data,companion,True,request,user_auth)))


    count = Message.objects.filter(Q(user=companion,companion=user)|Q(user=user,companion=companion)).count()

    if (count-int(limit)-10) < 0:
        lim = 0
    else:
        lim = count-int(limit)-10

    if count-int(limit) < 0:
       lim2 = count
    else:
       lim2 = count-int(limit)

    data = Message.objects.filter(Q(user=companion,companion=user)|Q(user=user,companion=companion)).order_by('date')[lim:lim2]
    return HttpResponse(json.dumps(AsembleHistory(data,companion,False,request,user_auth)))







#получить историю в чате
def GetHistory(request):
    user_auth = CheckAuth(request)
    if user_auth == False:
        return HttpResponse(status=403)
    else:
        pass

    user = CheckAuth(request)[0]['id']
    companion = request.GET.get('companion',False)
    group = request.GET.get('group',False)


    if int(group) == 1:
        count = Message.objects.filter(group=companion).count()
        if (count-10) <= 0:
            data = Message.objects.filter(group=companion).order_by('date')
        else:
            data = Message.objects.filter(group=companion).order_by('date')[(count-10):count]
        try:
            data.update(reading=True)
        except:
            pass

        for a in data:
            usr = User.objects.get(init=user)
            a.reading_group.remove(usr)
        return HttpResponse(json.dumps(AsembleHistory(data,companion,True,request,user_auth)))



    if companion == False:
        return HttpResponse(status=404)

    count = Message.objects.filter(Q(user=companion,companion=user)|Q(user=user,companion=companion)).count()
    not_read = Message.objects.filter(user=companion,companion=user,reading=False)

    if len(not_read)>0:
        if (count-len(not_read)-10) <= 0:
            data = Message.objects.filter(Q(user=companion,companion=user)|Q(user=user,companion=companion)).order_by('date')
        else:
            data = Message.objects.filter(Q(user=companion,companion=user)|Q(user=user,companion=companion)).order_by('date')[(count-len(not_read)-10):count]
        mass = []
        print(count-len(not_read))
        for a in not_read:
            print(a)
            mass.append(a.id)
        Message.objects.filter(pk__in=mass).update(reading=True)

    else:
        if count < 10:
            data = Message.objects.filter(Q(user=companion,companion=user)|Q(user=user,companion=companion)).order_by('date')
        else:
            data = Message.objects.filter(Q(user=companion,companion=user)|Q(user=user,companion=companion)).order_by('date')[(count-10):count]


    return HttpResponse(json.dumps(AsembleHistory(data,companion,False,request,user_auth)))






def AsembleHistory(data,companion,group,request,user_auth):
    mass = []
    for a in data:
        if group == False:
            if a.companion == companion:
                message = 'main'
            else:
                message = 'recive'
        else:
            if a.user == user_auth[0]['id']:
                message = 'main'
            else:
                message = 'recive'

        body = a.text

        mass.append({
            'id':a.id,
            'user':a.user,
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

    users = Membership.objects.filter(group=id_group)

    users_mass = []
    for a in users:
        for i in a.users.all():
            if i.init != user[0]['id']:
                users_mass.append(i.init)

    return HttpResponse(json.dumps(users_mass))
