from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('',views.homeView,name='home'),
    path('register',views.regOrgView,name='register'),
    path('login',views.loginView,name='login'),
    path('list',views.listView,name='list'),
    path('add_user',views.addUserView,name='add_user'),
    path('register_permission',views.registerPermissionView,name='register_permission'),
    path('logout',views.logoutView,name='logout'),
    path('detail/<int:pk>',views.empDetails,name='detail'),
    path('loginlog',views.loginLogView,name='loginlog'),
    path('registerlog',views.registerLogView,name='registerlog'),
    path('deletePerm/<int:pk>',views.deletePermissionView,name='deletePerm'),
    path('deleteuser/<int:pk>',views.userDeletionView,name='deleteuser'),
]

