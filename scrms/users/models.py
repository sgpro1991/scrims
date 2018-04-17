from django.db import models
from django.utils.html import mark_safe
from scrms.settings import MEDIA_URL



class Group(models.Model):
    init =  models.CharField(max_length=32)
    admin = models.CharField(max_length=32)
    name = models.CharField(max_length=255, blank=True, unique=True)
    date_create = models.DateTimeField(null=True)
    image = models.ImageField(upload_to='group/', blank=True, verbose_name='')
    public_key = models.CharField(max_length=255, blank=True)
    #last _message =
    def __str__(self):              # __unicode__ on Python 2
        return self.name



class Departament(models.Model):
    name = models.CharField(max_length=255,blank=True)
    def __str__(self):              # __unicode__ on Python 2
        return self.name


class User(models.Model):
    init = models.CharField(max_length=32,blank=True)
    group = models.ManyToManyField(Group,blank=True)
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
    dep = models.ForeignKey(Departament,on_delete=models.CASCADE,blank=True,null=True)
    def image_tag(self):
        return mark_safe('<img src='+MEDIA_URL+'%s style="max-width:200px" />' % (self.image))
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True




class Membership(models.Model):
    group = models.CharField(max_length=32,blank=True)
    users = models.ManyToManyField(User,blank=True)






class Message(models.Model):
    TYPE_CHOICES = (
        ('1', 'text'),
        ('2', 'file'),
        ('3', 'link'),
    )
    group = models.CharField(max_length=32,blank=True)
    user = models.CharField(max_length=32,blank=True)
    companion = models.CharField(max_length=32,blank=True)
    text = models.TextField()
    img = models.CharField(max_length=255,null=True)
    type_msg = models.CharField(choices=TYPE_CHOICES, max_length=255, default=False,blank=True)
    date = models.DateTimeField(null=True)
    delivered = models.BooleanField(default=False)
    reading = models.BooleanField(default=False)
    reading_group = models.ManyToManyField(User,blank=True)
    crypting = models.BooleanField(default=False)



class LastMessage(models.Model):
    companion_1 = models.CharField(max_length=32,blank=True)
    companion_2 = models.CharField(max_length=32,blank=True)
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






class Likes(models.Model):
    TYPE_CHOICES = (
        ('1', 'post'),
        ('2', 'comment'),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    type_like = models.CharField(choices=TYPE_CHOICES, max_length=255, default=False,blank=True)
    post_likes = models.CharField(max_length=255)


class Views(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post_views = models.CharField(max_length=255)


class Comment(models.Model):
    creator = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    date = models.DateTimeField()


class Post(models.Model):
    creator = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    comment = models.ManyToManyField(Comment,blank=True)
    likes = models.ManyToManyField(Likes,blank=True)
    views = models.ManyToManyField(Views,blank=True)
    date = models.DateTimeField()
