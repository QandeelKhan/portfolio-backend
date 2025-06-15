from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views
from rest_framework_nested import routers

urlpatterns = [
    path('user/register/', views.UserRegistrationView.as_view(), name='register'),
    path('user/login/', views.UserLoginView.as_view(), name='login'),
    path('user/logout/', views.LogoutView.as_view(), name='logout'),
    path('user/profile/', views.UserProfileView.as_view(), name='profile'),
    path('changepassword/', views.UserChangePasswordView.as_view(),
         name='changepassword'),
    path('send-reset-password-email/', views.SendPasswordResetEmailView.as_view(),
         name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', views.UserPasswordResetView.as_view(),
         name='reset-password'),
    path('user/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('user/token/refresh/',
         views.CustomTokenRefreshView.as_view(), name='token_refresh'),
    #     path('user/token/refresh/',
    #          TokenRefreshView.as_view(), name='token_refresh'),
]

# --------- using router of rest framework

# router = routers.DefaultRouter()
# user_router = routers.DefaultRouter()
# user_router.register(
#     'user/register', views.UserRegistrationViewSet, basename='register')
# user_router.register(
#     'user/login', views.UserLoginViewSet, basename='login')
# user_router.register(
#     'user/profile/', views.UserProfileViewSet, basename='profile'),
# user_router.register('changepassword/', views.UserChangePasswordViewSet,
#                      basename='changepassword'),
# user_router.register('send-reset-password-email/', views.SendPasswordResetEmailViewSet,
#                      basename='send-reset-password-email'),
# user_router.register('reset-password/<uid>/<token>/',
#                      views.UserPasswordResetViewSet, basename='reset-password'),
# user_router.register('logout/', views.LogoutViewSet, basename='logout'),

# urlpatterns = [
#     path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
# ] + user_router.urls
