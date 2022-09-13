from rest_framework import serializers
from .models import *
from django.contrib.auth.models import Group
  
class accountserializer(serializers.ModelSerializer):
    class Meta:
        model=account
        fields=('email', 'date_joined', 'is_superuser', 'groups')


class RegistrationUserSerializer(serializers.ModelSerializer):
    
    password2 = serializers.CharField(style={'input_type': 'password'},
                                      write_only=True)
    
    class Meta:
        model = account
        fields = ('email', 'password', 'password2')
        extra_kwargs = {
			'password': {'write_only': True}
		}
        
    def save(self, **kwargs):
        user = account(email=self.validated_data['email'])
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})

        user.set_password(password)
        user.save()
        
        group = Group.objects.get(name=kwargs['destinationGroup'])
        user.groups.add(group)
        
        return user