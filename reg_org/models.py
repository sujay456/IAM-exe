from email.policy import default
from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone


# Create your models here.

class Organization(models.Model):
    
    org_name=models.CharField(max_length=100,unique=True)
    
    num_of_users=models.IntegerField(default=0)
    
    head_user=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    
    client_secret=models.UUIDField(default=uuid.uuid4,editable=False)
    
    def __str__(self):
        
        return f"{self.org_name} - {self.head_user.username}"
    
class IsRoot(models.Model):
    is_root=models.BooleanField(default=False)
    
    user=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    
class PartOf(models.Model):
    
    org=models.ForeignKey(Organization, on_delete=models.CASCADE,null=True)
    
    emp=models.ForeignKey(User, on_delete=models.CASCADE,null=True) 
    

    
class Permissions(models.Model):
    org=models.ForeignKey(Organization, on_delete=models.CASCADE,null=True)
    
    permission_name=models.CharField(max_length=100)
    
    def __str__(self):
        return self.permission_name

class UserPermissions(models.Model):
    emp=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    
    perm_name=models.ForeignKey(Permissions, on_delete=models.CASCADE,null=True)
    
class LoginHistory(models.Model):
    org=models.ForeignKey(Organization, on_delete=models.CASCADE,null=True)
    
    login_time=models.DateTimeField(auto_now_add=True,null=True)  #auto now add can fill this field when it is created
    
    login_user=models.CharField(max_length=255,null=True)
    
    status=models.CharField(max_length=100,null=True,default="success")
    
    type=models.CharField(max_length=255,null=True)
    
    message=models.CharField(max_length=100,null=True,default="Ok")
    def __str__(self):
        
        return f"{self.login_time} {self.login_user} {self.status} {self.message} "

class RegisterHistory(models.Model):
    org=models.ForeignKey(Organization, on_delete=models.CASCADE,null=True)
    
    register_time=models.DateTimeField(auto_now_add=True,null=True)
    
    register_user=models.CharField(max_length=100)
    
    status=models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.org} {self.register_time} {self.register_user} {self.status}"