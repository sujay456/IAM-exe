from django.db import IntegrityError
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import LoginHistory, Organization,IsRoot,PartOf,Permissions,UserPermissions,RegisterHistory
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.
from .form import RegisterationForm,LoginForm,EmployeeRegForm,EmployeeUpdForm,PermissionRegisterForm,EmployeePermissionForm

from django.core.exceptions import ObjectDoesNotExist

from django.contrib import messages
import uuid
import re


# utility functions
def check_password_validity(password):
    reg="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    pat=re.compile(reg)
    print("hello from password")
    if re.search(pat,password):
        return True
    else:
        return False
        


def regOrgView(request):
    if request.user.is_authenticated:
        messages.error(request,"You are already logged in")
        return redirect(reverse('list'))
    if request.method == 'POST':
        form = RegisterationForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data["username"]
            p1=form.cleaned_data["password1"]
            p2=form.cleaned_data["password2"]
            email=form.cleaned_data['email']
            organization=form.cleaned_data["organization"]
            if User.objects.filter(username=username) or (p1!=p2) or Organization.objects.filter(org_name=organization):
                
                if p1!=p2:
                    messages.error(request,'Passwords do not match')
                else:
                    messages.error(request,'Either organization or username is registered already')
                return redirect(reverse('register'))            
            if check_password_validity(p1)==False:    
                messages.success(request,"Password must include capital letters ,special characters [@$!%*#?&] , numbers")
                return redirect(reverse('register'))
            user=User(username=username,email=email)
            user.set_password(p1)
            user.save()
            client_secret=uuid.uuid4()
            org=Organization(org_name=organization,num_of_users=0,head_user=user,client_secret=client_secret)
            org.save()
            
            IsRoot.objects.create(is_root=True,user=user)
            return redirect(reverse('login'))     
            
    else:
        form =RegisterationForm()
        
    return render(request,'reg_form.html',{'form':form})

def loginView(request):
    
    if request.user.is_authenticated:
        return redirect(reverse('list'))
    if request.method == 'POST':
        form=LoginForm(request.POST)
        
        if form.is_valid():
            # print(form.cleaned_data)
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            print(password)
            user=authenticate(username=username,password=password)
            
            if user is not None:
                isroot=IsRoot.objects.get(user=user)
                
                if isroot.is_root==False:
                    
                    messages.error(request,"Invalid root credentials")
                    
                    return redirect(reverse('login'))
                login(request,user)
                messages.success(request,"Logged in successfully")
                return redirect(reverse('list'))
            else:
                messages.error(request,"Invalid credentials provided")
                return redirect(reverse('login'))
            
    else:
        form=LoginForm()
    
    return render(request,'login.html',{'form':form})

@login_required
def listView(request):
    
    try:
        org=Organization.objects.get(head_user=request.user)
        usernamesearch=request.GET.get('username')
        
        if usernamesearch is not None:
            user=User.objects.get(username=usernamesearch)
            if user is not None:
                return redirect(reverse('detail', kwargs={'pk': user.pk}))
                                
        permissions=Permissions.objects.filter(org=org)
        all_emps=PartOf.objects.filter(org=org)
        num=all_emps.count()
        return render(request,'list_user.html',{'num_of_users':num,'emps':all_emps,'client_secret':org.client_secret,'permissions':permissions})
    
    except ObjectDoesNotExist:
        return render(request,'error.html',{'error':'data not found'})
    

@login_required
def empDetails(request,pk):
    
    try:
        user=User.objects.get(pk=pk)
        emp=PartOf.objects.get(emp=user)
        usernamesearch=request.GET.get('username')
        org=Organization.objects.get(head_user=request.user)
        userperms=UserPermissions.objects.filter(emp=user)
        perms=Permissions.objects.filter(org=org)
        if usernamesearch is not None:
            user=User.objects.get(username=usernamesearch)
            if user is not None:
                return redirect(reverse('detail', kwargs={'pk': user.pk}))
        if request.method == 'POST':
            
            form=EmployeeUpdForm(request.POST,prefix=org)
            
            if form.is_valid():
                username=form.cleaned_data['username']
                email=form.cleaned_data['email']
                
                
                user.username=username
                user.email=email
                user.save()
                dict={}
                for p in perms:
                    dict[p.permission_name]=False
                for p in userperms:
                    dict[p.perm_name.permission_name]=True
                    if form.cleaned_data[p.perm_name.permission_name]==False:
                        p.delete()
                
                for p in perms:
                    if dict[p.permission_name]:
                        continue
                    
                    if form.cleaned_data[p.permission_name]==True:
                        UserPermissions.objects.create(emp=user,perm_name=p)            
                
                messages.success(request,"changes updated successfully")
        data={'username':user.username,'email':user.email}
        
        for p in perms:
            data[p.permission_name]=False
        userperms=UserPermissions.objects.filter(emp=user)
        for p in userperms:
            data[p.perm_name.permission_name]=True
        form=EmployeeUpdForm(data,prefix=org)    
        
        return render(request,'empDetail.html',{'name':emp.emp.username,'org':emp.org.org_name,'form':form})
    except (IntegrityError,ObjectDoesNotExist) as e:
        return render(request,'error.html',{'error':'User does not exist'})

