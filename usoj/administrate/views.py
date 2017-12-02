# coding: utf-8
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.http import StreamingHttpResponse
from django.utils import timezone

from xml.etree.ElementTree import parse
from utils.decorators import power_required

from solution.models import Solution
from problem.models import Problem
from account.models import User
from contest.models import ContestProblem, Contest
from group.models import Group
from judger.models import Judger
from index.models import Notice

import urllib
import urllib2
import json
import random
import zipfile
import os


@power_required(redirect='/', powerneed=100)
def index(request):
    return render(request, 'manage/index.html', {})


@csrf_exempt
@power_required(redirect='/', powerneed=100)
def rejudge(request):
    if request.method == 'POST':
        retype = request.POST.get('type', 'solution')
        reid = request.POST.get('id', 0)
        result = {}
        if retype == 'solution':
            sol = Solution.objects.get(solution_id=reid)
            problem = sol.problem_id
            res = {'lang': sol.languge,
                   'id': problem.id,
                   'timelim': problem.time_limit,
                   'memorylim': problem.memory_limit,
                   'code': sol.code}
            res['sid'] = sol.solution_id
            res['type'] = 'ORD'
            post_data = urllib.urlencode(res).encode('utf-8')
            try:
                urllib2.urlopen("http://localhost:8888/", post_data, timeout=2)
            except Exception:
                result['reason'] = u'判题端未开启，请联系管理员。'
                return HttpResponse(json.dumps(result))
        elif retype == 'contestpro':
            problem = ContestProblem.objects.get(id=reid)
            sol = Solution.objects.filter(contestproblem=problem)
            problem = problem.problem
            for eachsol in sol:
                res = {'lang': eachsol.languge,
                       'id': problem.id,
                       'timelim': problem.time_limit,
                       'memorylim': problem.memory_limit,
                       'code': eachsol.code}
                res['sid'] = eachsol.solution_id
                res['type'] = 'ORD'
                post_data = urllib.urlencode(res).encode('utf-8')
                try:
                    urllib2.urlopen("http://localhost:8888/",
                                    post_data, timeout=2)
                except Exception:
                    result['reason'] = u'判题端未开启，请联系管理员。'
                    return HttpResponse(json.dumps(result))
        else:
            problem = Problem.objects.get(id=reid)
            sol = Solution.objects.filter(problem_id=problem)
            for eachsol in sol:
                res = {'lang': eachsol.languge,
                       'id': problem.id,
                       'timelim': problem.time_limit,
                       'memorylim': problem.memory_limit,
                       'code': eachsol.code}
                res['sid'] = eachsol.solution_id
                res['type'] = 'ORD'
                post_data = urllib.urlencode(res).encode('utf-8')
                try:
                    urllib2.urlopen("http://localhost:8888/",
                                    post_data, timeout=2)
                except Exception:
                    result['reason'] = u'判题端未开启，请联系管理员。'
                    return HttpResponse(json.dumps(result))
        result['reason'] = u'提交成功。'
        return HttpResponse(json.dumps(result))

    return render(request, 'manage/rejudge.html', {})


@power_required(redirect='/', powerneed=100)
def showProblem(request):
    problems = Problem.objects.all()
    return render(request, 'manage/showproblem.html',
                  {'problems': problems})


@power_required(redirect='/', powerneed=100)
def showContest(request):
    contests = Contest.objects.all()
    problem = Problem.objects.values('id', 'title')
    user = User.objects.values('id', 'username')
    group = Group.objects.values('id', 'name')

    return render(request, 'manage/showcontest.html',
                  {'contests': contests,
                   'problems': problem,
                   'users': user,
                   'groups': group})


@power_required(redirect='/', powerneed=100)
def showNotice(request):
    notices = Notice.objects.all()
    return render(request, 'manage/shownotice.html',
                  {'notices': notices})


@power_required(redirect='/', powerneed=100)
def showJudger(request):
    judgers = Judger.objects.all()
    return render(request, 'manage/showjudger.html',
                  {'judgers': judgers})


@power_required(redirect='/', powerneed=100)
def showAccount(request):
    users = User.objects.all()
    return render(request, 'manage/showaccount.html',
                  {'users': users})


@power_required(redirect='/', powerneed=100)
def showGroup(request):
    return render(request, 'manage/showgroup.html', {})


