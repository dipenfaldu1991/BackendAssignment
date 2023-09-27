
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics,status,viewsets
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import User,Post
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from .serializer import MyTokenObtainPairSerializer, RegisterSerializer, ProfileSerializer,PostSerializer,LogoutSer,FollowSerializer
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSer
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        if (not request.user.id):
            return Response({'error': 'You are already loged out'})
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": 'Refresh token seccesfully blacklisted.'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": 'Refresh token alread blacklisted or invialid.'},
                            status=status.HTTP_400_BAD_REQUEST)


#api/profile  and api/profile/update
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfile(request):
    user = request.user
    serializer = ProfileSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateProfile(request):
    user = request.user
    serializer = ProfileSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = (IsAuthenticated)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FollowUserView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated)
    def put(self, request, *args, **kwargs):
        user_to_follow = self.get_object()
        user_profile = request.data['followers']

        if user_profile != user_to_follow and user_to_follow not in user_to_follow.followers.all():
            user_to_follow.followers.add(user_profile)
            user_to_follow.save()
            return Response({"message":"Follow successfully."},status=status.HTTP_204_NO_CONTENT)
        return Response({"message":"please select valid profile."},status=status.HTTP_400_BAD_REQUEST)



class UnfollowUserView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated)
    def put(self, request, *args, **kwargs):
        user_to_unfollow = self.get_object()
        user_profile = request.data['followers']
        if user_profile in [i.id for i in user_to_unfollow.followers.all()]:
            user_to_unfollow.followers.remove(user_profile)
            user_to_unfollow.save()
            return Response({"message":"Unfollow successfully."},status=status.HTTP_204_NO_CONTENT)
        return Response({"message":"please select valid profile."},status=status.HTTP_400_BAD_REQUEST)
