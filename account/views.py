from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from forms import *


dir_tpl = 'account/'


@csrf_protect
def sign_in(request):
    rtn = None

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                rtn = HttpResponseRedirect(reverse('account.views.home'))
    else:
        rtn = render(request, dir_tpl + 'sign_in.html')

    return rtn


@csrf_protect
def sign_up(request):
    rtn = None

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            rtn = render(request, dir_tpl + 'sign_up.html', {'form': form})
    else:
        form = SignupForm()
        rtn = render(request, dir_tpl + 'sign_up.html', {'form': form})

    return rtn


def logout(request):
    logout(request)
    # return HttpResponseRedirect(reverse('depotapp.views.store'))
    pass


@login_required
def home(request):
    pass
