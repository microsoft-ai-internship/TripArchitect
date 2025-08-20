 // DOM Elements
    const loginForm = document.getElementById('login-form');
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    const passwordToggle = document.querySelector('.password-toggle');
    const passwordInput = document.getElementById('password');

    // Theme Toggle
    function toggleTheme() {
      document.documentElement.classList.toggle('dark');
      const isDark = document.documentElement.classList.contains('dark');
      themeIcon.className = isDark ? 'fas fa-moon' : 'fas fa-sun';
      localStorage.setItem('theme', isDark ? 'dark' : 'light');
    }

    // Password Toggle
    function togglePasswordVisibility() {
      const icon = passwordToggle.querySelector('i');
      if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        icon.classList.replace('fa-eye', 'fa-eye-slash');
      } else {
        passwordInput.type = 'password';
        icon.classList.replace('fa-eye-slash', 'fa-eye');
      }
    }

    // Form Validation
    function validateEmail(email) {
      const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return re.test(String(email).toLowerCase());
    }

    function showError(input, message) {
      const formGroup = input.closest('.input-group');
      const errorElement = formGroup.querySelector('.error-message') ||
        document.createElement('div');

      errorElement.className = 'error-message';
      errorElement.textContent = message;

      if (!formGroup.querySelector('.error-message')) {
        formGroup.appendChild(errorElement);
      }

      input.classList.add('input-error');
    }

    function clearError(input) {
      const formGroup = input.closest('.input-group');
      const errorElement = formGroup.querySelector('.error-message');

      if (errorElement) {
        errorElement.remove();
      }

      input.classList.remove('input-error');
    }

    // Form Submission
    async function handleLogin(e) {
      e.preventDefault();

      const email = document.getElementById('email').value.trim();
      const password = document.getElementById('password').value.trim();
      const rememberMe = document.getElementById('remember-me').checked;

      // Validate inputs
      let isValid = true;

      if (!email) {
        showError(document.getElementById('email'), 'E-posta adresi gereklidir');
        isValid = false;
      } else if (!validateEmail(email)) {
        showError(document.getElementById('email'), 'Geçerli bir e-posta adresi girin');
        isValid = false;
      } else {
        clearError(document.getElementById('email'));
      }

      if (!password) {
        showError(document.getElementById('password'), 'Şifre gereklidir');
        isValid = false;
      } else if (password.length < 6) {
        showError(document.getElementById('password'), 'Şifre en az 6 karakter olmalıdır');
        isValid = false;
      } else {
        clearError(document.getElementById('password'));
      }

      if (!isValid) return;

      // Simulate API call
      try {
        // Show loading state
        const submitBtn = loginForm.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Giriş Yapılıyor...';
        submitBtn.disabled = true;

        // Simulate network request
        await new Promise(resolve => setTimeout(resolve, 1500));

        // For demo purposes, just redirect to index page
        window.location.href = 'index.html';

      } catch (error) {
        console.error('Login error:', error);
        alert('Giriş başarısız: ' + (error.message || 'Bilinmeyen hata'));

        // Reset button state
        const submitBtn = loginForm.querySelector('button[type="submit"]');
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
      }
    }

    // Initialize
    function init() {
      // Load theme preference
      if (localStorage.getItem('theme') === 'dark' ||
          (window.matchMedia('(prefers-color-scheme: dark)').matches && !localStorage.getItem('theme'))) {
        document.documentElement.classList.add('dark');
        themeIcon.className = 'fas fa-sun';
      }

      // Event listeners
      themeToggle.addEventListener('click', toggleTheme);
      passwordToggle.addEventListener('click', togglePasswordVisibility);
      loginForm.addEventListener('submit', handleLogin);
    }

    // Run when DOM is loaded
    document.addEventListener('DOMContentLoaded', init);