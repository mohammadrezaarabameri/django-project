import logging

from django.http import Http404, HttpResponse
from django.shortcuts import render

logger = logging.getLogger(__name__)

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
    try:
        data_user = users[user]
    except KeyError as exc:
        logger.warning("Requested unknown user id %r", user)
        raise Http404(f"No user with id {user}.") from exc

    context = {
        'data': data_user,
        'user': user,
    }
    return render(request, 'challenges/challenge.html', context)


def list_users(request):
    data_users = list(users.keys())
    context = {
        'users': data_users,
    }
    return render(request, 'challenges/index.html', context)
