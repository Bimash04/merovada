from django.http import HttpResponseForbidden
from django.shortcuts import redirect

def role_required(role):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')  # Redirect to login if user is not authenticated
            if request.user.role != role:
                return HttpResponseForbidden("You are not authorized to access this page.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
