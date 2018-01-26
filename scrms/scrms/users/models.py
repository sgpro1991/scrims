from django.db import models
from django.utils.html import mark_safe
from scrms.settings import MEDIA_URL


class User(models.Model):
    image = models.ImageField(upload_to='user/', blank=True, verbose_name='')
    name = models.CharField(max_length=100,blank=True)
    password = models.CharField(max_length=150,)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, blank=True)
    position = models.CharField(max_length=255)
    subordinate = models.TextField(blank=True)
    about = models.TextField(blank=True)
    delete = models.BooleanField(blank=True,default=False)
    def image_tag(self):
        return mark_safe('<img src='+MEDIA_URL+'%s style="max-width:200px" />' % (self.image))
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True



#class Storage(models.Model):
    #user = models.ForeignKey(User,on_delete=models.CASCADE)



from django.utils import timezone

class Message(models.Model):
    TYPE_CHOICES = (
        ('1', 'text'),
        ('2', 'img'),
        ('3', 'file'),
        ('4', 'link'),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    companion = models.IntegerField(null=True)
    text = models.TextField()
    type_msg = models.CharField(choices=TYPE_CHOICES, max_length=255, default=False,blank=True)
    date = models.DateTimeField(null=True)
    reading = models.BooleanField(default=False)
