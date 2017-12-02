# coding: utf-8
from django import forms
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from solution.models import Solution
from problem.models import Problem
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import urllib
import urllib2
import json
import redis
import time

recon = redis.Redis(host='localhost', port=6379)


class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['title', 'description', 'input_description',
                  'output_description', 'input', 'output',
                  'hint', 'time_limit', 'memory_limit',
                  'visible', 'spj', 'source', 'difficulty', 'show_id']


def problemList(request):
    problemlist = Problem.objects.filter(visible=True)
    paginator = Paginator(problemlist, 25)

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'problem/problem.html', {'problems': contacts})


class SubmitForm(forms.Form):
    langChoices = (
        ('c', 'C'),
        ('g++', 'g++'),
        ('c++', 'c++'),
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
        ('js', 'js'),)
    lang = forms.ChoiceField(label='语言:', choices=langChoices)
    code = forms.CharField(label='代码:', widget=forms.Textarea)
    problem = forms.CharField(label='题号:', widget=forms.Textarea)


def problemDetail(request):
    if request.method == 'GET':
        if request.GET['id']:
            try:
                id = request.GET['id']
                problem = get_object_or_404(Problem, pk=id)
                form = SubmitForm()
                return render(request,
                              'problem/problemDetail.html',
                              {'form': form, 'problem': problem})
            except Exception:
                return HttpResponse('获取失败。')
    return HttpResponse('参数错误。')


def problemSolution(request):
    if request.method == 'GET':
        if request.GET['id']:
            flag = request.GET.get('contest')
            try:
                if flag:
                    id = request.GET['id']
                    solution = Solution.objects.filter(
                        contestproblem_id=id, user_id=request.user)[:8]
                    return render(request, 'solution/solutionshow.html',
                                  {'solutions': solution})
            except Exception:
                return HttpResponse('发生错误。')
            try:
                id = request.GET['id']
                solution = Solution.objects.filter(
                    problem_id_id=id, user_id=request.user)[:8]
                return render(request, 'solution/solutionshow.html',
                              {'solutions': solution})
            except Exception:
                return HttpResponse('请登录后查看。')
    return HttpResponse('参数错误。')


def timelim(user):
    now = time.time()
    last = recon.hget(str(user), 'lastsub')
    if last:
        if now - float(last) >= 1:
            recon.hset(str(user), 'lastsub', str(now))
            return True
        return False
    recon.hset(str(user), 'lastsub', str(now))
    return True


@login_required(login_url='/account/login/')
def problemSubmit(request):
    if request.method == 'POST':
        result = {}
        result['status'] = 'error'
        if not timelim(request.user.username):
            result['reason'] = u'提交速度过快，请稍后再尝试提交。'
            return HttpResponse(json.dumps(result))
        form = SubmitForm(request.POST)
        if form.is_valid():
            problem = \
                get_object_or_404(Problem,
                                  pk=int(form.cleaned_data['problem']))
            res = {'lang': form.cleaned_data['lang'],
                   'id': int(form.cleaned_data['problem']),
                   'timelim': problem.time_limit,
                   'memorylim': problem.memory_limit,
                   'code': form.cleaned_data['code']}
            submit = Solution(problem_id=problem, memory=0, runtime=0.0,
                              result='Waiting', languge=res['lang'],
                              code=res['code'], user_id=request.user)
            submit.save()
            res['sid'] = submit.solution_id
            res['type'] = 'ORD'
            post_data = urllib.urlencode(res).encode('utf-8')
            try:
                urllib2.urlopen("http://localhost:8888/", post_data, timeout=2)
            except Exception:
                result['reason'] = u'判题端未开启，请联系管理员。'
                return HttpResponse(json.dumps(result))
            result['status'] = 'ok'
            result['id'] = submit.solution_id
            return HttpResponse(json.dumps(result))
        result['reason'] = u'参数错误。'
        return HttpResponse(json.dumps(result))


def submitWaiting():
    solutions = Solution.objects.filter(result='Waiting')
    for solution in solutions:
        problem = solution.problem_id
        res = {'lang': solution.languge,
               'id': problem.id,
               'timelim': problem.time_limit,
               'memorylim': problem.memory_limit,
               'code': solution.code}
        res['sid'] = solution.solution_id
        res['type'] = 'ORD'
        post_data = urllib.urlencode(res).encode('utf-8')
        try:
            urllib2.urlopen("http://118.89.227.149:8888/",
                            post_data, timeout=2)
        except Exception:
            return False
    return True


'''
trysubmit = submitWaiting()
if trysubmit:
    print 'Try submit all waiting problem success.'
else:
    print 'Try submit all waiting problem fail.'
'''
