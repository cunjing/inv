# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, logout as auth_logout
from django.contrib.auth.decorators import login_required

from forms import *


@csrf_protect
def sign_in(request):
    form = SignInForm()
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            login(request, form.user_cache)
            return HttpResponseRedirect(reverse('inv.views.index'))
    return render(request, 'account/sign_in.html', {'form': form})


@csrf_protect
def sign_up(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.create_user()
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('inv.views.index'))
    return render(request, 'account/sign_up.html', {'form': form})


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('inv.views.index'))


@login_required
def home(request):
    pass
