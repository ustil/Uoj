# coding=utf-8

import datetime

def get_problem(problem, rank):
    try:
        if rank[str(problem.id)]['solvetime']:
            m, s = divmod(rank[str(problem.id)]['solvetime'], 60)
            h, m = divmod(m, 60)
            strtime = "%02d:%02d:%02d" % (h, m, s)
            if rank[str(problem.id)]['error'] == 0:
                return '<span class="text-success">%s</span>' % (strtime)
            else:
                return '<span class="text-success">%s(-%d)</span>' % (strtime, rank[str(problem.id)]['error'])
        else:
            if rank[str(problem.id)]['error'] == 0:
                return '<span class="text-info">未解决</span>'
            else:
                return '<span class="text-info">未解决(-%d)</span>' % rank[str(problem.id)]['error']
    except:
        return '<span class="text-info">未解决</span>'

def get_time(time):
    m, s = divmod(time, 60)
    h, m = divmod(m, 60)
    strtime = "%02d:%02d:%02d" % (h, m, s)
    return strtime

def get_status(problem, rank):
    if rank:
        try:
            if rank.problems_status['problems'][str(problem.id)]['solvetime']:
                return '<span class="text-success">已解决</span>'
            else:
                return '<span class="text-info">未解决</span>'
        except:
            return '<span class="text-info">未解决</span>'
    return '未参加'

from django import template

register = template.Library()
register.simple_tag(get_problem, name="get_problem")
register.simple_tag(get_time, name="get_time")
register.simple_tag(get_status, name="get_status")
