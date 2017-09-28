# coding: utf-8
from functools import wraps
from contest.models import Contest
from group.models import Group
from django.http import HttpResponse, HttpResponseRedirect
import json

def power_required(redirect=None, powerneed=1):
    def decorator(func):
        @wraps(func)
        def returned_power(request, *args, **kwargs):
            if request.user.is_authenticated:
                power = request.user.admin_type
                if int(power) < int(powerneed):
                    return HttpResponseRedirect(redirect)
            return func(request, *args, **kwargs)
        return returned_power
    return decorator

def contest_required(redirect=None):
    def decorator(func):
        @wraps(func)
        def returned_join(request, *args, **kwargs):
            id = kwargs['id']
            contest = Contest.objects.get(id=id)
            #if contest.password != None or contest.password != "":
            #    passw = request.COOKIES.get('contest_'+str(id), None)
            #    if passw != contest.password:
            #        return HttpResponseRedirect("/contest/password/"+str(id)+"/")
            #power = request.user.admin_type
            #if int(power) >= 255:
            #    return func(request, *args, **kwargs)
            type = contest.contest_type
            if type == 5 or type == 6:
                if request.user in contest.users.all():
                    return func(request, *args, **kwargs)
                else:
                    return HttpResponseRedirect(redirect)
            elif type == 3 or type == 4:
                usergroup = set(Group.objects.filter(groupmember__account=request.user))
                contestgroup = set(contest.groups.all())
                group = list(usergroup.intersection(contestgroup))
                if group:
                    return func(request, *args, **kwargs)
                else:
                    return HttpResponseRedirect(redirect)
            else:
                return func(request, *args, **kwargs)
        return returned_join
    return decorator

def contest_time_required(redirect=None):
    def decorator(func):
        @wraps(func)
        def returned_join(request, *args, **kwargs):
            power = request.user.admin_type
            if int(power) >= 255:
                return func(request, *args, **kwargs)
            id = kwargs['id']
            contest = Contest.objects.get(id=id)
            if contest.status == 0:
                return HttpResponseRedirect(redirect)
            else:
                return func(request, *args, **kwargs)
        return returned_join
    return decorator