@csrf_exempt
@power_required(redirect='/', powerneed=100)
def addProblem(request):
    if request.method == 'POST':
        id = request.POST.get('id', None)
        if not id:
            if "file" not in request.FILES:
                return HttpResponse(u"测试用例文件上传失败")
            f = request.FILES["file"]
            fileName = ' '.join(
                random.sample('abcdefghijklmnopqrstuvwxyzA' +
                              'BCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
                              10)).replace(' ', '') + ".zip"
            tmp_zip = "/tmp/" + fileName
            try:
                with open(tmp_zip, "wb") as test_case_zip:
                    for chunk in f:
                        test_case_zip.write(chunk)
            except Exception:
                return HttpResponse(u"测试用例上传失败")
            try:
                test_case_file = zipfile.ZipFile(tmp_zip, 'r')
            except Exception:
                return HttpResponse(u"测试用例解压失败")
            name_list = test_case_file.namelist()

            if len(name_list) == 0:
                return HttpResponse(u"压缩包内没有文件")

            if len(name_list) % 2 == 1:
                return HttpResponse(u"测试用例文件格式错误，文件数目为奇数")

            for index in range(1, len(name_list) / 2 + 1):
                if not (str(index) + ".in" in name_list and
                        str(index) + ".out" in name_list):
                    return HttpResponse(
                        u"测试用例文件格式错误，缺少" + str(index) + u".in/.out文件")

            problem = Problem()
            problem.title = \
                request.POST.get('title', 'No Title') \
                if request.POST.get('title', 'No Title') != "" else 'No Title'
            problem.description = \
                request.POST.get('description',
                                 "Description empty.") \
                if request.POST.get('description',
                                    "Description empty.") != "" else \
                'Description empty.'
            problem.input_description = \
                request.POST.get('input_description', "")
            problem.output_description = \
                request.POST.get('output_description', "")
            problem.input = request.POST.get('input', "")
            problem.output = request.POST.get('output', "")
            problem.hint = request.POST.get('hint', "")
            problem.time_limit = \
                request.POST.get('time_limit', 1) \
                if request.POST.get('time_limit', 1) != "" else 1
            problem.memory_limit = \
                request.POST.get('memory_limit', 128) \
                if request.POST.get('memory_limit', 128) != "" else 128
            problem.source = request.POST.get('source', "")
            problem.difficulty = \
                request.POST.get('difficulty', 0) \
                if request.POST.get('difficulty', 0) != "" else 1
            problem.created_by = request.user
            problem.save()

            os.chdir('/home/problem/')
            os.system('mkdir ' + str(problem.id))
            os.system('cp ' + tmp_zip + ' /home/problem/' + str(problem.id))
            os.chdir('/home/problem/' + str(problem.id))
            with zipfile.ZipFile(fileName) as caseFile:
                caseFile.extractall()
            os.system('rm ' + fileName)

            return HttpResponse(u"添加成功。")
        else:
            if "file" in request.FILES:
                f = request.FILES["file"]
                fileName = ' '.join(random.sample('abcdefghijklmnopqrst' +
                                                  'uvwxyzABCDEFGHIJKLMN' +
                                                  'OPQRSTUVWXYZ0123456789',
                                                  10)).replace(' ',
                                                               '') + ".zip"
                tmp_zip = "/tmp/" + fileName
                try:
                    with open(tmp_zip, "wb") as test_case_zip:
                        for chunk in f:
                            test_case_zip.write(chunk)
                except Exception:
                    return HttpResponse(u"测试用例上传失败")
                try:
                    test_case_file = zipfile.ZipFile(tmp_zip, 'r')
                except Exception:
                    return HttpResponse(u"测试用例解压失败")
                name_list = test_case_file.namelist()

                if len(name_list) == 0:
                    return HttpResponse(u"测试用例压缩包内没有文件")

                if len(name_list) % 2 == 1:
                    return HttpResponse(u"测试用例文件格式错误，文件数目为奇数")

                for index in range(1, len(name_list) / 2 + 1):
                    if not (str(index) + ".in" in name_list and
                            str(index) + ".out" in name_list):
                        return HttpResponse(
                            u"测试用例文件格式错误，缺少" + str(index) + u".in/.out文件")

                os.chdir('/home/problem/')
                os.system('rm -rf ' + str(problem.id))
                os.system('mkdir ' + str(problem.id))
                os.system('cp ' + tmp_zip +
                          ' /home/problem/' + str(problem.id))
                os.chdir('/home/problem/' + str(problem.id))
                with zipfile.ZipFile(fileName) as caseFile:
                    caseFile.extractall()
                os.system('rm ' + fileName)

            problem = Problem.objects.get(pk=id)
            problem.title = \
                request.POST.get('title', problem.title) \
                if request.POST.get('title', problem.title) != "" else \
                problem.title
            problem.description = \
                request.POST.get('description', problem.description)
            problem.input_description = \
                request.POST.get('input_description',
                                 problem.input_description)
            problem.output_description = \
                request.POST.get('output_description',
                                 problem.output_description)
            problem.input = request.POST.get('input', problem.input)
            problem.output = request.POST.get('output', problem.output)
            problem.hint = request.POST.get('hint', problem.hint)
            problem.time_limit = \
                request.POST.get('time_limit', 1) \
                if request.POST.get('time_limit', 1) != "" else \
                problem.time_limit
            problem.memory_limit = \
                request.POST.get('memory_limit', 128) \
                if request.POST.get('memory_limit', 128) != "" else \
                problem.time_limit
            problem.source = request.POST.get('source', "")
            problem.difficulty = \
                request.POST.get('difficulty', 0) \
                if request.POST.get('difficulty', 0) != "" else \
                problem.time_limit

            problem.save()

            return HttpResponse(u"修改成功。")

    return HttpResponse(u"please use post.")


