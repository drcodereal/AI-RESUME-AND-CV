document.addEventListener('DOMContentLoaded', () => {
  /* ---------- register form: live password-match indicator ---------- */
  const registerForm = document.getElementById('registerForm');
  if (registerForm) {
    const pass = document.getElementById('regPassword');
    const confirm = document.getElementById('regConfirm');
    const matchMsg = document.getElementById('matchMsg');

    const checkMatch = () => {
      if (!confirm.value) { matchMsg.textContent = ''; matchMsg.className = 'match-msg'; return true; }
      const ok = pass.value === confirm.value;
      matchMsg.textContent = ok ? '✓ Passwords match' : '✕ Passwords do not match';
      matchMsg.className = 'match-msg ' + (ok ? 'match-ok' : 'match-bad');
      return ok;
    };
    pass?.addEventListener('input', checkMatch);
    confirm?.addEventListener('input', checkMatch);

    registerForm.addEventListener('submit', e => {
      if (!checkMatch()) { /* let native "required"/minlength validation still submit; just flag mismatch visually */ }
      const btn = registerForm.querySelector('button[type="submit"]');
      btn?.classList.add('is-loading');
    });
  }

  /* ---------- login form: submit spinner ---------- */
  const loginForm = document.getElementById('loginForm');
  if (loginForm) {
    loginForm.addEventListener('submit', () => {
      const errorEl = document.getElementById('authError');
      if (errorEl) { errorEl.textContent = ''; }
      const btn = loginForm.querySelector('button[type="submit"]');
      btn?.classList.add('is-loading');
    });
    const huskyEl = document.getElementById('huskyMascot');
    if (huskyEl && document.getElementById('authError')?.textContent.trim()) {
      huskyEl.classList.add('shake');
      setTimeout(() => huskyEl.classList.remove('shake'), 500);
    }
  }

  /* ---------- husky mascot reactions ---------- */
  const husky = document.getElementById('huskyMascot');
  if (husky) {
    const greetVariants = ['greet-a', 'greet-b', 'greet-c'];
    let greetTimer;

    const triggerGreeting = () => {
      husky.classList.remove(...greetVariants, 'greeting');
      void husky.offsetWidth; // restart CSS animation
      const variant = greetVariants[Math.floor(Math.random() * greetVariants.length)];
      husky.classList.add('greeting', variant);
      clearTimeout(greetTimer);
      greetTimer = setTimeout(() => husky.classList.remove('greeting', variant), 700);
    };

    document.querySelectorAll('input[data-role="greet"]').forEach(field => {
      field.addEventListener('input', triggerGreeting);
      field.addEventListener('focus', triggerGreeting);
    });

    document.querySelectorAll('input[data-role="password"]').forEach(field => {
      field.addEventListener('focus', () => husky.classList.add('hide-eyes'));
      field.addEventListener('input', () => husky.classList.add('hide-eyes'));
      field.addEventListener('blur', () => husky.classList.remove('hide-eyes'));
    });
  }

  /* ---------- show/hide password ---------- */
  document.querySelectorAll('.toggle-pass').forEach(btn => {
    btn.addEventListener('click', () => {
      const input = document.getElementById(btn.dataset.target);
      if (!input) return;
      input.type = input.type === 'password' ? 'text' : 'password';
      btn.classList.toggle('showing');
      btn.textContent = input.type === 'password' ? '👁' : '🙈';
    });
  });
});
