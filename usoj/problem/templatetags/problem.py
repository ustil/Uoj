# coding=utf-8
from django import template


def get_problem_status(problems_status, problem_id):
    if not problems_status:
        return '<span class="text-info">未解决</span>'

    if str(problem_id) in problems_status:
        if problems_status[str(problem_id)] == 1:
            return '<span class="text-success">已解决</span>'
        return '<span class="text-warning">待解决</span>'
    return '<span class="text-info">未解决</span>'


register = template.Library()
register.simple_tag(get_problem_status, name="get_problem_status")
