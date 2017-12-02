# coding: utf-8
from django.db import models
from django.utils.timezone import now
from account.models import User
from DjangoUeditor.models import UEditorField
from problem.models import Problem
from group.models import Group
from jsonfield import JSONField


class Contest(models.Model):
    type_choices = (
        (1, '公开赛'),
        (2, '私有赛'),
        (3, '小组赛'),
        (4, '邀请赛-小组'),
        (5, '邀请赛-个人'),
        (6, '考试'),)
    title = models.CharField(max_length=30)
    description = UEditorField('description', height=100,
                               width=200, default=u'', blank=True,
                               imagePath="uploads/images/",
                               toolbars='besttome', filePath='uploads/files/')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    create_time = models.DateTimeField(auto_now_add=True)
    contest_type = models.IntegerField(choices=type_choices)
    password = models.CharField(max_length=20, blank=True)
    created_by = models.ForeignKey(User, related_name='create')
    groups = models.ManyToManyField(Group, blank=True)
    users = models.ManyToManyField(User, blank=True, related_name='users')
    visible = models.BooleanField(default=True)
    problems = models.ManyToManyField(Problem, through='ContestProblem')

    @property
    def status(self):
        if self.start_time > now():
            return -1
        elif self.end_time < now():
            return 0
        else:
            return 1

    class Meta:
        db_table = "contest"


class ContestProblem(models.Model):
    show_id = models.CharField(max_length=5, blank=True)
    all = models.IntegerField(default=0)
    ac = models.IntegerField(default=0)
    contest = models.ForeignKey(Contest)
    problem = models.ForeignKey(Problem)
    problems_status = JSONField(default={})

    class Meta:
        db_table = "contest_problem"


class ContestRank(models.Model):
    contest = models.ForeignKey(Contest)
    user = models.ForeignKey(User, blank=True, null=True)
    group = models.ForeignKey(Group, blank=True, null=True)
    problems_status = JSONField(default={})

    class Meta:
        db_table = "contest_rank"
