// Helper to get Django CSRF Cookie
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// Floating Toast Notification
function showToast(msg, type = 'success') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerText = msg;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

// Handle Like Toggle
async function toggleLike(postId) {
  const btn = document.getElementById(`like-btn-${postId}`);
  const countSpan = document.getElementById(`like-count-${postId}`);
  
  try {
    const res = await fetch(`/api/posts/${postId}/like/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
    
    if (!res.ok) throw new Error('Like request failed');
    const data = await res.json();
    
    countSpan.innerText = data.count;
    if (data.liked) {
      btn.classList.add('active');
      btn.querySelector('.heart-icon').innerText = '❤️';
      showToast('Liked post! ❤️');
    } else {
      btn.classList.remove('active');
      btn.querySelector('.heart-icon').innerText = '🤍';
    }
  } catch (err) {
    showToast('Failed to like post', 'error');
  }
}

// Toggle Comments Box Visibility
function toggleComments(postId) {
  const box = document.getElementById(`comments-section-${postId}`);
  if (box.style.display === 'none' || !box.style.display) {
    box.style.display = 'block';
  } else {
    box.style.display = 'none';
  }
}

// Add Comment via AJAX
async function submitComment(event, postId) {
  event.preventDefault();
  const input = document.getElementById(`comment-input-${postId}`);
  const content = input.value.trim();
  if (!content) return;

  try {
    const res = await fetch(`/api/posts/${postId}/comment/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: new URLSearchParams({ content })
    });

    if (!res.ok) throw new Error('Failed to post comment');
    const data = await res.json();

    const list = document.getElementById(`comments-list-${postId}`);
    const commentItem = document.createElement('div');
    commentItem.className = 'comment-item';
    commentItem.innerHTML = `
      <img src="${data.avatar_url}" class="avatar-xs" alt="${data.author}">
      <div>
        <a href="/profile/${data.author}/" class="comment-author">${data.author}</a>
        <span style="font-size:0.75rem;color:var(--text-muted);margin-left:6px;">${data.created_at}</span>
        <div class="comment-text">${data.content}</div>
      </div>
    `;
    list.appendChild(commentItem);

    // Update comment counter
    const countSpan = document.getElementById(`comment-count-${postId}`);
    if (countSpan) countSpan.innerText = data.total_comments;

    input.value = '';
    showToast('Comment added!');
  } catch (err) {
    showToast('Failed to post comment', 'error');
  }
}

// Handle Follow / Unfollow Toggle
async function toggleFollow(userId, btnId) {
  const btn = document.getElementById(btnId);
  try {
    const res = await fetch(`/api/users/${userId}/follow/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });

    if (!res.ok) throw new Error('Follow request failed');
    const data = await res.json();

    if (data.following) {
      btn.innerText = 'Following ✔️';
      btn.className = 'btn btn-secondary btn-sm';
      showToast('User followed!');
    } else {
      btn.innerText = 'Follow +';
      btn.className = 'btn btn-primary btn-sm';
      showToast('Unfollowed user', 'info');
    }

    const followersCountEl = document.getElementById('followers-count');
    if (followersCountEl) followersCountEl.innerText = data.followers_count;
  } catch (err) {
    showToast('Failed to toggle follow status', 'error');
  }
}

// Create Post via AJAX
async function createPost(event) {
  event.preventDefault();
  const input = document.getElementById('create-post-content');
  const content = input.value.trim();
  if (!content) return showToast('Please enter post text', 'error');

  try {
    const res = await fetch('/api/posts/create/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: new URLSearchParams({ content })
    });

    if (!res.ok) throw new Error('Failed to create post');
    const data = await res.json();

    input.value = '';
    showToast('Post published successfully! 🎉');
    setTimeout(() => { window.location.reload(); }, 600);
  } catch (err) {
    showToast('Failed to publish post', 'error');
  }
}
