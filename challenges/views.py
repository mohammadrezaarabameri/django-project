from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound,Http404
from django.template.loader import render_to_string

users = {
    1: 'user own',
    2: 'user two',
    3: 'user three',
    4: 'user for',
}


def profile(request):
    return HttpResponse("user profile")


def edit(request):
    return HttpResponse("user edit")


def dynamic_users(request, user):
    data_user = users.get(user)
    context = {
        'data': data_user,
        'user': user,
    }
    if data_user is not None:
        return render(request,'challenges/challenge.html', context)
    raise Http404()

def list_users(request):
    data_users = list(users.keys())
    context = {
        'users': data_users,
    }
    return render(request,'challenges/index.html', context)