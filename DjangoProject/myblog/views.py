from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost, User
from .forms import BlogPostForm


def index(request):
    posts = BlogPost.objects.all().order_by('-created_date')
    context = {'posts': posts}
    return render(request, 'index.html', context)


def detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    context = {'post': post}
    return render(request, 'detail.html', context)


def create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = User.objects.get(id=request.user.id)
            post.save()
            return redirect('index')
    else:
        form = BlogPostForm()
    context = {'form': form}
    return render(request, 'create.html', context)


def update(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('detail', pk=post.pk)
    else:
        form = BlogPostForm(instance=post)
    context = {'form': form}
    return render(request, 'update.html', context)


def delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('index')
    context = {'post': post}
    return render(request, 'delete.html', context)


def registration(request):
    info = {'error': []}
    i = 0

    if request.method == 'POST':
        form = User(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']

            if username in get_all_users():
                i += 1
                info[f'error {i}'] = HttpResponse(f'Пользователь {username} уже существует', status=400,
                                                  reason='Повторяющийся логин')
                return HttpResponse('Пользователь уже существует', status=400, reason='Повторяющийся логин')

            if email in get_all_users():
                i += 1
                info[f'error {i}'] = HttpResponse(f'Пользователь с таким {email} уже существует', status=400,
                                                  reason='Повторяющийся email')
                return HttpResponse('Пользователь уже существует', status=400, reason='Повторяющийся email')

            if password != repeat_password:
                i += 1
                info[f'error {i}'] = HttpResponse('Пароли не совпадают', status=400,
                                                  reason='Пароли не совпадают')
                return HttpResponse('Пароли не совпадают', status=400, reason='Пароли не совпадают')

            new_user = User.objects.create(username=username, email=email, password=password)
            response = HttpResponse(f'Приветствуем {new_user.username}')
            response.status_code = 201
            return response

    else:
        form = User()
        context = {'info': info, 'form': form}
        return render(request, 'registration_page.html', context)


def get_all_users():
    return User.objects.all().values_list('username', 'email', flat=True)