'''
@power_required(redirect='/', powerneed=100)
def addxmlProblem(request):
    return render(request, 'manage/addxmlproblem.html', {})
'''


@csrf_exempt
@power_required(redirect='/', powerneed=100)
def addContest(request):
    if request.method == 'POST':
        id = request.POST.get('id', None)
        if not id:
            contest = Contest()
            contest.title = \
                request.POST.get('title', 'No Title') \
                if request.POST.get('title', 'No Title') != "" else 'No Title'
            contest.description = \
                request.POST.get('description', "Description empty.")
            contest.start_time = \
                request.POST.get('start_time', timezone.now()) \
                if request.POST.get('start_time', timezone.now()) != "" \
                else timezone.now()
            contest.end_time = \
                request.POST.get('end_time', timezone.now()) \
                if request.POST.get('end_time', timezone.now()) != "" \
                else timezone.now()
            contest.contest_type = \
                request.POST.get('contest_type', "1") \
                if request.POST.get('contest_type', "1") != "" else 1
            contest.password = request.POST.get('password', "")
            contest.created_by = request.user
            contest.save()

            problem = request.POST.get('problems', "").strip().split(',')
            user = request.POST.get('users', "").strip().split(',')
            group = request.POST.get('groups', "").strip().split(',')
            showid = 1
            for each in problem:
                if each:
                    add = ContestProblem(show_id=str(showid),
                                         contest=contest,
                                         problem=Problem.objects.get(id=each))
                    add.save()
                    showid += 1
            for each in user:
                if each:
                    add = User.objects.get(pk=int(each))
                    contest.users.add(add)
            for each in group:
                if each:
                    add = Group.objects.get(pk=int(each))
                    contest.groups.add(add)
            contest.save()

            return HttpResponse(u"添加成功。")
        else:
            contest = Contest.objects.get(pk=id)
            contest.title = \
                request.POST.get('title', contest.title) \
                if request.POST.get('title', 'No Title') != "" else 'No Title'
            contest.description = \
                request.POST.get('description', contest.description)
            contest.start_time = \
                request.POST.get('start_time', contest.start_time) \
                if request.POST.get('start_time', timezone.now()) != "" else \
                timezone.now()
            contest.end_time = \
                request.POST.get('end_time', contest.end_time) \
                if request.POST.get('end_time', timezone.now()) != "" else \
                timezone.now()
            contest.contest_type = \
                request.POST.get('contest_type', contest.contest_type) \
                if request.POST.get('contest_type', "1") != "" else 1
            contest.password = \
                request.POST.get('password', contest.password)
            contest.save()

            for each in contest.users.all():
                contest.users.remove(each)
            for each in contest.groups.all():
                contest.groups.remove(each)
            problem = request.POST.get('problems', "").strip().split(',')
            user = request.POST.get('users', "").strip().split(',')
            group = request.POST.get('groups', "").strip().split(',')
            showid = 1

            old = ContestProblem.objects.filter(contest=contest)
            for each in old:
                if str(each.problem.id) in problem:
                    problem.remove(str(each.problem.id))
                else:
                    each.delete()
            for each in problem:
                if each:
                    add = ContestProblem(
                        show_id=0, contest=contest,
                        problem=Problem.objects.get(id=int(each)))
                    add.save()
            now = ContestProblem.objects.filter(contest=contest)
            for each in now:
                each.show_id = showid
                each.save()
                showid += 1
            for each in user:
                if each:
                    add = User.objects.get(pk=int(each))
                    contest.users.add(add)
            for each in group:
                if each:
                    add = Group.objects.get(pk=int(each))
                    contest.groups.add(add)
            contest.save()

            return HttpResponse(u"修改成功。")

    return HttpResponse(u"please use post.")


