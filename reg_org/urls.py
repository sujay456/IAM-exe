from django.urls import path
from . import views


urlpatterns = [
    path('register',views.regOrgView,name='register'),
    path('login',views.loginView,name='login'),
    path('list',views.listView,name='list'),
    path('add_user',views.addUserView,name='add_user'),
    path('register_permission',views.registerPermissionView,name='register_permission'),
    path('logout',views.logoutView,name='logout'),
    path('detail/<int:pk>',views.empDetails,name='detail'),
]