@login_required
def addUserView(request):
    try:
        org=Organization.objects.get(head_user=request.user)
        perms=Permissions.objects.filter(org=org)
        if request.method =='POST':
            form=EmployeeRegForm(request.POST,prefix=org)
            
            if form.is_valid():
                
                print(form.cleaned_data)
                username=form.cleaned_data['username']
                
                password=form.cleaned_data['password']
                
                if check_password_validity(password)==False:
                    
                    messages.success(request,"Password must include capital letters ,special characters [@$!%*#?&] , numbers")
                    return redirect(reverse('add_user'))
                email=form.cleaned_data['email']
                user=User.objects.create(username=username,email=email)
                
                IsRoot.objects.create(is_root=False,user=user)
                org.num_of_users+=1;
                org.save()
                
                PartOf.objects.create(org=org,emp=user)
                
                for p in perms:
                    if form.cleaned_data[p.permission_name]:
                        UserPermissions.objects.create(emp=user,perm_name=p)
                
                messages.success(request,"user created successfully")
                RegisterHistory.objects.create(org=org,register_user=username,status="OK")
                return redirect('list')
        else:
            form=EmployeeRegForm(prefix=org)
                
        # print(org.client_secret)
        return render(request,'add_user.html',{'form':form,'perms':perms})
    
    except ObjectDoesNotExist:
        return render(request,'error.html',{'error':'data not found'})
    except IntegrityError as e:
        return render(request,'error.html',{'error':'username already in use'})
    
@login_required
def loginLogView(request):
    
    try:
        org=Organization.objects.get(head_user=request.user)
        logs=LoginHistory.objects.filter(org=org)
        usernamesearch=request.GET.get('username')
        
        if usernamesearch is not None:
            user=User.objects.get(username=usernamesearch)
            if user is not None:
                return redirect(reverse('detail', kwargs={'pk': user.pk}))
        context_log=[]
        
        for l in logs:
            context_log.append({'org':l.org,'status':l.status,'time':l.login_time,'mssg':l.message,'user':l.login_user,'type':l.type})
        
        return render(request,'loginlog.html',{'logs':context_log})
        
    except ObjectDoesNotExist:
        return render(request,'error.html',{'error':'data not found'})
@login_required
def registerLogView(request):
    
    try:
        org=Organization.objects.get(head_user=request.user)
        logs=RegisterHistory.objects.filter(org=org)
        usernamesearch=request.GET.get('username')
        
        if usernamesearch is not None:
            user=User.objects.get(username=usernamesearch)
            if user is not None:
                return redirect(reverse('detail', kwargs={'pk': user.pk}))
        context_log=[]
        
        for l in logs:
            context_log.append({'org':l.org,'status':l.status,'time':l.register_time,'user':l.register_user})
        
        return render(request,'registerlog.html',{'logs':context_log})
        
    except ObjectDoesNotExist:
        return render(request,'error.html',{'error':'data not found'})
def registerPermissionView(request):
    
    try:
        org=Organization.objects.get(head_user=request.user)
        usernamesearch=request.GET.get('username')
        
        if usernamesearch is not None:
            user=User.objects.get(username=usernamesearch)
            if user is not None:
                return redirect(reverse('detail', kwargs={'pk': user.pk}))
        if request.method == 'POST':
            form=PermissionRegisterForm(request.POST)
            
            if form.is_valid():
                perm=Permissions.objects.create(org=org,permission_name=form.cleaned_data['permission_name'])
                print(perm)
                messages.success(request,f"Permission {perm.permission_name} added successfully")
            else:
                messages.error(request,"error in form")
        else:
            form=PermissionRegisterForm()
        
        return render(request,'add_permission.html',{'form':form})
    except ObjectDoesNotExist:
        return render(request,'error.html',{'error':'data not found'})

def homeView(request):
    # if request.user.is_authenticated:
    #     return redirect(reverse('list'))
    
    return render(request,'home.html')

def logoutView(request):
     
    try:
        
        logout(request)
        messages.success(request,"Logged out successfully")
        return redirect(reverse('login'))

    except ObjectDoesNotExist:
        return render(request,'error.html',{'error':'data not found'})

    
@login_required
def deletePermissionView(request,pk):
    
    try:
        org=Organization.objects.get(head_user=request.user)
        # user=User.objects.get(user=request.user.username)
        
        permission=Permissions.objects.get(pk=pk,org=org)
        
        permission.delete()
        
        return redirect(reverse('list'))
                        
    except Permissions.DoesNotExist:
        return render(request,'error.html',{'error':'Permission does not exist'})
    except Organization.DoesNotExist:
        return render(request,'error.html',{'error':'Organization not found'})
    
@login_required
def userDeletionView(request,pk):
    
    try:
        org=Organization.objects.get(head_user=request.user)
        user=User.objects.get(pk=pk)
        
        PartOf.objects.get(emp=user,org=org)
        
        user.delete()
        
        return redirect(reverse('list'))
        
    except Organization.DoesNotExist:
        return render(request,'error.html',{'error':'Organization not found'})
    except User.DoesNotExist:
        return render(request,'error.html',{'error':'Looks Like user does not exist'})
    except PartOf.DoesNotExist:
        return render(request,'error.html',{'error':'Permission denied'})