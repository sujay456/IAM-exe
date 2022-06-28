from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views


urlpatterns = [
    path('<str:org>/login/',views.login_view,name='servicelogin'),
    path('<str:org>/logout',views.logout_view,name='servicelogout'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('<str:org>/getperm/',views.get_permissions_view,name='get_perm')
]
