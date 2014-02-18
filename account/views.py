# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from forms import *


@csrf_protect
def sign_in(request):
    rtn = None
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if email and password:
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                rtn = HttpResponseRedirect(reverse('inv.views.index'))
    else:
        form = SignInForm()
        rtn = render(request, 'account/sign_in.html', {'form': form})
    return rtn


@csrf_protect
def sign_up(request):
    rtn = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            rtn = render(request, 'account/sign_up.html', {'form': form})
    else:
        form = SignUpForm()
        rtn = render(request, 'account/sign_up.html', {'form': form})
    return rtn


def logout(request):
    logout(request)
    # return HttpResponseRedirect(reverse('depotapp.views.store'))
    pass


@login_required
def home(request):
    pass
