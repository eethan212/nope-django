from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from nope.demo.models import Teacher, Student
from nope.demo.serializers import (
    SingleTeacherSerializer,
    SingleStudentSerializer,
    TeacherWithStudentSerializer,
    StudentWithTeacherSerializer
)


class SingleTeacherViewSet(viewsets.ModelViewSet):
    """
    singleTeacher
    """
    queryset = Teacher.objects.all()
    serializer_class = SingleTeacherSerializer
    permission_classes = [AllowAny]


class TeacherWithStudentViewSet(viewsets.ModelViewSet):
    """
    TeacherWithStudent
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherWithStudentSerializer
    permission_classes = [AllowAny]


class SingleStudentViewSet(viewsets.ModelViewSet):
    """
    singleStudent
    """
    queryset = Student.objects.all()
    serializer_class = SingleStudentSerializer
    permission_classes = [AllowAny]


class StudentWithTeacherViewSet(viewsets.ModelViewSet):
    """
    StudentWithTeacher
    """
    queryset = Student.objects.all()
    serializer_class = StudentWithTeacherSerializer
    permission_classes = [AllowAny]
