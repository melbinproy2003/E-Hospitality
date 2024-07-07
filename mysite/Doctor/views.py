from django.shortcuts import render, redirect

# Create your views here.
def doctor_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.session.get('type') != 'doctor':
            return redirect('login')  # Redirect to the login page if not 'webadmin'
        return view_func(request, *args, **kwargs)
    return wrapper_func