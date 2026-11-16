from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, Http404
from django.contrib import messages
from django.views.decorators.http import require_POST


# User Storage Folder
def get_user_storage(request):
    return FileSystemStorage(), f'user_files/{request.user.id}'


# Dashboard
@login_required
def dashboard(request):
    fs, user_folder = get_user_storage(request)

    try:
        _, files = fs.listdir(user_folder)
    except FileNotFoundError:
        files = []

    total_files = len(files)

    storage_used = sum(
        fs.size(f'{user_folder}/{file}')
        for file in files
    )

    storage_mb = round(storage_used / (1024 * 1024), 2)

    return render(request, 'filemanager/dashboard.html', {
        'total_files': total_files,
        'uploaded_files': total_files,
        'storage_used': storage_mb
    })


# Upload File
@login_required
def upload_file(request):
    fs, user_folder = get_user_storage(request)

    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')

        if uploaded_file:
            file_path = f'{user_folder}/{uploaded_file.name}'
            fs.save(file_path, uploaded_file)

            messages.success(request, 'File uploaded successfully!')
            return redirect('file_list')

        messages.error(request, 'Please select a file.')

    return render(request, 'filemanager/upload.html')


# File List
@login_required
def file_list(request):
    fs, user_folder = get_user_storage(request)

    try:
        _, files = fs.listdir(user_folder)
    except FileNotFoundError:
        files = []

    file_details = []

    for filename in files:
        file_path = f'{user_folder}/{filename}'

        file_details.append({
            'name': filename,
            'size': round(fs.size(file_path) / 1024, 2)
        })

    return render(request, 'filemanager/file_list.html', {
        'files': file_details
    })


# Download File
@login_required
def download_file(request, filename):
    fs, user_folder = get_user_storage(request)

    file_path = f'{user_folder}/{filename}'

    if not fs.exists(file_path):
        raise Http404("File not found")

    file_object = fs.open(file_path, 'rb')

    return FileResponse(
        file_object,
        as_attachment=True,
        filename=filename
    )


# Delete File
@login_required
@require_POST
def delete_file(request, filename):
    fs, user_folder = get_user_storage(request)

    file_path = f'{user_folder}/{filename}'

    if fs.exists(file_path):
        fs.delete(file_path)
        messages.success(request, 'File deleted successfully!')
    else:
        messages.error(request, 'File not found.')

    return redirect('file_list')