from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserViewSet, ResetPasswordAPIView, ResetPasswordConfirmAPIView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),

    #login/logout endpoints using JWT
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Password reset endpoints
    path('password-reset/', ResetPasswordAPIView.as_view(), name='password_reset'),
    path('password-reset-confirm/<str:uidb64>/<str:token>/', ResetPasswordConfirmAPIView.as_view(), name='password_reset_confirm'),
]