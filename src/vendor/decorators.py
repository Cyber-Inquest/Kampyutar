from django.shortcuts import redirect
from django.contrib import messages


def vendor_only(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff and request.user.profile.authorization:
            return view_func(request, *args, **kwargs)
        else:
            messages.warning(request, 'Access Denied!')
            return redirect('vendor_login_vendor')
    return wrap
