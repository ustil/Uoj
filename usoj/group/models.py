#coding: utf-8
from django.db import models
from account.models import User

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=15)
    member = models.ManyToManyField(User, through='GroupMember')
    type = models.IntegerField()

    # 1: 比赛队伍
    # 2: 交流队伍

    @property
    def members(self):
        return len(self.member.objects.all())

    def __str__(self):
        return '[' + str(self.type) + ']' + self.name
        
    class Meta:
        db_table = "group"
        
class GroupMember(models.Model):
    identity_choices = (
        ('M', '队员'),
        ('T', '老师'),
        ('L', '队长'),
        ('C', '创建人'),
        )
    identity = models.CharField(max_length=1, choices=identity_choices, default="M")
    account = models.ForeignKey(User)
    groups = models.ForeignKey(Group)
    
    def __str__(self):
        return '[' + self.groups.name + ' ' + self.identity + ']' + self.account.username
    
    class Meta:
        db_table = "group_member"

class Audit(models.Model):
    joinres = models.CharField(max_length=100, blank=True, null=True)
    rejectres = models.CharField(max_length=100, blank=True, null=True)
    account = models.ForeignKey(User)
    groups = models.ForeignKey(Group)
    
    def __str__(self):
        return '[' + self.groups.name + ']' + self.account.username
        
    class Meta:
        db_table = "group_audit"
