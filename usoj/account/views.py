# coding: utf-8
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import User, UserProfile
from django import forms
from django.http import HttpResponseRedirect


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=20,
                               min_length=1)
    password = forms.CharField(label='密码', max_length=20,
                               min_length=1)


class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名',
                               max_length=20, min_length=1)
    password = forms.CharField(label='密码', max_length=20,
                               min_length=1)
    confirm = forms.CharField(label='确认密码', max_length=20,
                              min_length=1)


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data["username"],
                                     password=form.cleaned_data["password"])
            if user:
                auth.login(request, user)

                next_to = request.GET.get('next', None)

                if next_to:
                    return HttpResponseRedirect(next_to)

                return HttpResponseRedirect("/problem/")
            else:
                form.add_error('username', u'用户名或密码错误。')
                form.add_error('password', u'用户名或密码错误。')

        return render(request, 'login.html', {'form': form})

    form = LoginForm()

    return render(request, 'login.html', {'form': form})


@login_required(login_url='/account/login/')
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/account/login/")


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                User.objects.get(username=form.cleaned_data["username"])
                form.add_error('username', u'用户名已存在。')
                return render(request, 'register.html', {'form': form})
            except Exception:
                pass
            if form.cleaned_data['password'] != form.cleaned_data['confirm']:
                form.add_error('password', u'两次密码输入不一样。')
                form.add_error('confirm', u'两次密码输入不一样。')
                return render(request, 'register.html', {'form': form})
            user = User.objects.create(username=form.cleaned_data['username'])
            user.set_password(form.cleaned_data['password'])
            user.save()
            UserProfile.objects.create(user=user).save()
            return HttpResponseRedirect("/account/login/")
        else:
            return render(request, 'register.html', {'form': form})

    form = RegisterForm()

    return render(request, 'register.html', {'form': form})
