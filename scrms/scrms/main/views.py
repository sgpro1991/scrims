from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from scrms.settings import BASE_DIR,LANG
from users.models import User
from django.utils.crypto import get_random_string
import os
import json





class Crypto:
    from cryptography.fernet import Fernet
    from crypto.key import KEY
    def __init__(self,fernet=Fernet(KEY)):
        self.fernet = fernet

    def Encrypt(self,text):
        self.text = text
        return str(self.fernet.encrypt(bytes(self.text.encode('utf-8')))).replace("b'",'').replace("'","")

    def Decrypt(self,text):
        self.text = text
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























def CheckAuth(request):
    try:
        check = os.path.exists(BASE_DIR+'/sessions/'+request.COOKIES['SCRIMS_TOKEN'])
        if check == True:
            f = open(BASE_DIR+'/sessions/'+request.COOKIES['SCRIMS_TOKEN'], encoding='utf-8')
            return (Crypto().Decrypt(f.read()))
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
    if CheckAuth(request) == False:
        return redirect('/auth/')
    else:
        user = CheckAuth(request)
    json_user = json.loads(user)
    user_data = User.objects.get(pk=json_user[0]['id'])
    users = User.objects.all()
    return render(request,"home.html",{'user':user_data,'users':users,'lang':LANG})
