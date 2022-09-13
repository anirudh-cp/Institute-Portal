from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

import sys

sys.path.append('../..')

from api.models import administrator
from api.serializers import adminstratorSerializer

class AdministratorSingleApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List single
    def get(self, request, admin_id, *args, **kwargs):
        ''' List text for given requested user. '''
        
        if administrator.objects.filter(admin_id=admin_id).exists():
            data = administrator.objects.filter(admin_id=admin_id)
            serializer = adminstratorSerializer(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        return Response("", status=status.HTTP_404_NOT_FOUND)
        

    # 2. Create/Update
    def put(self, request, admin_id, *args, **kwargs):
        ''' Create/Update the record with given data. '''
        
        data = request.data
        print(data)
        if administrator.objects.filter(admin_id=admin_id).exists():
            record = administrator.objects.get(admin_id=admin_id)
            serializer = adminstratorSerializer(record, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = adminstratorSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, admin_id, *args, **kwargs):
        """ Delete the record specified. """
        
        if administrator.objects.filter(admin_id=admin_id).exists():
            administrator.objects.filter(admin_id=admin_id).delete()
            return Response("", status=status.HTTP_200_OK)
            
        return Response("", status=status.HTTP_404_NOT_FOUND)


class AdministratorAllApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        ''' Get all records. '''
        
        if administrator.objects.exists():
            data = administrator.objects
            serializer = adminstratorSerializer(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response("", status=status.HTTP_404_NOT_FOUND)
    
        