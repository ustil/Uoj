#coding: utf-8
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from DjangoUeditor.forms import UEditorField
from solution.models import Solution
from problem.models import Problem
from account.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import zipfile
import urllib, urllib2
import random
import os
import json
import redis
import time

recon = redis.Redis(host='localhost', port=6379)

class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['title', 'description', 'input_description', 'output_description', 'input', 'output', 'hint', 'time_limit', 'memory_limit', 'visible', 'spj', 'source', 'difficulty', 'show_id']

'''
@login_required(login_url='/account/login/')
def addProblem(request):
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            if "file" not in request.FILES:
                return HttpResponse(u"文件上传失败")
            f = request.FILES["file"]
            fileName = ' '.join(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', 10)).replace(' ','') + ".zip"
            tmp_zip = "/tmp/" + fileName
            try:
                with open(tmp_zip, "wb") as test_case_zip:
                    for chunk in f:
                        test_case_zip.write(chunk)
            except:
                return HttpResponse(u"上传失败")
            try:
                test_case_file = zipfile.ZipFile(tmp_zip, 'r')
            except Exception:
                return HttpResponse(u"解压失败")
            name_list = test_case_file.namelist()

            if len(name_list) == 0:
                return HttpResponse(u"压缩包内没有文件")

            if len(name_list) % 2 == 1:
                return HttpResponse(u"测试用例文件格式错误，文件数目为奇数")

            for index in range(1, len(name_list) / 2 + 1):
                if not (str(index) + ".in" in name_list and str(index) + ".out" in name_list):
                    return HttpResponse(u"测试用例文件格式错误，缺少" + str(index) + u".in/.out文件")
            
            if form.cleaned_data['time_limit'] > 10:
                return HttpResponse(u"测试时间是否太长了呢？")
                
            addProblem = Problem(title=form.cleaned_data['title'], \
                                description=form.cleaned_data['description'], \
                                input_description=form.cleaned_data['input_description'], \
                                output_description=form.cleaned_data['output_description'], \
                                input=form.cleaned_data['input'], \
                                output=form.cleaned_data['output'], \
                                hint=form.cleaned_data['hint'], \
                                time_limit=form.cleaned_data['time_limit'], \
                                memory_limit=form.cleaned_data['memory_limit'], \
                                visible=form.cleaned_data['visible'], \
                                spj=form.cleaned_data['spj'], \
                                source=form.cleaned_data['source'], \
                                difficulty=form.cleaned_data['difficulty'], \
                                show_id=form.cleaned_data['show_id'], \
                                created_by=request.user)
            addProblem.save()
            
            os.chdir('/home/problem/')
            os.system('mkdir ' + str(addProblem.id))
            os.system('cp ' + tmp_zip + ' /home/problem/' + str(addProblem.id))
            os.chdir('/home/problem/' + str(addProblem.id))
            with zipfile.ZipFile(fileName) as caseFile:
                caseFile.extractall()
            os.system('rm ' + fileName)
            return HttpResponseRedirect("/problem/")
        else:
            return render(request, 'addProblem.html', {'form': form})
            
    form = ProblemForm()

    return render(request, 'addProblem.html', {'form': form})

def editProblem(request, id):
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            problem = get_object_or_404(Problem, pk=id)
            if "file" in request.FILES:
                f = request.FILES["file"]
                fileName = ' '.join(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', 10)).replace(' ','') + ".zip"
                tmp_zip = "/tmp/" + fileName
                try:
                    with open(tmp_zip, "wb") as test_case_zip:
                        for chunk in f:
                            test_case_zip.write(chunk)
                except:
                    return HttpResponse(u"上传失败")
                try:
                    test_case_file = zipfile.ZipFile(tmp_zip, 'r')
                except Exception:
                    return HttpResponse(u"解压失败")
                name_list = test_case_file.namelist()

                if len(name_list) == 0:
                    return HttpResponse(u"压缩包内没有文件")

                if len(name_list) % 2 == 1:
                    return HttpResponse(u"测试用例文件格式错误，文件数目为奇数")

                for index in range(1, len(name_list) / 2 + 1):
                    if not (str(index) + ".in" in name_list and str(index) + ".out" in name_list):
                        return HttpResponse(u"测试用例文件格式错误，缺少" + str(index) + u".in/.out文件")
                
                os.chdir('/home/problem/')
                os.system('rm -rf ' + str(problem.id))
                os.system('mkdir ' + str(problem.id))
                os.system('cp ' + tmp_zip + ' /home/problem/' + str(problem.id))
                os.chdir('/home/problem/' + str(problem.id))
                with zipfile.ZipFile(fileName) as caseFile:
                    caseFile.extractall()
                os.system('rm ' + fileName)

            problem.title = form.cleaned_data['title']
            problem.description = form.cleaned_data['description']
            problem.input_description = form.cleaned_data['input_description']
            problem.output_description = form.cleaned_data['output_description']
            problem.input = form.cleaned_data['input']
            problem.output = form.cleaned_data['output']
            problem.hint = form.cleaned_data['hint']
            problem.time_limit = form.cleaned_data['time_limit']
            problem.memory_limit = form.cleaned_data['memory_limit']
            problem.visible = form.cleaned_data['visible']
            problem.spj = form.cleaned_data['spj']
            problem.source = form.cleaned_data['source']
            problem.difficulty = form.cleaned_data['difficulty']
            problem.show_id = form.cleaned_data['show_id']
            problem.save()
            return HttpResponseRedirect("/problem/")
        else:
            return render(request, 'addProblem.html', {'form': form})

    problem = get_object_or_404(Problem, pk=id)
    form = ProblemForm(instance=problem)

    return render(request, 'addProblem.html', {'form': form})

def updateXMl(request):
    if request.method == 'POST':
        if "file" in request.FILES:
            from xml.etree.ElementTree import parse
            
            try:
                doc = parse(request.FILES["file"])
                
                for item in doc.iterfind('item'):
                    title = item.findtext('title')
                    time_limit = item.findtext('time_limit')
                    memory_limit = item.findtext('memory_limit')
                    description = item.findtext('description')
                    input = item.findtext('input')
                    output = item.findtext('output')
                    sample_input = item.findtext('sample_input')
                    sample_output = item.findtext('sample_output')
                    hint = item.findtext('hint')
                    source = item.findtext('source')
                    spj = item.findtext('spj')
                    
                    addProblem = Problem(title=title, description=description, input_description=input, output_description=output, \
                                    input=sample_input, output=sample_output, hint=hint, time_limit=time_limit, memory_limit=memory_limit, \
                                    visible=False, spj=False, source=source, difficulty=1, show_id=1, created_by=request.user)
                    addProblem.save()
                    
                    os.chdir('/home/problem/')
                    os.system('rm -rf ' + str(addProblem.id))
                    os.system('mkdir ' + str(addProblem.id))
                    os.chdir('/home/problem/' + str(addProblem.id))
                    
                    index = 1
                    for each in item.iterfind('test_input'):
                        #print each.text
                        infile = open(str(index) + '.in', 'w')
                        infile.write(each.text)
                        infile.close()
                        index += 1
        
                    index = 1
                    for each in item.iterfind('test_output'):
                        #print each.text
                        outfile = open(str(index) + '.out', 'w')
                        outfile.write(each.text)
                        outfile.close()
                        index += 1

                return HttpResponseRedirect("/problem/")
            except:
                return HttpResponseRedirect("/")
        else:
            return render(request, 'updatefile.html')

    return render(request, 'updatefile.html')
'''

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
        ('js', 'js'),
        )
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
                return render(request, 'problem/problemDetail.html', {'form': form, 'problem': problem})
            except:
                return HttpResponse('获取失败。')
    return HttpResponse('参数错误。')

