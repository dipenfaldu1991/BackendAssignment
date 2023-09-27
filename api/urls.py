
from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('post', views.PostViewSet)

app_name = 'api'
urlpatterns = [
    #Authentication
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),

    #Profile
    path('profile/', views.getProfile, name='profile'),
    path('profile/update/', views.updateProfile, name='update-profile'),
    path('follow/<int:pk>/', views.FollowUserView.as_view(), name='follow'),
    path('unfollow/<int:pk>/', views.UnfollowUserView.as_view(), name='unfollow'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
]