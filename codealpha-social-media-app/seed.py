import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_proj.settings')
django.setup()

from django.contrib.auth.models import User
from social_app.models import Profile, Post, Comment, Follow

def seed_database():
    print("Seeding database...")

    # Create Users
    users_data = [
        {'username': 'alex_dev', 'password': 'password123', 'bio': 'Full-stack software engineer & open source enthusiast', 'location': 'San Francisco, CA'},
        {'username': 'sarah_design', 'password': 'password123', 'bio': 'UI/UX designer crafting beautiful digital experiences', 'location': 'London, UK'},
        {'username': 'tech_lead_jon', 'password': 'password123', 'bio': 'Building distributed systems & scaling web applications', 'location': 'Berlin, Germany'},
    ]

    users = []
    for udata in users_data:
        user, created = User.objects.get_or_create(username=udata['username'])
        if created:
            user.set_password(udata['password'])
            user.save()
        user.profile.bio = udata['bio']
        user.profile.location = udata['location']
        user.profile.save()
        users.append(user)

    alex, sarah, jon = users

    # Create Follows
    Follow.objects.get_or_create(follower=alex, following=sarah)
    Follow.objects.get_or_create(follower=alex, following=jon)
    Follow.objects.get_or_create(follower=sarah, following=alex)

    # Create Posts
    posts_data = [
        {
            'author': alex,
            'content': 'Just launched our new full-stack Django social platform! Super excited about the sleek glassmorphism design and AJAX instant interactions.',
            'likes': [sarah, jon]
        },
        {
            'author': sarah,
            'content': 'Design tip of the day: Subtle micro-animations and harmonious HSL color palettes can elevate your web app from good to extraordinary!',
            'likes': [alex]
        },
        {
            'author': jon,
            'content': 'Python 3.13 and Django 6.0 performance benchmarks are looking impressive! Loving the speed improvements in view rendering.',
            'likes': [alex, sarah]
        }
    ]

    for pdata in posts_data:
        post, _ = Post.objects.get_or_create(author=pdata['author'], content=pdata['content'])
        for like_user in pdata['likes']:
            post.likes.add(like_user)

    print("Database seeded successfully with users, posts, and follow relationships!")

if __name__ == '__main__':
    seed_database()
