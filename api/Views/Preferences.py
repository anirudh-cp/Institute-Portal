from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

import sys

sys.path.append('../..')

from api.models import preference
from api.serializers import preferenceSerializer

class preferenceSingleApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List single
    def get(self, request, emp_id, *args, **kwargs):
        ''' List text for given requested user. '''
        
        if preference.objects.filter(emp_id=emp_id).exists():
            data = preference.objects.filter(emp_id=emp_id)
            serializer = preferenceSerializer(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        return Response("", status=status.HTTP_404_NOT_FOUND)
        

    # 2. Create/Update
    def put(self, request, emp_id, *args, **kwargs):
        ''' Create/Update the record with given data. '''
        
        data = request.data
        print(data)
        if preference.objects.filter(emp_id=emp_id).exists():
            record = preference.objects.get(emp_id=emp_id)
            serializer = preferenceSerializer(record, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = preferenceSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, emp_id, *args, **kwargs):
        """ Delete the record specified. """
        
        if preference.objects.filter(emp_id=emp_id).exists():
            preference.objects.filter(emp_id=emp_id).delete()
            return Response("", status=status.HTTP_200_OK)
            
        return Response("", status=status.HTTP_404_NOT_FOUND)


class preferenceAllApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        ''' Get all records. '''
        
        if preference.objects.exists():
            data = preference.objects
            serializer = preferenceSerializer(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response("", status=status.HTTP_404_NOT_FOUND)
    
        