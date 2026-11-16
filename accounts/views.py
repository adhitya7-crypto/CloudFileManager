from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from .models import UserProfile


# Login
def login_view(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        messages.error(request, "Invalid username or password")

    return render(request, 'accounts/login.html')


# Register
def register_view(request):

    if request.method == "POST":

        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful!")
            return redirect('login')

    else:
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


# Dashboard
@login_required
def dashboard_view(request):
    return render(request, 'filemanager/dashboard.html')


# User Profile
@login_required
def profile_view(request):

    user = request.user

    profile, created = UserProfile.objects.get_or_create(user=user)

    fs = FileSystemStorage(location=None)
    user_folder = f'user_files/{user.id}'

    try:
        folders, files = fs.listdir(user_folder)
    except FileNotFoundError:
        files = []

    total_files = len(files)

    storage_used = sum(
        fs.size(f'{user_folder}/{filename}')
        for filename in files
    )

    storage_mb = round(storage_used / (1024 * 1024), 2)

    # Check whether profile photo exists
    profile_photo_url = None

    if profile.profile_picture:
        if (
            profile.profile_picture.name != 'profile_pictures/default.png'
            and profile.profile_picture.storage.exists(
                profile.profile_picture.name
            )
        ):
            profile_photo_url = profile.profile_picture.url

    context = {
        'username': user.username,
        'email': user.email,
        'date_joined': user.date_joined,
        'total_files': total_files,
        'storage_used': storage_mb,
        'profile': profile,
        'profile_photo_url': profile_photo_url,
    }

    return render(request, 'accounts/profile.html', context)


# Edit Profile
@login_required
def edit_profile_view(request):

    user = request.user

    if request.method == "POST":

        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()

        if not username:
            messages.error(request, "Username cannot be empty.")

        elif User.objects.filter(username=username).exclude(id=user.id).exists():
            messages.error(request, "Username already exists.")

        else:
            user.username = username
            user.email = email
            user.save()

            messages.success(request, "Profile updated successfully!")
            return redirect('profile')

    return render(request, 'accounts/edit_profile.html', {
        'username': user.username,
        'email': user.email,
    })


# Upload / Change Profile Photo
@login_required
def upload_profile_photo(request):

    if request.method == "POST":

        uploaded_photo = request.FILES.get('profile_picture')

        if not uploaded_photo:
            messages.error(request, "Please select a photo.")
            return redirect('profile')

        # Validate image
        image_field = forms.ImageField()

        try:
            validated_photo = image_field.clean(uploaded_photo)
        except forms.ValidationError:
            messages.error(request, "Please upload a valid image.")
            return redirect('profile')

        # Maximum file size: 5 MB
        if validated_photo.size > 5 * 1024 * 1024:
            messages.error(request, "Image size must be below 5 MB.")
            return redirect('profile')

        profile, created = UserProfile.objects.get_or_create(
            user=request.user
        )

        # Remove old photo when changing
        if profile.profile_picture:
            profile.profile_picture.delete(save=False)

        profile.profile_picture.save(
            validated_photo.name,
            validated_photo,
            save=True
        )

        messages.success(request, "Profile photo uploaded successfully!")
        return redirect('profile')

    return redirect('profile')


# Remove Profile Photo
@login_required
def remove_profile_photo(request):

    if request.method == "POST":

        profile, created = UserProfile.objects.get_or_create(
            user=request.user
        )

        if profile.profile_picture:
            profile.profile_picture.delete(save=False)
            profile.profile_picture = None
            profile.save()

            messages.success(request, "Profile photo removed successfully!")

        else:
            messages.error(request, "No profile photo found.")

    return redirect('profile')

# Change Password
@login_required
def change_password_view(request):

    if request.method == "POST":

        form = PasswordChangeForm(
            user=request.user,
            data=request.POST
        )

        if form.is_valid():

            user = form.save()

            # Keep the user logged in after password change
            update_session_auth_hash(request, user)

            messages.success(
                request,
                "Your password has been changed successfully!"
            )

            return redirect('profile')

        else:
            messages.error(
                request,
                "Please correct the errors below."
            )

    else:
        form = PasswordChangeForm(user=request.user)

    return render(
        request,
        'accounts/change_password.html',
        {'form': form}
    )