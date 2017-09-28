# -*- coding:utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from contest.models import Contest, ContestProblem, ContestRank
from problem.views import SubmitForm, timelim
from problem.models import Problem
from solution.models import Solution
from group.models import Group, GroupMember
from django.utils.timezone import now
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from utils.decorators import power_required, contest_required, contest_time_required
from django.views.decorators.csrf import csrf_exempt
import urllib, urllib2
import json
import redis

class ContestForm(forms.ModelForm):
    class Meta:
        model = Contest
        fields = ['title', 'description', 'start_time', 'end_time', 'contest_type', 'password', 'groups', 'visible', 'users']

'''
@login_required(login_url='/account/login/')
@power_required(redirect='/contest/notice/', powerneed=244)
def addContest(request):
    ProblemFormSet = modelformset_factory(ContestProblem, fields=('show_id', 'problem'), min_num=1)
    if request.method == 'POST':
        form = ContestForm(request.POST)
        formset = ProblemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            contest = Contest(title=form.cleaned_data['title'], \
                              description=form.cleaned_data['description'], \
                              start_time=form.cleaned_data['start_time'], \
                              end_time=form.cleaned_data['end_time'], \
                              contest_type=form.cleaned_data['contest_type'], \
                              password=form.cleaned_data['password'], \
                              visible=form.cleaned_data['visible'], \
                              created_by=request.user)
            contest.save()
            for group in form.cleaned_data['groups']:
                contest.groups.add(group)
            for eachuser in form.cleaned_data['users']:
                contest.users.add(eachuser)
            print contest.users.all()
            showid = 1
            for problems in formset:
                problem = ContestProblem(show_id=str(showid), contest=contest, problem=problems.cleaned_data['problem'])
                problem.save()
                showid += 1
            return HttpResponseRedirect("/contest/")
        else:
            return render(request, 'addcontest.html', {'form': form, 'forms' : formset})

    form = ContestForm()
    formset = ProblemFormSet()

    return render(request, 'addcontest.html', {'form': form, 'forms' : formset})
'''

@login_required(login_url='/account/login/')
@contest_required(redirect='/contest/notice/')
@contest_time_required(redirect='/contest/notice/')
def contestSubmit(request, id):
    contest = Contest.objects.get(pk=id)
    usergroup = set(Group.objects.filter(groupmember__account=request.user))
    contestgroup = set(contest.groups.all())
    group = list(usergroup.intersection(contestgroup))
    if len(group) > 1:
        error = ""
        for each in group:
            error += 'Id: ' + str(each.id) + ' Name:' + str(each.name) + '<br>'
        result = {}
        result['status'] = 'error'
        result['reason'] = u'你同时加入此比赛比赛队伍：<br>' + error + u'请尝试退出并保留一个参赛队伍。'
        return HttpResponse(json.dumps(result))
    if request.method == 'POST':
        form = SubmitForm(request.POST)
        result = {}
        result['status'] = 'error'
        if not timelim(request.user.username):
            result['reason'] = u'提交速度过快，请稍后再尝试提交。'
            return HttpResponse(json.dumps(result))
        if form.is_valid():
            contestproblem = get_object_or_404(ContestProblem, pk=int(form.cleaned_data['problem']))
            problem = contestproblem.problem
            res = { 'lang' : form.cleaned_data['lang'], 'id' : int(problem.id), 'timelim' : problem.time_limit, 'memorylim' : problem.memory_limit, 'code' : form.cleaned_data['code']}
            if contestproblem.contest.contest_type == 3 or contestproblem.contest.contest_type == 4:
                #print contestproblem.contest.member__set.all()
                thisgroup = Group.objects.get(member=request.user, contest__id=contestproblem.contest.id)
                submit = Solution(contestproblem=contestproblem, memory=0, runtime=0.0, result='Waiting', languge=res['lang'], code=res['code'], user_id=request.user, group=thisgroup, contest=contestproblem.contest)
            else:
                submit = Solution(contestproblem=contestproblem, memory=0, runtime=0.0, result='Waiting', languge=res['lang'], code=res['code'], user_id=request.user, contest=contestproblem.contest)
            submit.save()
            res['sid'] = submit.solution_id
            res['type'] = 'ORD'
            post_data = urllib.urlencode(res).encode('utf-8')
            allproblem = ContestProblem.objects.filter(contest=submit.contest)
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

def mycmp(rank1, rank2):
    if rank1['ac'] > rank2['ac']:
        return -1
    elif rank1['ac'] < rank2['ac']:
        return 1
    else:
        if rank1['time'] > rank2['time']:
            return 1
        else:
            return -1

recon = redis.Redis(host='localhost', port=6379)

def updateRank(id):
    rank = ContestRank.objects.filter(contest_id=id).values('problems_status')
    ranks = []
    for each in rank:
        ranks.append(json.loads(each['problems_status']))

    if ranks:
        ranks.sort(cmp=mycmp)
        i = 1
        for each in ranks:
            if each['name'].startswith("*"):
                each['rank'] = '*'
            else:
                each['rank'] = i
                i += 1
    
    recon.hset(str('contest_'+str(id)), 'rank', str(ranks))

