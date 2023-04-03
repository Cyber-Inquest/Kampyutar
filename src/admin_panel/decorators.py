from django.shortcuts import redirect
from django.contrib import messages


def admin_only(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            messages.warning(request, 'Access Denied!')
            return redirect('admin_login_admin')
    return wrap
