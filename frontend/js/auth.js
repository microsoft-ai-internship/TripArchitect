// DOM Elements
    const registerForm = document.getElementById('register-form');
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    const passwordToggle = document.querySelector('.password-toggle');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm-password');
    const strengthBar = document.getElementById('strength-bar');
    const strengthText = document.getElementById('strength-text');
    const termsCheckbox = document.getElementById('terms');

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

    // Password Strength Check
    function checkPasswordStrength(password) {
      const strength = {
        0: { text: "Çok zayıf", color: "#FF4D4F", width: "25%" },
        1: { text: "Zayıf", color: "#FF4D4F", width: "25%" },
        2: { text: "Orta", color: "#FAAD14", width: "50%" },
        3: { text: "Güçlü", color: "#52C41A", width: "75%" },
        4: { text: "Çok güçlü", color: "#34A853", width: "100%" }
      };

      let score = 0;
      if (!password) return strength[0];

      // Uzunluk kontrolü
      if (password.length > 6) score++;
      if (password.length > 10) score++;

      // Karakter çeşitliliği
      if (/[A-Z]/.test(password)) score++;
      if (/[0-9]/.test(password)) score++;
      if (/[^A-Za-z0-9]/.test(password)) score++;

      return strength[Math.min(score, 4)];
    }

    // Form Validation
    function validateEmail(email) {
      const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return re.test(String(email).toLowerCase());
    }

    function validatePassword(password) {
      return password.length >= 6;
    }

    function passwordsMatch(password, confirmPassword) {
      return password === confirmPassword;
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
    async function handleRegister(e) {
      e.preventDefault();

      const fullname = document.getElementById('fullname').value.trim();
      const email = document.getElementById('email').value.trim();
      const password = document.getElementById('password').value.trim();
      const confirmPassword = document.getElementById('confirm-password').value.trim();
      const termsAccepted = document.getElementById('terms').checked;

      // Validate inputs
      let isValid = true;

      if (!fullname) {
        showError(document.getElementById('fullname'), 'Ad soyad gereklidir');
        isValid = false;
      } else {
        clearError(document.getElementById('fullname'));
      }

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
      } else if (!validatePassword(password)) {
        showError(document.getElementById('password'), 'Şifre en az 6 karakter olmalıdır');
        isValid = false;
      } else {
        clearError(document.getElementById('password'));
      }

      if (!confirmPassword) {
        showError(document.getElementById('confirm-password'), 'Şifre onayı gereklidir');
        isValid = false;
      } else if (!passwordsMatch(password, confirmPassword)) {
        showError(document.getElementById('confirm-password'), 'Şifreler eşleşmiyor');
        isValid = false;
      } else {
        clearError(document.getElementById('confirm-password'));
      }

      if (!termsAccepted) {
        alert('Kullanım koşullarını kabul etmelisiniz');
        isValid = false;
      }

      if (!isValid) return;

      // Simulate API call
      try {
        // Show loading state
        const submitBtn = registerForm.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Kayıt Olunuyor...';
        submitBtn.disabled = true;

        // Simulate network request
        await new Promise(resolve => setTimeout(resolve, 1500));

        // For demo purposes, just redirect to login page
        window.location.href = 'login.html?registered=true';

      } catch (error) {
        console.error('Registration error:', error);
        alert('Kayıt başarısız: ' + (error.message || 'Bilinmeyen hata'));

        // Reset button state
        const submitBtn = registerForm.querySelector('button[type="submit"]');
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

      // Password strength indicator
      passwordInput.addEventListener('input', function() {
        const strength = checkPasswordStrength(this.value);
        strengthBar.style.width = strength.width;
        strengthBar.style.backgroundColor = strength.color;
        strengthText.textContent = `Şifre gücü: ${strength.text}`;
      });

      // Event listeners
      themeToggle.addEventListener('click', toggleTheme);
      passwordToggle.addEventListener('click', togglePasswordVisibility);
      registerForm.addEventListener('submit', handleRegister);
    }

    // Run when DOM is loaded
    document.addEventListener('DOMContentLoaded', init);