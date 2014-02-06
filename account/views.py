from django.shortcuts import render_to_response


def index(request):
    return render_to_response('index.html')


def sign_in(request):
    return render_to_response('sign_in.html')


def sign_up(request):
    return render_to_response('sign_up.html')
