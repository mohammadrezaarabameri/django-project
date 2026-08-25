from django.http import Http404

users = {
    1: 'user own',
    2: 'user two',
    3: 'user three',
    4: 'user for',
}


def get_user_ids():
    return list(users.keys())


def get_user_or_404(user):
    data_user = users.get(user)
    if data_user is None:
        raise Http404()
    return data_user
