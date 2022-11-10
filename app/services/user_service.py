def is_user_in_group(request, *groups):
    return request.user.groups.filter(name__in=groups).exists()