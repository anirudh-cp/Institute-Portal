from api.serializers import courseSerializer
from api.models import course
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

import sys

sys.path.append('../..')


class CourseSingleApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, course_code, *args, **kwargs):
        ''' List text for given requested user. '''

        if course.objects.filter(course_code=course_code).exists():
            data = course.objects.filter(course_code=course_code)
            serializer = courseSerializer(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response("", status=status.HTTP_404_NOT_FOUND)

    def put(self, request, course_code, *args, **kwargs):
        ''' Create/Update the record with given data. '''

        data = request.data

        if (int(data.dict()['wishNum']) < 10):
            return Response("Number of wishlist registrations lesser than 10, record ignored",
                            status=status.HTTP_400_BAD_REQUEST)

        if course.objects.filter(course_code=course_code).exists():
            record = course.objects.get(course_code=course_code)
            serializer = courseSerializer(record, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = courseSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, course_code, *args, **kwargs):
        """ Delete the record specified. """

        if course.objects.filter(course_code=course_code).exists():
            course.objects.filter(course_code=course_code).delete()
            return Response("", status=status.HTTP_200_OK)

        return Response("", status=status.HTTP_404_NOT_FOUND)


class CourseAllApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        ''' Get all records. '''

        if course.objects.exists():
            data = course.objects
            serializer = courseSerializer(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response("", status=status.HTTP_404_NOT_FOUND)


    def put(self, request, *args, **kwargs):
        ''' Create/Update the records in bulk with given data. '''
        
        data = request.data

        for row in data:
            if (int(row['wishNum']) < 10):
                continue

            if course.objects.filter(course_code=row["course_code"]).exists():
                record = course.objects.get(course_code=row["course_code"])
                serializer = courseSerializer(record, data=row, partial=True)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            else:
                serializer = courseSerializer(data=row)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response("", status=status.HTTP_200_OK)
