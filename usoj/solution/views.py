# coding: utf-8
from django.shortcuts import render
from solution.models import Solution

from django import forms
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json


class CodeForm(forms.Form):
    langChoices = (
        ('c', 'C'),
        ('g++', 'g++'),
        ('pascal', 'pascal'),
        ('javac', 'javac'),
        ('ruby', 'ruby'),
        ('chmod', 'chmod'),
        ('python', 'python'),
        ('php', 'php'),
        ('perl', 'perl'),
        ('gmcs', 'gmcs'),
        ('gcc', 'gcc'),
        ('fbc', 'fbc'),
        ('clang', 'clang'),
        ('clang++', 'clang++'),
        ('luac', 'luac'),
        ('js', 'js'))
    problemId = forms.CharField(label='题目:', max_length=10,
                                min_length=1)
    lang = forms.ChoiceField(label='语言:', choices=langChoices)
    code = forms.CharField(label='代码:', widget=forms.Textarea)


def solutionList(request):
    solutions = Solution.objects.filter(contest=None)
    paginator = Paginator(solutions, 25)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'solution/solution.html', {'solutions': contacts})


@login_required(login_url='/account/login/')
def mySolution(request):
    solutions = Solution.objects.filter(contest=None, user_id=request.user)
    paginator = Paginator(solutions, 25)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'solution/solution.html', {'solutions': contacts})


@login_required(login_url='/account/login/')
def getCode(request):
    if request.method == 'GET':
        if request.GET['id']:
            try:
                id = request.GET['id']
                sol = Solution.objects.get(solution_id=id,
                                           user_id=request.user)
                return HttpResponse(str(sol.code))
            except Exception:
                return HttpResponse('发生错误。')
    return HttpResponse('发生错误。')


@login_required(login_url='/account/login/')
def getStatus(request):
    if request.method == 'GET':
        if request.GET['id']:
            try:
                id = request.GET['id']
                sol = Solution.objects.get(solution_id=id,
                                           user_id=request.user)
                results = {}
                results['result'] = sol.result
                results['time'] = sol.runtime
                results['memory'] = sol.memory
                return HttpResponse(json.dumps(results))
            except Exception:
                return HttpResponse('ERROR')
    return HttpResponse('ERROR')