@power_required(redirect='/', powerneed=100)
def addNotice(request):
    return render(request, 'manage/addnotice.html', {})


@csrf_exempt
@power_required(redirect='/', powerneed=100)
def addAccount(request):
    if request.method == 'POST':
        id = request.POST.get('id', None)
        user = User.objects.get(pk=id)
        user.real_name = \
            request.POST.get('realname', "") \
            if request.POST.get('realname', "") != "" else user.real_name
        user.admin_type = \
            request.POST.get('admin_type', 0) \
            if request.POST.get('admin_type', "1") != "" else 0
        if request.POST.get('password', "") != "":
            user.set_password(request.POST.get('password', ""))
        user.save()
        return HttpResponse(u"修改成功。")
    return HttpResponse(u"please use post.")


@csrf_exempt
@power_required(redirect='/', powerneed=100)
def addJudger(request):
    if request.method == 'POST':
        remote = False if request.POST.get('remote', None) else True
        newjudger = Judger(max=request.POST.get('max', 4),
                           ip=request.POST.get('ip', '0.0.0.0'),
                           port=request.POST.get('port', 8888),
                           remote=remote, token=request.POST.get('token', ''))
        newjudger.save()
        return HttpResponseRedirect("/manage/judger/")

    return render(request, 'manage/addjudger.html',
                  {'action': 'add'})


@csrf_exempt
@power_required(redirect='/', powerneed=100)
def editProblem(request):
    if request.method == 'POST':
        json_ = {}
        id = request.POST.get('id', None)
        problem = Problem.objects.get(id=id)
        json_['title'] = problem.title
        json_['description'] = problem.description
        json_['input_description'] = problem.input_description
        json_['output_description'] = problem.output_description
        json_['input'] = problem.input
        json_['output'] = problem.output
        json_['hint'] = problem.hint
        json_['time_limit'] = problem.time_limit
        json_['memory_limit'] = problem.memory_limit
        json_['source'] = problem.source
        json_['difficulty'] = problem.difficulty
        json_['id'] = id
        return HttpResponse(json.dumps(json_), content_type="application/json")
    return HttpResponse('Error')


@csrf_exempt
@power_required(redirect='/', powerneed=100)
def editContest(request):
    if request.method == 'POST':
        json_ = {}
        id = request.POST.get('id', None)
        contest = Contest.objects.get(id=id)
        json_['title'] = contest.title
        json_['description'] = contest.description
        json_['start_time'] = contest.start_time.strftime("%Y-%m-%d %H:%I")
        json_['end_time'] = contest.end_time.strftime("%Y-%m-%d %H:%I")
        json_['password'] = contest.password
        json_['contest_type'] = contest.contest_type
        json_['id'] = id
        json_['problem'] = ""
        for each in ContestProblem.objects.filter(contest_id=id):
            json_['problem'] += str(each.problem.id) + ','
        json_['problem'] = json_['problem'][:-1]
        json_['user'] = ""
        for each in contest.users.all():
            json_['user'] += str(each.id) + ','
        json_['user'] = json_['user'][:-1]
        json_['group'] = ""
        for each in contest.groups.all():
            json_['group'] += str(each.id) + ','
        json_['group'] = json_['group'][:-1]
        return HttpResponse(json.dumps(json_), content_type="application/json")
    return HttpResponse('Error')


@power_required(redirect='/', powerneed=100)
def editNotice(request):
    return render(request, 'manage/editnotice.html', {})


@csrf_exempt
@power_required(redirect='/', powerneed=100)
def editJudger(request):
    if request.method == 'POST':
        editid = request.POST.get('remote', None)
        remote = True if request.POST.get('remote', None) == 1 else False
        editjudger = Judger.objects.get(id=request.POST.get('id', 1))
        editjudger.max = request.POST.get('max', 4)
        editjudger.ip = request.POST.get('ip', '0.0.0.0')
        editjudger.port = request.POST.get('port', 8888)
        editjudger.remote = remote
        editjudger.topken = request.POST.get('token', '')
        editjudger.save()
        return HttpResponseRedirect("/manage/judger/")

    editid = request.GET.get('id', 1)
    editjudger = Judger.objects.get(id=editid)

    remote = 1 if editjudger.remote is True else 0
    return render(request, 'manage/addjudger.html',
                  {'action': 'edit',
                   'max': editjudger.max,
                   'ip': editjudger.ip,
                   'port': editjudger.port,
                   'remote': remote,
                   'token': editjudger.token,
                   'id': editid})


