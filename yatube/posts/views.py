from tkinter import PAGES
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from .models import Post, Group, User, Comment
from .forms import PostForm, CommentForm


PAGES = 10


# Главная страница
def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, PAGES)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


# Список групп
def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).all()
    paginator = Paginator(posts, PAGES)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
        'posts': posts,
    }
    return render(request, 'posts/group_list.html', context)


# Профайл пользователя
def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.posts.all()
    paginator = Paginator(posts, PAGES)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'author': user,
        'user': user,
        'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


# Запись пользователя
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post_count = Post.objects.filter(author=post.author).count()
    comments = Comment.objects.filter(post_id=post_id)
    form_comments = CommentForm(request.POST or None)
    context = {
        'post': post,
        'post_count': post_count,
        'comments': comments,
        'form_comments': form_comments
    }
    return render(request, 'posts/post_detail.html', context)


# Создание записи
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(
            request.POST,
            files=request.FILES or None,
        )
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', username=request.user)
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


# Изменение записи
@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if request.user != post.author:
        return redirect('posts:profile', post.author)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
    context = {
        'form': form,
        'is_edit': True,
        'post': post,
    }
    return render(request, 'posts/create_post.html', context)

# Добавление комментария
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)