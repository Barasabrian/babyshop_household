document.addEventListener('DOMContentLoaded', function () {
  // Initialize tooltips
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // Initialize popovers
  const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
  popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl);
  });

  // Back to top button
  const backToTopButton = document.querySelector('.back-to-top');
  if (backToTopButton) {
    window.addEventListener('scroll', function () {
      if (window.pageYOffset > 300) {
        backToTopButton.style.display = 'block';
      } else {
        backToTopButton.style.display = 'none';
      }
    });

    backToTopButton.addEventListener('click', function (e) {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // Quantity controls
  document.querySelectorAll('.quantity-btn').forEach(button => {
    button.addEventListener('click', function (e) {
      e.preventDefault();
      const input = this.closest('.quantity-input-group').querySelector('.quantity-input');
      let value = parseInt(input.value);
      const max = parseInt(input.getAttribute('max')) || 20;
      const min = parseInt(input.getAttribute('min')) || 1;

      if (this.classList.contains('minus') && value > min) {
        input.value = value - 1;
      } else if (this.classList.contains('plus') && value < max) {
        input.value = value + 1;
      }

      // Dispatch change event
      input.dispatchEvent(new Event('change'));
    });
  });

  // Image gallery for product detail
  const thumbnails = document.querySelectorAll('.product-thumbnail');
  const mainImage = document.querySelector('.product-image-main');

  if (thumbnails && mainImage) {
    thumbnails.forEach(thumbnail => {
      thumbnail.addEventListener('click', function () {
        // Update main image
        mainImage.src = this.src;

        // Update active thumbnail
        thumbnails.forEach(t => t.classList.remove('active'));
        this.classList.add('active');
      });
    });
  }

  // Add to cart animation
  document.querySelectorAll('.add-to-cart-btn').forEach(button => {
    button.addEventListener('click', function () {
      const productCard = this.closest('.product-card');
      if (productCard) {
        productCard.classList.add('added-to-cart');

        setTimeout(() => {
          productCard.classList.remove('added-to-cart');
        }, 1000);
      }

      // Update cart count
      const cartBadge = document.querySelector('.cart-badge');
      if (cartBadge) {
        const currentCount = parseInt(cartBadge.textContent) || 0;
        cartBadge.textContent = currentCount + 1;

        // Add animation
        cartBadge.classList.add('animate-bounce');
        setTimeout(() => {
          cartBadge.classList.remove('animate-bounce');
        }, 1000);
      }
    });
  });

  // Dark mode toggle
  const darkModeToggle = document.getElementById('darkModeToggle');
  if (darkModeToggle) {
    // Check for saved preference
    const savedMode = localStorage.getItem('darkMode');
    if (savedMode === 'true') {
      document.documentElement.setAttribute('data-theme', 'dark');
      darkModeToggle.checked = true;
    }

    darkModeToggle.addEventListener('change', function () {
      if (this.checked) {
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('darkMode', 'true');
      } else {
        document.documentElement.removeAttribute('data-theme');
        localStorage.setItem('darkMode', 'false');
      }
    });
  }

  // Product search
  const searchInput = document.querySelector('input[name="q"]');
  if (searchInput) {
    searchInput.addEventListener('input', function () {
      const searchTerm = this.value.trim();
      if (searchTerm.length > 2) {
        // You could implement live search here with fetch API
      }
    });
  }

  // Form validation
  document.querySelectorAll('form.needs-validation').forEach(form => {
    form.addEventListener('submit', function (event) {
      if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
      }

      form.classList.add('was-validated');
    }, false);
  });
});

// AJAX helper function
function ajaxRequest(method, url, data, successCallback, errorCallback) {
  const xhr = new XMLHttpRequest();
  xhr.open(method, url, true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));

  xhr.onload = function () {
    if (xhr.status >= 200 && xhr.status < 300) {
      const response = JSON.parse(xhr.responseText);
      successCallback(response);
    } else {
      errorCallback(xhr.statusText);
    }
  };

  xhr.onerror = function () {
    errorCallback('Network error');
  };

  xhr.send(JSON.stringify(data));
}

// Get CSRF token from cookies
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

// Debounce function for performance optimization
function debounce(func, wait, immediate) {
  let timeout;
  return function () {
    const context = this, args = arguments;
    const later = function () {
      timeout = null;
      if (!immediate) func.apply(context, args);
    };
    const callNow = immediate && !timeout;
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
    if (callNow) func.apply(context, args);
  };
}