@csrf_exempt
@power_required(redirect='/', powerneed=100)
def editAccount(request):
    if request.method == 'POST':
        json_ = {}
        id = request.POST.get('id', None)
        user = User.objects.get(pk=id)
        json_['username'] = user.username
        json_['id'] = id
        json_['realname'] = user.real_name
        json_['admin_type'] = user.admin_type
        json_['password'] = ""
        return HttpResponse(json.dumps(json_), content_type="application/json")
    return HttpResponse('Error')


def editGroup(request):
    return render(request, 'manage/editgroup.html', {})


@power_required(redirect='/', powerneed=100)
def rmProblem(request):
    rmid = request.GET.get('id', None)
    try:
        rmproblem = Problem.objects.get(id=rmid)
        rmproblem.delete()
    except Exception:
        return HttpResponse(u"删除失败。")
    try:
        os.chdir('/home/problem/')
        os.system('rm -rf ' + str(rmid))
    except Exception:
        pass
    return HttpResponse(u"删除成功。")


@csrf_exempt
@power_required(redirect='/', powerneed=100)
def rmContest(request):
    rmid = request.GET.get('id', None)
    try:
        rmcontest = Contest.objects.get(id=rmid)
        rmcontest.delete()
    except Exception:
        return HttpResponse(u"删除失败。")
    return HttpResponse(u"删除成功。")


@power_required(redirect='/', powerneed=100)
def rmNotice(request):
    rmid = request.GET.get('id', None)
    try:
        rmproblem = Problem.objects.get(id=rmid)
        rmproblem.delete()
    except Exception:
        return HttpResponse(u"删除失败。")
    return HttpResponse(u"删除成功，请刷新页面。")


@power_required(redirect='/', powerneed=100)
def rmJudger(request):
    rmid = request.GET.get('id', None)
    try:
        rmjudger = Judger.objects.get(id=rmid)
        rmjudger.delete()
    except Exception:
        return HttpResponse(u"删除失败。")
    return HttpResponse(u"删除成功，请刷新页面。")


@power_required(redirect='/', powerneed=100)
def rmGroup(request):
    return render(request, 'manage/rmgroup.html', {})


@power_required(redirect='/', powerneed=100)
def downloadtest(request):
    id = request.GET.get('id', None)
    newzip = zipfile.ZipFile('/tmp/test.zip', 'w')
    for dirpath, dirnames, filenames in \
            os.walk('/home/problem/' + str(id) + '/'):
        for filename in filenames:
            newzip.write(os.path.join(dirpath, filename))
    # newzip.write('/home/problem/'+str(id)+'/')
    newzip.close()

    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    the_file_name = "/tmp/test.zip"
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = \
        'attachment;filename="{0}"'.format(the_file_name)
    return response


@power_required(redirect='/', powerneed=100)
def changeshow(request):
    id = request.GET.get('id', None)
    problem = Problem.objects.get(id=id)
    visible = problem.visible
    if visible is True:
        problem.visible = False
    else:
        problem.visible = True
    problem.save()
    return HttpResponseRedirect('/manage/problem/')


@csrf_exempt
@power_required(redirect='/', powerneed=100)
def addxmlProblem(request):
    if request.method == 'POST':
        if "file" in request.FILES:
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
                    # spj = item.findtext('spj')

                    addProblem = Problem(title=title, description=description,
                                         input_description=input,
                                         output_description=output,
                                         input=sample_input,
                                         output=sample_output,
                                         hint=hint, time_limit=time_limit,
                                         memory_limit=memory_limit,
                                         visible=False, spj=False,
                                         source=source, difficulty=0,
                                         show_id=1, created_by=request.user)
                    addProblem.save()

                    os.chdir('/home/problem/')
                    os.system('rm -rf ' + str(addProblem.id))
                    os.system('mkdir ' + str(addProblem.id))
                    os.chdir('/home/problem/' + str(addProblem.id))

                    index = 1
                    for each in item.iterfind('test_input'):
                        infile = open(str(index) + '.in', 'w')
                        infile.write(str(each.text))
                        infile.close()
                        index += 1

                    index = 1
                    for each in item.iterfind('test_output'):
                        outfile = open(str(index) + '.out', 'w')
                        outfile.write(str(each.text))
                        outfile.close()
                        index += 1

                return HttpResponse(u"添加成功。")
            except Exception, e:
                return HttpResponse(u"添加失败，原因：" + str(e))
        else:
            return HttpResponse(u"上传失败。")

    return HttpResponse(u"请求错误。")