@login_required(login_url='/account/login/')
@contest_required(redirect='/contest/notice/')
def contestRank(request, id):
    cacherank = recon.hget(str('contest_'+str(id)), 'rank')
    problem = ContestProblem.objects.filter(contest_id=id)

    if not cacherank:
        updateRank(id)
    else:
        ranks = eval(cacherank)

    return render(request, 'contest/contestRank.html', {'ranks': ranks, 'problems' : problem, 'id' : id})

@login_required(login_url='/account/login/')
@contest_required(redirect='/contest/notice/')
def contestSolution(request, id):
    solutions = Solution.objects.filter(contest_id=id)

    paginator = Paginator(solutions, 25)
 
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'contest/contestSol.html', {'solutions': contacts, 'id': id})

@login_required(login_url='/account/login/')
@contest_required(redirect='/contest/notice/')
@contest_time_required(redirect='/contest/notice/')
def contestProblem(request, id):
    if request.method == 'GET':
        if request.GET['pid']:
            try:
                pid = request.GET['pid']
                problem = get_object_or_404(ContestProblem, pk=pid)
                form = SubmitForm()
                return render(request, 'contest/contestProblem.html', {'form': form, 'problem': problem, 'pid':id})
            except:
                return HttpResponse('获取失败。')
    return HttpResponse('参数错误。')

def contestList(request):
    contest = Contest.objects.all()

    paginator = Paginator(contest, 25)

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'contest/contest.html', {'contests': contacts})

@csrf_exempt
@login_required(login_url='/account/login/')
@contest_time_required(redirect='/contest/notice/')
def enrollGroup(request, id):
    contest = Contest.objects.get(id=id)
    if contest.status == 0:
        return HttpResponse('报名时间已经结束。')
    if request.method == 'POST':
        power = GroupMember.objects.get(account=request.user, groups_id=request.POST['id'])
        if power.identity == 'C':
            thisgroup = Group.objects.get(id=request.POST['id'])
            group = contest.groups.all()
            if thisgroup in group:
                return HttpResponse('该队伍已经报名。')
            groupuser = []
            for each in thisgroup.groupmember_set.all():
                groupuser.append(each.account)
            groupuser = set(groupuser)
            alluser = []
            for each in group:
                for eachper in each.groupmember_set.all():
                    alluser.append(eachper.account)
            alluser = set(alluser)
            print alluser, ':', groupuser, ":", list(groupuser.intersection(alluser))
            if list(groupuser.intersection(alluser)):
                return HttpResponse('队伍有队员已经参加比赛。')
            contest.groups.add(thisgroup)
            return HttpResponse('报名成功！')
        else:
            return HttpResponse('只有队长才能报名比赛。')
    return HttpResponse('参数错误。')

@login_required(login_url='/account/login/')
@contest_time_required(redirect='/contest/notice/')
def enrollUser(request, id):
    contest = Contest.objects.get(id=id)
    if request.user in users:
        return HttpResponse('你已经报名过了。')
    contest.users.add(request.user)
    return HttpResponse('报名成功！')

def notice(request):
    return render(request, 'error.html', {'error': u'你没有权限进去该页面，请尝试报名比赛。'})

@csrf_exempt
@login_required(login_url='/account/login/')
@contest_required(redirect='/contest/notice/')
def contestPassword(request, id):
    if request.method == 'POST':
        contest = Contest.objects.get(pk=id)
        temppass = request.POST.get('password', None)
        if temppass == contest.password:
            response = HttpResponseRedirect('/contest/detail/'+str(id)+'/')
            response.set_cookie('contest_'+str(id), temppass, 18000)
            return response
        else:
            return HttpResponse('密码错误。')
    return render(request, 'contest/contestPassword.html', {'id': id })

@login_required(login_url='/account/login/')
@contest_time_required(redirect='/contest/notice/')
@contest_required(redirect='/contest/notice/')
def contestDetail(request, id):
    contest = get_object_or_404(Contest, pk=id)
    try:
        if contest.contest_type == 3 or contest.contest_type == 4 :
            thisgroup = Group.objects.get(member=request.user, contest__id=contest.id)
            rank = ContestRank.objects.get(group=thisgroup, contest=contest)
        else:
            rank = ContestRank.objects.get(user=request.user, contest=contest)
    except:
        rank = None
    return render(request, 'contest/contestDetail.html', {'contest': contest ,'rank' : rank})

def contestGroup(request, id):
    contest = get_object_or_404(Contest, pk=id)
    return render(request, 'contest/contestGroup.html', {'contest': contest})

@login_required(login_url='/account/login/')
def chooseGroup(request):
    groups = Group.objects.filter(groupmember__account=request.user, groupmember__identity='C')
    id = request.GET.get('id',None)
    return render(request, 'contest/chooseGroup.html', {'groups' : groups, 'id' : id})
