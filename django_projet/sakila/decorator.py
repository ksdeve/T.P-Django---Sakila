from django.shortcuts import redirect

def my_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('/')  # ou la page login
        return view_func(request, *args, **kwargs)
    return wrapper
