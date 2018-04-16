from django.contrib import admin
from .models import User, Message, Storage, LastMessage, Group, Membership, Departament,Post
from main.views import Crypto
from django.utils.crypto import get_random_string
from sorl.thumbnail import get_thumbnail
import hashlib









class UserAdmin(admin.ModelAdmin):
    fields = ('init','group','image', 'image_tag','name','hash_password','email','phone','position','public_key_user','dep','subordinate','about','status')
    readonly_fields = ('image_tag',)
    search_fields = ('name',)
    def save_model(self, request, obj, form, change):

        obj.user = request.user
        if obj.id is None:
            password = get_random_string(length=11)
            init = get_random_string(length=32)
            publick_key = get_random_string(length=32)
            crypt = Crypto().Encrypt(password)
            hash_sha256 = hashlib.sha256(password.encode('utf-8'))
            print(hash_sha256.hexdigest())
        else:
            crypt = ''


        super().save_model(request, obj, form, change)
        if crypt != '':
            print(password)
            User.objects.filter(id=obj.id).update(init=init,password=crypt,hash_password=hash_sha256.hexdigest(),about=password,public_key_user=publick_key)

admin.site.register(Departament)
admin.site.register(Membership)
admin.site.register(LastMessage)
admin.site.register(Message)
admin.site.register(Storage)
admin.site.register(Post)
admin.site.register(User,UserAdmin)
admin.site.register(Group)
# Register your models here.
