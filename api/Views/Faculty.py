from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

import sys

sys.path.append('../..')

from api.models import faculty
from api.serializers import facultySerializer

class FacultySingleApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List single
    def get(self, request, emp_id, *args, **kwargs):
        ''' List text for given requested user. '''
        
        if faculty.objects.filter(emp_id=emp_id).exists():
            data = faculty.objects.filter(emp_id=emp_id)
            serializer = facultySerializer(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        return Response("", status=status.HTTP_404_NOT_FOUND)
        

    # 2. Create/Update
    def put(self, request, emp_id, *args, **kwargs):
        ''' Create/Update the record with given data. '''
        
        data = request.data
        print(data)
        if faculty.objects.filter(emp_id=emp_id).exists():
            record = faculty.objects.get(emp_id=emp_id)
            serializer = facultySerializer(record, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = facultySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, emp_id, *args, **kwargs):
        """ Delete the record specified. """
        
        if faculty.objects.filter(emp_id=emp_id).exists():
            faculty.objects.filter(emp_id=emp_id).delete()
            return Response("", status=status.HTTP_200_OK)
            
        return Response("", status=status.HTTP_404_NOT_FOUND)


class FacultyAllApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        ''' Get all records. '''
        
        if faculty.objects.exists():
            data = faculty.objects
            serializer = facultySerializer(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response("", status=status.HTTP_404_NOT_FOUND)
    
        