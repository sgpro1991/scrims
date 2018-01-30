from django.contrib import admin
from .models import User,Message,Storage
from main.views import Crypto
from django.utils.crypto import get_random_string
from sorl.thumbnail import get_thumbnail



class UserAdmin(admin.ModelAdmin):
    fields = ('image', 'image_tag','name','email','phone','position','subordinate','about','status')
    readonly_fields = ('image_tag',)
    def save_model(self, request, obj, form, change):

        obj.user = request.user
        if obj.id is None:
            password = get_random_string(length=6)
            crypt = Crypto().Encrypt(password)
        else:
            crypt = ''


        super().save_model(request, obj, form, change)
        if crypt != '':
            print(password)
            User.objects.filter(id=obj.id).update(password=crypt)





admin.site.register(Message)
admin.site.register(Storage)

admin.site.register(User,UserAdmin)

# Register your models here.
