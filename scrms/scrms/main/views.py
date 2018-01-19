from django.shortcuts import render
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from scrms.settings import BASE_DIR,LANG
from users.models import User
# Create your views here.




class Crypto:
    from cryptography.fernet import Fernet
    from crypto.key import KEY
    def __init__(self,fernet=Fernet(KEY)):
        self.fernet = fernet

    def Encrypt(self,text):
        self.text = text
        return str(self.fernet.encrypt(bytes(self.text.encode('utf-8')))).replace('b','').replace("'","")

    def Decrypt(self,text):
        self.text = text
        return self.fernet.decrypt(self.text)







def Auth():
    print(BASE_DIR)





def AuthForm(request):
    email = request.POST.get('email',False)
    password = request.POST.get('password',False)
    if email and password:
    #    try:
    #        User
        return HttpResponse(2)
    else:
        return render(request,'auth.html',{'lang':LANG})



def Main(request):
    a = Crypto()

    print(a.Encrypt('21312312 312321321'))

    print(a.Decrypt(b'gAAAAABaYcE_p9Bsj5k57DstrxZ4A7gbW9GZxeKfcaTGIzovmfbAx9v7cU7xL_S8fV-SwJMg9wIWYaKfHje2j-KO3tTp6fhqVv3Ph_vM4I-QndRjngyHyVg='))

    #print(get_random_string(length=32))
    Auth()
    return HttpResponse(1)
