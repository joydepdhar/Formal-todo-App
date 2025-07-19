from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # User registration
    path('register/', views.register_user, name='register'),

    # Profile
    path('profile/', views.get_user_profile, name='get-profile'),
    path('profile/update/', views.update_user_profile, name='update-profile'),

    # JWT Auth
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
