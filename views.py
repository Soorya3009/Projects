from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Bookmark
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('bookmark_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def add_bookmark(request):
    username = request.user.username

    if Bookmark.objects.filter(username=username).count() >= 5:
        return render(request, 'add.html', {
            'error': 'You can add only 5 bookmarks'
        })

    if request.method == 'POST':
        title = request.POST['title']
        url = request.POST['url']

        Bookmark.objects.create(
            username=username,
            title=title,
            url=url
        )
        return redirect('bookmark_list')

    return render(request, 'add.html')

@login_required
def bookmark_list(request):
    username = request.user.username
    search = request.GET.get('search', '')

    bookmarks = Bookmark.objects.filter(
        username=username,
        title__icontains=search
    ) | Bookmark.objects.filter(
        username=username,
        url__icontains=search
    )

    paginator = Paginator(bookmarks.order_by('-created_at'), 2)
    page = request.GET.get('page')
    bookmarks = paginator.get_page(page)

    return render(request, 'list.html', {'bookmarks': bookmarks})

@login_required
def edit_bookmark(request, id):
    bookmark = get_object_or_404(
        Bookmark, id=id, username=request.user.username
    )

    if request.method == 'POST':
        bookmark.title = request.POST['title']
        bookmark.url = request.POST['url']
        bookmark.save()
        return redirect('bookmark_list')

    return render(request, 'edit.html', {'bookmark': bookmark})

@login_required
def delete_bookmark(request, id):
    bookmark = get_object_or_404(
        Bookmark, id=id, username=request.user.username
    )
    bookmark.delete()
    return redirect('bookmark_list')





