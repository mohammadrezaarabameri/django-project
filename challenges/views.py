from django.shortcuts import render
from django.http import HttpResponse

from .utils import get_user_ids, get_user_or_404


def profile(request):
    return HttpResponse("user profile")


def edit(request):
    return HttpResponse("user edit")


def dynamic_users(request, user):
    context = {
        'data': get_user_or_404(user),
        'user': user,
    }
    return render(request, 'challenges/challenge.html', context)


def list_users(request):
    context = {
        'users': get_user_ids(),
    }
    return render(request, 'challenges/index.html', context)