def problemSolution(request):
    if request.method == 'GET':
        if request.GET['id']:
            flag = request.GET.get('contest')
            try:
                if flag:
                    id = request.GET['id']
                    solution = Solution.objects.filter(contestproblem_id=id, user_id=request.user)[:8]
                    return render(request, 'solution/solutionshow.html', {'solutions': solution})
            except:
                return HttpResponse('发生错误。')
            try:
                id = request.GET['id']
                solution = Solution.objects.filter(problem_id_id=id, user_id=request.user)[:8]
                return render(request, 'solution/solutionshow.html', {'solutions': solution})
            except:
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
            problem = get_object_or_404(Problem, pk=int(form.cleaned_data['problem']))
            res = { 'lang' : form.cleaned_data['lang'], 'id' : int(form.cleaned_data['problem']), 'timelim' : problem.time_limit, 'memorylim' : problem.memory_limit, 'code' : form.cleaned_data['code']}
            submit = Solution(problem_id=problem, memory=0, runtime=0.0, result='Waiting', languge=res['lang'], code=res['code'], user_id=request.user)
            submit.save()
            res['sid'] = submit.solution_id
            res['type'] = 'ORD'
            post_data = urllib.urlencode(res).encode('utf-8')
            try:
                urllib2.urlopen("http://localhost:8888/", post_data, timeout=2)
            except:
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
        res = { 'lang' : solution.languge, 'id' : problem.id, 'timelim' : problem.time_limit, 'memorylim' : problem.memory_limit, 'code' : solution.code}
        res['sid'] = solution.solution_id
        res['type'] = 'ORD'
        post_data = urllib.urlencode(res).encode('utf-8')
        try:
            urllib2.urlopen("http://118.89.227.149:8888/", post_data, timeout=2)
        except:
            return False
    return True

#trysubmit = submitWaiting()
#if trysubmit:
#    print 'Try submit all waiting problem success.'
#else:
#    print 'Try submit all waiting problem fail.'
