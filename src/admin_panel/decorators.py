from django.shortcuts import redirect
from django.contrib import messages


def is_admin(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            messages.warning(request, 'Access Denied!')
            return redirect('admin_login')
    return wrap

def is_staff(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            messages.warning(request, 'Access Denied!')
            return redirect('admin_login')
    return wrap
