from .models import Permissions
from django import forms
from django.contrib.auth.models import User

class RegisterationForm(forms.Form):
    
    username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Username'}))
    email = forms.EmailField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'email'}))
    organization = forms.CharField(label='Organization',max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Organization'}))
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput)

    password1.widget.attrs.update({'class': 'form-control'})
    password1.widget.attrs.update({'placeholder': 'Password'})
    
    password2.widget.attrs.update({'class': 'form-control'})
    password2.widget.attrs.update({'placeholder': 'confirm Password'})

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Username'}))
    password= forms.CharField(widget=forms.PasswordInput)
    
    password.widget.attrs.update({'class': 'form-control'})
    password.widget.attrs.update({'placeholder': 'Password'})
    

class EmployeeRegForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(EmployeeRegForm, self).__init__(*args, **kwargs)
        # from here onwareds we can create dynamic fields
        org=kwargs.pop('prefix')
        
        
        perms=Permissions.objects.filter(org=org)
        for p in perms:
            self.fields[p.permission_name]=forms.BooleanField(required=False)
    username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Username'}))
    email = forms.EmailField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'email'}))
    password= forms.CharField(widget=forms.PasswordInput)
    
    
    
    password.widget.attrs.update({'class': 'form-control'})
    password.widget.attrs.update({'placeholder': 'Password'})
    
    
class EmployeePermissionForm(forms.ModelForm):
    class Meta:
        model=Permissions
        fields="__all__"
class EmployeeUpdForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # from here onwareds we can create dynamic fields
        
        org=kwargs.pop('prefix')
        
        
        perms=Permissions.objects.filter(org=org)
        super(EmployeeUpdForm, self).__init__(*args, **kwargs)
        print(args, kwargs)
        for p in perms:
            self.fields[p.permission_name]=forms.BooleanField(required=False)
        
    username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Username'}))
    email = forms.EmailField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'email'}))
    
    
        
    

class PermissionRegisterForm(forms.Form):
    permission_name=forms.CharField(max_length=100)