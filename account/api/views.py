from email import message
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializer import LoginSerializer,LogoutSerializer
from django.contrib.auth import authenticate,login
import jwt
import datetime
from django.utils import timezone
from reg_org.models import Organization,UserPermissions,LoginHistory
import uuid
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import TokenError
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
@api_view(['POST'])
def login_view(request,org):
    try:
        if Organization.objects.filter(org_name=org).exists():
            client_secret=request.META.get('HTTP_CLIENT_SECRET')
            org=Organization.objects.get(client_secret=client_secret)
            # x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            # if x_forwarded_for:
            #     ip = x_forwarded_for.split(',')[0]
            # else:
            #     ip = request.META.get('REMOTE_ADDR')
            # print(ip)
            if org is None:
                return Response({"error":'Invalid secret Key'})  
            
            
            if request.method == 'POST':
                
                serializer=LoginSerializer(data=request.data)
                # print(serializer)
                if serializer.is_valid():
                    username=serializer.data['username']
                    password=serializer.data['password']
                    user=authenticate(username=username,password=password)
                    
                    if user is not None:
                        # as the user exist in the database , we now need to generate a jwt token 
                        # now i can decide what things i can give to encode the payload
                        refresh = RefreshToken.for_user(user)
                        
                                        
                        data={
                            'message':'Logged in sucessfully',
                            'access_token':str(refresh.access_token),
                            'refresh_token':str(refresh),
                            'username':user.username
                        }
                        LoginHistory.objects.create(org=org,login_user=username,status="success")
                        return Response(data)
                        
                    else:
                        
                        data={
                            'message':'Invalid credentials'
                            
                        }
                        LoginHistory.objects.create(org=org,login_user=username,status="failed",message="Invalid credentials")
                        
                        return Response(data=data,status=status.HTTP_403_FORBIDDEN)
                        
                else:
                    LoginHistory.objects.create(org=org,login_user=username,status="failed",message="Erros in Form")

                    return Response({'error':serializer.errors})
        else:
            return Response({'error':'Invalid URL'})
    except ValidationError as v:
        return Response({'errorTE':v.__cause__})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request,org):
    
    try:
        serializer =LogoutSerializer(data=request.data)

        if serializer.is_valid():
            
            # there is a custom save method in the serializer class
            serializer.save()
            
            return Response(status=status.HTTP_204_NO_CONTENT)
    except TokenError as e:
        return Response({'error':"Token BlackListed"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_permissions_view(request,org):
    
    try:
        user=User.objects.get(username=request.user)
        permObj=UserPermissions.objects.filter(emp=user)
        
        perms=[]
        
        for p in permObj:
            perms.append(p.perm_name.permission_name)
        print(perms)
        return Response({'permissions':perms})
    except :
        return Response({'error':"Internal Server Error"})