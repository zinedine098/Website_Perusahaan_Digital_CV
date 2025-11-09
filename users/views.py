from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm


def register(request):
    """Mendaftarkan pengguna baru"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Otomatis login setelah registrasi
            messages.success(request, 'Akun berhasil dibuat. Selamat datang di KursusKu!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    """Menampilkan profil pengguna"""
    return render(request, 'users/profile.html', {'user': request.user})


@login_required
def profile_edit(request):
    """Mengedit profil pengguna"""
    if request.method == 'POST':
        # Update user data
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.bio = request.POST.get('bio', '')
        request.user.phone_number = request.POST.get('phone_number', '')
        
        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            request.user.profile_picture = request.FILES['profile_picture']
        
        request.user.save()
        messages.success(request, 'Profil berhasil diperbarui.')
        return redirect('profile')
    
    return render(request, 'users/profile_edit.html', {'user': request.user})