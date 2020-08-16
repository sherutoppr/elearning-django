from rest_framework import generics
from ..models import Subject
from .serializers import SubjectSerializer

# for enrollment
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Course

# fro basic authentication
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

# viewset used for both to access all course or single courses
from rest_framework import viewsets
from .serializers import CourseSerializer

# to add additional action to viewset()
from rest_framework.decorators import action

# permission added
from .permissions import IsEnrolled
from .serializers import CourseWithContentsSerializer


# used for both course list and course detail
class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=True,         # action to be done on single objects
            methods=['post'],
            authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated])
    def enroll(self, request, *args, **kwargs):
        course = self.get_object()          # retrieve the courses objects
        course.students.add(request.user)   # enroll the student to that course
        return Response({'enrolled': True})

    @action(detail=True,      # action to be done for single objects
            methods=['get'],   # only for get request
            serializer_class=CourseWithContentsSerializer,
            authentication_classes=[BasicAuthentication],   # login type
            permission_classes=[IsAuthenticated, IsEnrolled])  # must be login and is_enrolled to see the content
    def contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


# class CourseEnrollView(APIView):
#     authentication_classes = (BasicAuthentication,)
#     permission_classes = (IsAuthenticated,)
#
#     def post(self, request, pk, format=None):             # only post request can access it(login required)
#         course = get_object_or_404(Course, pk=pk)  # retrieve course based on pk
#         course.students.add(request.user)
#         return Response({'enrolled': True})


class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
