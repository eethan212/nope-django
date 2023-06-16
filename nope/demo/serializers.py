from rest_framework import serializers

from nope.demo.models import Teacher, Student


class SingleTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class SingleStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class StudentWithTeacherSerializer(serializers.ModelSerializer):
    teacher = SingleTeacherSerializer(many=False, required=False)

    class Meta:
        model = Student
        fields = '__all__'


class TeacherWithStudentSerializer(serializers.ModelSerializer):
    students = SingleStudentSerializer(many=True, required=False)

    class Meta:
        model = Teacher
        fields = '__all__'
