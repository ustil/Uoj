from django.shortcuts import render
from index.models import Notice
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from problem.models import Problem
from solution.models import Solution
from contest.models import Contest
from group.models import Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    notices = Notice.objects.order_by('create_time')[:5]
    return render(request, 'index.html', {'notices': notices})

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'description']

def searchpage(request):
    return render(request, 'search.html')

def search(request):
    type = request.GET.get('type')
    exact = request.GET.get('exact')
    if type == "1":
        id = request.GET.get('pro_id')
        title = request.GET.get('pro_title')
        diff = request.GET.get('pro_diff')
        user = request.GET.get('pro_user')
        
        if exact:
            answer = Problem.objects.filter(visible=True)
            if id:
                answer = answer.filter(id=str(id))
            if title:
                answer = answer.filter(title=str(title))
            if diff:
                answer = answer.filter(difficulty=str(diff))
            if user:
                answer = answer.filter(created_by__username=str(user))
        else:
            answer = Problem.objects.filter(Q(id__contains=str(id)))
            answer = answer.filter(Q(title__contains=str(title)))
            answer = answer.filter(Q(difficulty__contains=str(diff)))
            answer = answer.filter(Q(created_by__username__contains=str(user)))

        paginator = Paginator(answer, 25)
 
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)

        return render(request, 'problem/problem.html', {'problems': contacts})
    elif type == "2":
        id = request.GET.get('sol_id')
        title = request.GET.get('sol_title')
        user = request.GET.get('sol_user')

        if exact:
            answer = Solution.objects.filter(contest=None)
            if id:
                answer = answer.filter(solution_id=str(id))
            if title:
                answer = answer.filter(problem_id__id=str(title))
            if user:
                answer = answer.filter(user_id__username=str(user))
        else:
            answer = Solution.objects.filter(Q(solution_id__contains=str(id)))
            answer = answer.filter(Q(problem_id__id__contains=str(title)))
            answer = answer.filter(Q(user_id__username__contains=str(user)))

        paginator = Paginator(answer, 25)

        page = request.GET.get('page')

        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)

        return render(request, 'solution/solution.html', {'solutions': contacts})

    elif type == "3":
        id = request.GET.get('con_id')
        title = request.GET.get('con_title')
        
        if exact:
            answer = Contest.objects.all()
            if id:
                answer = answer.filter(id=str(id))
            if title:
                answer = answer.filter(title=str(title))
        else:
            answer = Contest.objects.filter(Q(id__contains=str(id)))
            answer = answer.filter(Q(title__contains=str(title)))

        paginator = Paginator(answer, 25)
 
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)

        return render(request, 'contest/contest.html', {'contests': contacts})

    elif type == "4":
        #gro_id=&gro_title=&gro_member=
        id = request.GET.get('gro_id')
        title = request.GET.get('gro_title')
        member = request.GET.get('gro_member')
        
        if exact:
            answer = Group.objects.all()
            if id:
                answer = answer.filter(id=str(id))
            if title:
                answer = answer.filter(name=str(title))
        else:
            answer = Group.objects.filter(Q(id__contains=str(id)))
            answer = answer.filter(Q(name__contains=str(title)))
        paginator = Paginator(answer, 25)
 
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)

        return render(request, 'group/group.html', {'groups': contacts})
    else:
        return HttpResponseRedirect("/")

def addNotice(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = Notice(title=form.cleaned_data['title'], \
                              description=form.cleaned_data['description'], \
                              created_by=request.user)
            notice.save()
            return HttpResponseRedirect("/")
        else:
            return render(request, 'addcontest.html', {'form': form})

    form = NoticeForm()

    return render(request, 'addcontest.html', {'form': form})
