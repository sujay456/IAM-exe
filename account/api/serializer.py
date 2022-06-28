
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken,TokenError

class LoginSerializer(serializers.Serializer):
    
    username=serializers.CharField(max_length=150)
    password=serializers.CharField(max_length=150)


class LogoutSerializer(serializers.Serializer):

    refresh=serializers.CharField()
    
    def validate(self,data):
        
        self.token=data['refresh']
        
        return data      
        
    def save(self,**kwargs):
            
        RefreshToken(self.token).blacklist()
        
        
        