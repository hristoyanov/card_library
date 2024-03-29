from django.shortcuts import render


def group_required(groups=None):
    if groups is None:
        groups = []

    groups_set = set(groups)

    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            raw_groups = request.user.groups.only('name')
            user_groups = set([group.name for group in raw_groups])

            if user_groups.intersection(groups_set):
                return view_func(request, *args, **kwargs)
            return render(request, 'common/unauthorized.html')
        return wrapper
    return decorator
