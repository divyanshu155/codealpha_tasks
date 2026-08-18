from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

from django.contrib.auth.models import User
from .models import Profile, Post, Comment, Follow

def register_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to SocialPulse, {user.username}!")
            return redirect('feed')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('feed')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('login')

@login_required
def feed_view(request):
    posts = Post.objects.all().select_related('author', 'author__profile').prefetch_related('likes', 'comments', 'comments__author')
    
    # Track posts liked by current user
    user_liked_ids = set(request.user.liked_posts.values_list('id', flat=True))
    
    context = {
        'posts': posts,
        'user_liked_ids': user_liked_ids
    }
    return render(request, 'feed.html', context)

@login_required
def profile_view(request, username=None):
    if username:
        profile_user = get_object_or_404(User, username=username)
    else:
        profile_user = request.user

    posts = Post.objects.filter(author=profile_user).prefetch_related('likes', 'comments')
    followers_count = Follow.objects.filter(following=profile_user).count()
    following_count = Follow.objects.filter(follower=profile_user).count()
    
    is_following = False
    if request.user != profile_user:
        is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()

    user_liked_ids = set(request.user.liked_posts.values_list('id', flat=True))

    context = {
        'profile_user': profile_user,
        'posts': posts,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
        'user_liked_ids': user_liked_ids
    }
    return render(request, 'profile.html', context)

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        bio = request.POST.get('bio', '')
        location = request.POST.get('location', '')
        profile = request.user.profile
        profile.bio = bio
        profile.location = location
        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')
    return render(request, 'edit_profile.html')

@login_required
def discover_view(request):
    # Exclude current user and list users to follow
    users = User.objects.exclude(id=request.user.id).select_related('profile')
    following_ids = set(Follow.objects.filter(follower=request.user).values_list('following_id', flat=True))
    
    context = {
        'users': users,
        'following_ids': following_ids
    }
    return render(request, 'discover.html', context)

# ==================== AJAX JSON APIs ==================== #

@login_required
@require_POST
def api_create_post(request):
    content = request.POST.get('content', '').strip()
    if not content:
        return JsonResponse({'error': 'Post content cannot be empty'}, status=400)
    
    post = Post.objects.create(author=request.user, content=content)
    return JsonResponse({
        'success': True,
        'id': post.id,
        'author': post.author.username,
        'avatar_url': post.author.profile.avatar_url,
        'content': post.content,
        'created_at': post.created_at.strftime('%b %d, %Y %I:%M %p')
    })

@login_required
@require_POST
def api_toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return JsonResponse({
        'liked': liked,
        'count': post.total_likes()
    })

@login_required
@require_POST
def api_add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    content = request.POST.get('content', '').strip()
    if not content:
        return JsonResponse({'error': 'Comment content cannot be empty'}, status=400)

    comment = Comment.objects.create(post=post, author=request.user, content=content)
    return JsonResponse({
        'success': True,
        'id': comment.id,
        'author': comment.author.username,
        'avatar_url': comment.author.profile.avatar_url,
        'content': comment.content,
        'created_at': comment.created_at.strftime('%b %d, %I:%M %p'),
        'total_comments': post.comments.count()
    })

@login_required
@require_POST
def api_toggle_follow(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    if target_user == request.user:
        return JsonResponse({'error': 'Cannot follow yourself'}, status=400)

    follow_rel = Follow.objects.filter(follower=request.user, following=target_user)
    if follow_rel.exists():
        follow_rel.delete()
        following = False
    else:
        Follow.objects.create(follower=request.user, following=target_user)
        following = True

    followers_count = Follow.objects.filter(following=target_user).count()
    return JsonResponse({
        'following': following,
        'followers_count': followers_count
    })
