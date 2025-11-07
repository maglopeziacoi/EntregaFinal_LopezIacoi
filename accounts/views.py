from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .forms import SignUpForm, ProfileForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registro exitoso. ¡Bienvenido!')
            login(request, user)
            return redirect('home')
        return render(request, 'accounts/signup.html', {'form': form})
    else:
        form = SignUpForm()
        return render(request, 'accounts/signup.html', {'form': form})
    

def public_profile(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'accounts/public_profile.html', {'profile_user': user})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado')
            return redirect('profile')
        return render(request, 'accounts/profile_form.html', {'form': form})
    else:
        form = ProfileForm(instance=request.user.profile)
        return render(request, 'accounts/profile_form.html', {'form': form})

class PasswordChange(PasswordChangeView):
    success_url = reverse_lazy('profile')
    template_name = 'registration/password_change_form.html'