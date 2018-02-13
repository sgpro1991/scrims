from django.db import models
from django.utils.html import mark_safe
from scrms.settings import MEDIA_URL


class User(models.Model):
    image = models.ImageField(upload_to='user/', blank=True, verbose_name='')
    name = models.CharField(max_length=100,blank=True)
    password = models.CharField(max_length=150)
    hash_password = models.CharField(max_length=150,blank=True)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, blank=True)
    position = models.CharField(max_length=255)
    subordinate = models.TextField(blank=True)
    about = models.TextField(blank=True)
    is_deleted = models.BooleanField(blank=True,default=False)
    status = models.BooleanField(blank=True,default=False)
    public_key_user = models.CharField(max_length=255, blank=True)
    def image_tag(self):
        return mark_safe('<img src='+MEDIA_URL+'%s style="max-width:200px" />' % (self.image))
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True



#class Storage(models.Model):
    #user = models.ForeignKey(User,on_delete=models.CASCADE)


class Message(models.Model):
    TYPE_CHOICES = (
        ('1', 'text'),
        ('2', 'file'),
        ('3', 'link'),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    companion = models.IntegerField(null=True)
    text = models.TextField()
    type_msg = models.CharField(choices=TYPE_CHOICES, max_length=255, default=False,blank=True)
    date = models.DateTimeField(null=True)
    delivered = models.BooleanField(default=False)
    reading = models.BooleanField(default=False)



class LastMessage(models.Model):
    companion_1 = models.IntegerField()
    companion_2 = models.IntegerField()
    text = models.TextField()
    id_msg = models.IntegerField()
    type_msg = models.CharField(max_length=10)




class Storage(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    type_file = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    hash_name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    date = models.DateTimeField(null=True)
    cache = models.CharField(max_length=255,null=True)
