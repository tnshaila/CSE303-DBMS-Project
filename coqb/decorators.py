from django.shortcuts import render
from django.shortcuts import redirect


def authenticated(viewFunc):
    def wrapperFunc(request, *args, **kwargs):
        if request.user.is_authenticated:
            return viewFunc(request, *args, **kwargs)
        else:
            return redirect('signin')
            
    return wrapperFunc
    
    
def unauthenticated(viewFunc):
    def wrapperFunc(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return viewFunc(request, *args, **kwargs)
            
    return wrapperFunc