from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def login_view(request):
    if request.user.is_authenticated:
        return redirect('executive_summary')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            next_url = request.GET.get('next', 'executive_summary')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
        
    return render(request, 'auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

def custom_404(request, exception):
    return render(request, 'components/error_state.html', {
        'error_code': 404,
        'error_title': 'Page Not Found',
        'error_message': 'The requested dashboard domain or analytical view does not exist.'
    }, status=404)

def custom_500(request):
    return render(request, 'components/error_state.html', {
        'error_code': 500,
        'error_title': 'Internal Analytical Error',
        'error_message': 'An unexpected database or query exception occurred. Please try again.'
    }, status=500)
