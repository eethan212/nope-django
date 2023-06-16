from django.db import models


# Demo
class Teacher(models.Model):
    id = models.CharField(help_text='ID', max_length=128, primary_key=True)
    name = models.CharField(help_text='name', max_length=256, null=True, blank=True)
    del_flag = models.IntegerField(help_text='删除标识', null=True, blank=True)

    class Meta:
        db_table = 'teacher'
        verbose_name = 'teacher'
        verbose_name_plural = 'teacher'


class Student(models.Model):
    class State(models.TextChoices):
        PENDING = "0", "未开始"
        SUCCESS = "1", "成功"
        FAIL = "-1", "失败"

    id = models.CharField(help_text='ID', max_length=128, primary_key=True)
    name = models.CharField(help_text='name', max_length=256, null=True, blank=True)
    del_flag = models.IntegerField(help_text='删除标识', null=True, blank=True)
    description = models.TextField(help_text='描述', null=True, blank=True)
    state = models.CharField(help_text='训练状态', max_length=36, choices=State.choices, default=State.PENDING)
    user = models.ForeignKey('accounts.User', help_text='用户', on_delete=models.CASCADE, related_name='students')
    parent = models.ForeignKey('demo.Teacher', help_text='父', on_delete=models.CASCADE, related_name='students')

    class Meta:
        db_table = 'student'
        verbose_name = 'student'
        verbose_name_plural = 'student'
