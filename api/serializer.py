
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User,Post
from rest_framework.validators import UniqueValidator

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        # ...

        return token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'bio', 'cover_photo')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            bio=validated_data['bio'],
            cover_photo=validated_data['cover_photo']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class LogoutSer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=555)

    class Meta:
        fields = ['refresh_token']

class ProfileSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id','cover_photo','bio','email','followers','following']

    def get_followers(self, obj):
        if obj.id is not None:
            print(User.objects.filter(followers=obj.id))
            getfollowing = User.objects.filter(followers=obj.id)
            return len(getfollowing)
        return 0
    def get_following(self, obj):
        if obj.followers is not None:
            return len(obj.followers.all())
        return 0

class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for object author info"""

    class Meta:
        model = User
        fields = ('username', 'cover_photo','followers')



class PostSerializer(serializers.ModelSerializer):
    """Serializer for the post objects"""
    author = AuthorSerializer(read_only=True)
    image = serializers.ImageField(max_length=None, allow_empty_file=False)
    caption = serializers.CharField(max_length=255,allow_null=True,allow_blank=True)
    location = serializers.CharField(max_length=255,allow_null=True,allow_blank=True)
    class Meta:
        model = Post
        fields = ('id', 'author',  'image',
                  'caption', 'location')

class FollowSerializer(serializers.ModelSerializer):
    """Serializer for the post objects"""
    followers = AuthorSerializer(read_only=True)
    class Meta:
        model = User
        fields = ('id', 'followers',)