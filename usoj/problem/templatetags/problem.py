# coding=utf-8

def get_problem_status(problems_status, problem_id):
    # 用户没登陆 或者 user.problem_status 中没有这个字段都会到导致这里的problem_status 为 ""
    if not problems_status:
        return '<span class="text-info">未解决</span>'

    if str(problem_id) in problems_status:
        if problems_status[str(problem_id)] == 1:
            return '<span class="text-success">已解决</span>'
        return '<span class="text-warning">待解决</span>'
    return '<span class="text-info">未解决</span>'

from django import template

register = template.Library()
register.simple_tag(get_problem_status, name="get_problem_status")
