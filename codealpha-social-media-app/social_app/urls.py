from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed_view, name='feed'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('profile/<str:username>/', views.profile_view, name='user_profile'),
    path('discover/', views.discover_view, name='discover'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # AJAX APIs
    path('api/posts/create/', views.api_create_post, name='api_create_post'),
    path('api/posts/<int:post_id>/like/', views.api_toggle_like, name='api_toggle_like'),
    path('api/posts/<int:post_id>/comment/', views.api_add_comment, name='api_add_comment'),
    path('api/users/<int:user_id>/follow/', views.api_toggle_follow, name='api_toggle_follow'),
]
