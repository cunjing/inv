from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def index(request):
    return render_to_response('index.html')


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
        rtn = render(request, 'sign_in.html')

    return rtn


@csrf_protect
def sign_up(request):
    return render(request, 'sign_up.html')


def logout(request):
    logout(request)
    # return HttpResponseRedirect(reverse('depotapp.views.store'))
    pass


@login_required
def home(request):
    pass
