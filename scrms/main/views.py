from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from scrms.settings import BASE_DIR,LANG,MEDIA_ROOT,MEDIA_URL
from users.models import User,Storage,Message,LastMessage,Group,Membership,Post
from django.utils.crypto import get_random_string
import os
import json
from datetime import datetime,date
import re
from PIL import Image
import hashlib



class Crypto:
    from cryptography.fernet import Fernet
    from crypto.key import KEY
    def __init__(self,fernet=Fernet(KEY)):
        self.fernet = fernet

    def Encrypt(self,text):
        self.text = text
        if isinstance(text, bytes) == True:
            return self.fernet.encrypt(text)
        if isinstance(text, str) == True:
            return str(self.fernet.encrypt(bytes(self.text.encode('utf-8')))).replace("b'",'').replace("'","")

    def Decrypt(self,text):
        self.text = text

        if isinstance(text, bytes) == True:
            decryptor = self.fernet.decrypt(text)
            return decryptor


        if isinstance(text, str) == True:
            decryptor = self.fernet.decrypt(bytes(text.encode('utf-8')))
            return str(decryptor.decode('utf-8'))



crypto = Crypto()





def Auth(request):
    email = request.POST.get('email',False)
    password = request.POST.get('password',False)
    print(password)
    if email and password:
        if User.objects.filter(email=email).exists():
            a = User.objects.get(email=email)
            user_pass = crypto.Decrypt(a.password)

            if a.hash_password == password:
                resp = HttpResponse(status=200)
                token = get_random_string(length=32)
                resp.set_cookie('SCRIMS_TOKEN',token)

                with open(BASE_DIR+'/sessions/'+token,'w',encoding='utf-8') as f:
                     json = '[{"id":"'+str(a.init)+'","ip":"'+request.META.get('REMOTE_ADDR')+'"}]'
                     f.write(crypto.Encrypt(json))
                return resp

            else:
                return HttpResponse(status=404)
        else:
            return HttpResponse(status=404)
    else:
        if CheckAuth(request) == False:
            pass
        else:
            return redirect('/')

        return render(request,'auth.html',{'lang':LANG,'title':LANG[0]['auth'][0]['title']})










def FileUpload(request):

    user = CheckAuth(request)
    if user == False:
        return HttpResponse(status=403)

    file_add = request.FILES.get('file')

    images_type = ["jpg","JPG","gif","JPEG","png","PNG","tiff","GIF"]
    name = get_random_string(length=32)

    type_file = (os.path.splitext(file_add.name)[1]).replace(".",'')
    usr = User.objects.get(init=user[0]['id'])
    data=file_add.read()

    path = BASE_DIR+'/media/storage/'+str(date.today())+'/'
    url = '/media/storage/'+str(date.today())+'/'
    if not os.path.exists(path):
        os.makedirs(path)

    with open(path+name,'wb') as f:
        f.write(crypto.Encrypt(data))

    insert = Storage(user=usr,type_file=type_file,name=file_add.name,path=path,hash_name=name,date=datetime.now())
    insert.save()
    url = "/storage/"+str(insert.id)+"/"
    Storage.objects.filter(id=int(insert.id)).update(url=url)


    name_cache = ''
    if type_file in images_type:
        name_cache = get_random_string(length=32)
        size = 128, 128
        im = Image.open(file_add)
        im.thumbnail(size)
        im.save(BASE_DIR+"/media/storage/"+name+"."+im.format,format=im.format)
        name_cache = "/media/storage/"+name+"."+im.format
        Storage.objects.filter(pk=insert.id).update(cache=name)

    return HttpResponse(str('{"name":"'+file_add.name+'","types":"'+type_file+'","url":"'+url+'","cache":"'+name_cache+'"}'))











def StorageView(request,id):
    user = CheckAuth(request)
    if user == False:
        return HttpResponse(status=404)

    file_storage = Storage.objects.get(pk=id)

    with open(file_storage.path+file_storage.hash_name,'rb') as f:
        data = crypto.Decrypt(f.read())


    f_type = file_storage.type_file.replace('.','')
    images_type = ["jpg","JPG","gif","JPEG","png","PNG","tiff","GIF"]


    if f_type in images_type:
        return HttpResponse(data, content_type="image/"+file_storage.type_file.replace('.',''))
    elif f_type == 'pdf' or f_type == 'PDF':
        response = HttpResponse(content_type="application/"+file_storage.type_file.replace('.',''))
        response['Content-Disposition'] = 'attachment; filename=%s' % file_storage.name # force browser to download file
        response.write(data)
        return response
    else:
        response = HttpResponse(content_type="application/octet-stream")
        response['Content-Disposition'] = 'attachment; filename=%s' % file_storage.name # force browser to download file
        response.write(data)
        return response










def CheckAuth(request):
    try:
        check = os.path.exists(BASE_DIR+'/sessions/'+request.COOKIES['SCRIMS_TOKEN'])
        if check == True:
            f = open(BASE_DIR+'/sessions/'+request.COOKIES['SCRIMS_TOKEN'], encoding='utf-8')
            json_user = json.loads(crypto.Decrypt(f.read()))
            print(json_user,request.META.get('REMOTE_ADDR'))
            if json_user[0]['ip'] != request.META.get('REMOTE_ADDR'):
                return False
            else:
                pass

            return (json_user)
        else:
            return False
    except:
        return False



















def AuthForm(request):
    if CheckAuth(request) == False:
        pass
    else:
        return redirect('/')

    return render(request,'auth.html',{'lang':LANG,
                                       'title':LANG[0]['auth'][0]['title']
                                       })















def Main(request):
    user = CheckAuth(request)
    if user == False:
        return redirect('/auth/')


    #posts
    posts = Post.objects.all().order_by('-date')[:10]
    print(posts)


    user_data = User.objects.get(init=user[0]['id'])
    users = User.objects.all().exclude(init=user[0]['id']).order_by('-status')

    common_message = []
    ids = []
    for i in user_data.group.all():
        ids.append(i.id)

    group = Group.objects.filter(pk__in=ids) # получаем группы в которых состоит юзер

    group_mass = []
    for a in group:
        count = Message.objects.filter(group=a.init,reading_group=user_data).count()

        if count:
            common_message.append(count)

        group_mass.append({
            "search":a.name,
            "id":a.init,
            "name":a.name,
            "count_msg":count,
            "image":a.image,
            "status":True,
            #"users_group":
            #"last_msg":last_message,
            "public_key":a.public_key,
        })


    user_mass = []
    for a in users:
        count = Message.objects.filter(user=a.init,companion=user[0]['id'],reading=False).count()
        last_message = LastMessage.objects.filter(companion_1=a.init,companion_2=user[0]['id']) | LastMessage.objects.filter(companion_1=user[0]['id'],companion_2=a.init)

        if count:
            common_message.append(count)
        user_mass.append({
            "group":group,
            "search":a.name.split(" "),
            "id":a.init,
            "name":a.name,
            "count_msg":count,
            "image":a.image,
            "status":a.status,
            "last_msg":last_message,
            "public_key_user":a.public_key_user,
        })

    print(len(common_message))


    return render(request,"home.html",{'user':user_data,'users':user_mass,'lang':LANG,"group":group_mass,'common_message':len(common_message)})
    #return render(request,"react/react-home.html",{'user':user_data,'users':user_mass,'lang':str(LANG)})
