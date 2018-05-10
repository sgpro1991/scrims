from django.urls import  include,path
from users.models import Post,User,Likes
from rest_framework import routers, serializers, viewsets
from sorl_thumbnail_serializer.fields import HyperlinkedSorlImageField


class UserSerializer(serializers.ModelSerializer):
    image = HyperlinkedSorlImageField('50')
    class Meta:
        model = User
        fields = ('init','name','image')



class LikesSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Likes
        fields = ('user','post_init')

class ViewsSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Likes
        fields = ('user','post_init')



class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user','post_init')



# Serializers define the API representation.
class PostSerializer(serializers.ModelSerializer):
    likes = LikesSerializer(many=True)
    views = ViewsSerializer(many=True)
    creator = UserSerializer()
    class Meta:
        model = Post
        fields = ('creator', 'title', 'likes','views','text','comment','date')



# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register('users', UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('get-posts/', include(router.urls)),
]
