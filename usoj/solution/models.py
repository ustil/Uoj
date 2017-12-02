from django.db import models
from account.models import User
from problem.models import Problem
from contest.models import Contest, ContestProblem
from group.models import Group


class Solution(models.Model):
    solution_id = models.AutoField(primary_key=True)
    problem_id = models.ForeignKey(Problem, blank=True, null=True)
    user_id = models.ForeignKey(User, blank=True, null=True)
    group = models.ForeignKey(Group, blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True, blank=True)
    memory = models.IntegerField()
    runtime = models.FloatField()
    result = models.CharField(max_length=30)
    languge = models.CharField(max_length=30)
    # judger = models.CharField(max_length=16)
    code = models.TextField()
    error = models.TextField(blank=True)
    contest = models.ForeignKey(Contest, blank=True, null=True)
    contestproblem = models.ForeignKey(ContestProblem, blank=True, null=True)

    class Meta:
        db_table = "solution"
        ordering = ('-time',)

    def __str__(self):
        return self.solution_id


class TokenForm(models.Model):
    tokennum = models.CharField(max_length=10)
    creattime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "solution_token"


'''
class Sim(models.Model):
    s_id = models.IntegerField(primary_key=True)
    sim_s_id = models.IntegerField()
    sim = models.IntegerField()

    class Meta:
        db_table = "sim"
'''
