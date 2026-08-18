document.addEventListener('DOMContentLoaded', function () {
  console.log('CyberStore frontend logic initialized.');

  // CSRF helper function
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

  // Toast System
  window.showToast = function (message, type = 'success') {
    let container = document.getElementById('toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'toast-container';
      document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
      <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
      </svg>
      <span>${message}</span>
    `;

    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(100%)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  };

  // Intercept Add to Cart Forms for AJAX execution
  const addCartForms = document.querySelectorAll('.ajax-add-cart');
  addCartForms.forEach(form => {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      const url = this.action;
      const formData = new FormData(this);

      fetch(url, {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': csrftoken
        },
        body: formData
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          showToast(data.message, 'success');
          // Update cart badges
          const badges = document.querySelectorAll('.cart-badge');
          badges.forEach(badge => {
            badge.textContent = data.cart_count;
            badge.style.transform = 'scale(1.25)';
            setTimeout(() => badge.style.transform = 'scale(1)', 200);
          });
        }
      })
      .catch(err => {
        console.error('Add to cart error:', err);
        // Fallback to standard form submission
        this.submit();
      });
    });
  });

  // Category filter smooth navigation
  const catPills = document.querySelectorAll('.cat-pill');
  catPills.forEach(pill => {
    pill.addEventListener('click', function () {
      catPills.forEach(p => p.classList.remove('active'));
      this.classList.add('active');
    });
  });
});
