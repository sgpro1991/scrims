from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from scrms.settings import BASE_DIR,LANG,MEDIA_ROOT,MEDIA_URL
from users.models import User,Storage
from django.utils.crypto import get_random_string
import os
import json
from datetime import datetime





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









def Auth(request):
    email = request.POST.get('email',False)
    password = request.POST.get('password',False)
    if email and password:
        if User.objects.filter(email=email).exists():
            a = User.objects.get(email=email)
            user_pass = Crypto().Decrypt(a.password)
            if user_pass == password:
                resp = HttpResponse(status=200)
                token = get_random_string(length=32)
                resp.set_cookie('SCRIMS_TOKEN',token)

                with open(BASE_DIR+'/sessions/'+token,'w',encoding='utf-8') as f:
                     json = '[{"id":"'+str(a.id)+'"}]'
                     f.write(Crypto().Encrypt(json))
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
    name = get_random_string(length=32)


    filename = MEDIA_ROOT+'storage/'+user[0]["id"]+'/'+name
    url = MEDIA_URL+'storage/'+user[0]["id"]+'/'+name

    name_file = file_add.name
    type_file = (os.path.splitext(file_add.name)[1])
    path_file = filename
    hash_name = name

    usr = User.objects.get(id=user[0]['id'])

    insert = Storage(user=usr,type_file=type_file,name=file_add.name,path=filename,hash_name=name,url=url,date=datetime.now())
    insert.save()

    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    with open(filename, 'wb+') as f:
        f.write(Crypto().Encrypt(file_add.read()))
    print(url)
    return HttpResponse(str('{"name":"'+file_add.name+'","url":"'+url+'"}'))









def StorageView(request,user,filename):
    user = CheckAuth(request)
    if user == False:
        return HttpResponse(status=404)


    file_storage = Storage.objects.get(hash_name=filename)
    with open(file_storage.path, 'r') as fp:
        data = (Crypto().Decrypt(bytes(fp.read().encode('utf-8'))))

    response = HttpResponse(content_type="application/"+file_storage.type_file.replace('.',''))
    response['Content-Disposition'] = 'attachment; filename=%s' % file_storage.name # force browser to download file
    response.write(data)

    return response












def CheckAuth(request):
    try:
        check = os.path.exists(BASE_DIR+'/sessions/'+request.COOKIES['SCRIMS_TOKEN'])
        if check == True:
            f = open(BASE_DIR+'/sessions/'+request.COOKIES['SCRIMS_TOKEN'], encoding='utf-8')
            json_user = json.loads(Crypto().Decrypt(f.read()))
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

    print(user[0]['id'])
    user_data = User.objects.get(pk=user[0]['id'])
    users = User.objects.all().exclude(pk=user[0]['id'])
    return render(request,"home.html",{'user':user_data,'users':users,'lang':LANG})
