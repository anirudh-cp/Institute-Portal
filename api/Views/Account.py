from requests import request
from api.models import account, administrator, faculty
from api.serializers import RegistrationUserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status

from rest_framework.authtoken.models import Token

import sys
sys.path.append('../..')


@api_view(['POST', ])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def registration_view(request):

    if request.method == 'POST':
        data = {}
        
        email = request.data.get('email', '0').lower()
        if validate_email(email) != None:
            data['error_message'] = 'That email is already in use.'
            data['response'] = 'Error'
            return Response(data, status=status.HTTP_409_CONFLICT)

        group = request.user.groups.values_list('name', flat=True)
        if not any(item in ('admin', ) for item in group):
            data['error_message'] = 'Cannot create new user unless  admin.'
            data['response'] = 'Error'
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

        serializer = RegistrationUserSerializer(data=request.data)

        if serializer.is_valid():
            account = serializer.save(destinationGroup=request.data['destinationGroup'])
            data['response'] = 'successfully registered new user.'
            data['email'] = account.email
            data['groups'] = list(account.groups.values_list('name', flat=True))
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data, status=status.HTTP_201_CREATED)


def validate_email(email):
    try:
        accountObj = account.objects.get(email=email)
    except account.DoesNotExist:
        return None
    
    if accountObj != None:
        return email


class ObtainAuthTokenView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        context = {}

        email = request.data.get('email')
        password = request.data.get('password')
        
        account = authenticate(email=email, password=password)
        if account:
            try:
                token = Token.objects.get(user=account)
            except Token.DoesNotExist:
                token = Token.objects.create(user=account)
            context['response'] = 'Successfully authenticated.'
            context['groups'] = list(account.groups.values_list('name', flat=True))
            context['email'] = account.email
            
            if len(context['groups']) == 0:    
                context['response'] = 'Error'
                context['error_message'] = 'Group not defined'
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
                
            
            if context['groups'][0] == 'faculty':
                try:
                    queryData = faculty.objects.get(user=account.email)
                    context['name'] = queryData.name
                    context['id'] = queryData.emp_id
                except faculty.DoesNotExist:
                    context['name'] = 'undefined'
                    
                    context['id'] = -1
            elif context['groups'][0] == 'admin':
                try:
                    queryData = administrator.objects.get(user=account.email)
                    context['name'] = queryData.name
                    context['id'] = queryData.admin_id
                except administrator.DoesNotExist:
                    context['name'] = 'undefined'
                    context['id'] = -1

            context['token'] = token.key
            return Response(context, status=status.HTTP_200_OK)
        else:
            context['response'] = 'Error'
            context['error_message'] = 'Invalid credentials'
            return Response(context, status=status.HTTP_404_NOT_FOUND)