#coding: utf-8
from django.shortcuts import render
from django import forms
from group.models import Group, GroupMember, Audit
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class CreatGroupForm(forms.Form):
    typeChoices = (
        ('1', '比赛队伍'),
        ('2', '交流组织'),
        )
    groupname = forms.CharField(label='队伍名称:', max_length = 20, min_length = 1)
    type = forms.ChoiceField(label='队伍类型:', choices=typeChoices)

@login_required(login_url='/account/login/')
def createGroup(request):
    if request.method == 'POST':
        form = CreatGroupForm(request.POST)
        if form.is_valid():
            try:
                Group.objects.get(name=form.cleaned_data['groupname'])
                return HttpResponse('队伍名称已经存在。')
            except Group.DoesNotExist:
                pass
            creat = Group(name=form.cleaned_data['groupname'], type=int(form.cleaned_data['type']))
            creat.save()
            member = GroupMember(identity='C', account=request.user, groups=creat)
            member.save()
            return HttpResponse('创建成功！')
        else:
            return HttpResponse('参数错误。')

    form = CreatGroupForm()

    return render(request, 'group/groupcreate.html', {'form': form})

def groupList(request):
    groups = Group.objects.all()
   
    paginator = Paginator(groups, 25)
 
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
        
    return render(request, 'group/group.html', {'groups': contacts})

@login_required(login_url='/account/login/')
def joinGroup(request):
    if request.method == 'GET':
        if request.GET['id']:
            id = request.GET['id']
            join = Group.objects.get(id=id)
            try:
                Group.objects.get(id=id, groupmember__account=request.user)
                return HttpResponse('不可以重复加入。')
            except:
                pass
            try:
                Audit.objects.get(account=request.user, groups=join)
                return HttpResponse('不可以重复申请。')
            except:
                pass
            member = Audit(account=request.user, groups=join)
            member.save()
            return HttpResponse('申请成功。')
    return HttpResponse('发生错误。')

@login_required(login_url='/account/login/')
def delGroup(request, id):
    power = GroupMember.objects.get(account=request.user, groups_id=id)
    if power:
        if power.identity == 'C':
            Group.objects.get(id=id).delete()
            return HttpResponseRedirect("/group/mygroup/") #HttpResponse('解散成功。')
        else:
            power.delete()
            return HttpResponseRedirect("/group/mygroup/") #HttpResponse('退出成功。')
    else:
        return HttpResponseRedirect("/group/mygroup/") #HttpResponse('你不在队伍内。')

@login_required(login_url='/account/login/')
def kickGroup(request, id):
    temp = GroupMember.objects.get(id=id)
    try:
        GroupMember.objects.get(groups=temp.groups, identity='C', account=request.user)
        temp.delete()
        return HttpResponseRedirect("/group/mygroup/")
    except GroupMember.DoesNotExist:
        return HttpResponseRedirect("/group/mygroup/") #HttpResponse('你没有权限。')

@login_required(login_url='/account/login/')
def myGroup(request):
    myGroup = Group.objects.filter(groupmember__account=request.user)
    myAudit = Audit.objects.filter(groups__groupmember__identity='C', groups__groupmember__account=request.user)
    c = zip(myGroup, myAudit)
    create = []
    for group in myGroup:
        for each in group.groupmember_set.all():
            if each.identity == 'C' :
                create.append(each)
    myGroup = zip(myGroup, create)
    return render(request, 'group/groupown.html', {'groups': myGroup, 'audits' : myAudit})

@login_required(login_url='/account/login/')
def auditAllow(request, id):
    audit = Audit.objects.get(id=id)
    try:
        GroupMember.objects.get(groups=audit.groups, identity='C', account=request.user)
        member = GroupMember(identity='M', account=audit.account, groups=audit.groups)
        member.save()
        audit.delete()
        return HttpResponseRedirect("/group/mygroup/")
    except GroupMember.DoesNotExist:
        return HttpResponseRedirect("/group/mygroup/") #HttpResponse('你没有审核权限。')

@login_required(login_url='/account/login/')
def auditReject(request, id):
    audit = Audit.objects.get(id=id)
    try:
        GroupMember.objects.get(groups=audit.groups, identity='C', account=request.user)
        audit.delete()
        return HttpResponseRedirect("/group/mygroup/")
    except GroupMember.DoesNotExist:
        return HttpResponseRedirect("/group/mygroup/") #HttpResponse('你没有审核权限。')
