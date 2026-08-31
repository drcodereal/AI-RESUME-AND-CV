document.addEventListener('DOMContentLoaded', () => {
  const loader = document.getElementById('page-loader');
  window.setTimeout(() => loader?.classList.add('hidden'), 500);

  // Dashboard sidebar (hamburger / three-line menu)
  const sidebar = document.getElementById('appSidebar');
  const sidebarToggle = document.getElementById('sidebarToggle');
  const sidebarClose = document.getElementById('sidebarClose');
  const sidebarOverlay = document.getElementById('sidebarOverlay');

  const openSidebar = () => {
    sidebar?.classList.add('open');
    sidebarOverlay?.classList.add('show');
    sidebarToggle?.setAttribute('aria-expanded', 'true');
    sidebar?.setAttribute('aria-hidden', 'false');
    document.body.classList.add('sidebar-open');
  };
  const closeSidebar = () => {
    sidebar?.classList.remove('open');
    sidebarOverlay?.classList.remove('show');
    sidebarToggle?.setAttribute('aria-expanded', 'false');
    sidebar?.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('sidebar-open');
  };
  sidebarToggle?.addEventListener('click', () => {
    sidebar?.classList.contains('open') ? closeSidebar() : openSidebar();
  });
  sidebarClose?.addEventListener('click', closeSidebar);
  sidebarOverlay?.addEventListener('click', closeSidebar);
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeSidebar(); });
  sidebar?.querySelectorAll('a.sidebar-link').forEach(a => a.addEventListener('click', closeSidebar));

  // Reusable full-screen "working" overlay - shown while a form POSTs to the
  // server (e.g. generating or analyzing a resume) so the wait feels alive
  // instead of a frozen page. The overlay just plays; it never blocks the
  // real submit - the browser navigates away once the server responds.
  window.startWorkOverlay = (title, subtitle, steps) => {
    const overlay = document.getElementById('workOverlay');
    if (!overlay) return;
    document.getElementById('workTitle').textContent = title || 'Working…';
    document.getElementById('workSubtitle').textContent = subtitle || '';
    const list = document.getElementById('workSteps');
    list.innerHTML = (steps || []).map(s => `<li>${s}</li>`).join('');
    overlay.classList.add('show');
    overlay.setAttribute('aria-hidden', 'false');
    const items = list.querySelectorAll('li');
    let i = 0;
    const advance = () => {
      items.forEach((el, idx) => {
        el.classList.toggle('active', idx === i);
        el.classList.toggle('done', idx < i);
      });
      i++;
      if (i <= items.length) window.setTimeout(advance, 650);
    };
    advance();
  };

  // Reveal on scroll
  const revealItems = document.querySelectorAll('.reveal, .reveal-left, .reveal-right');
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08 });
    revealItems.forEach(el => observer.observe(el));
  } else revealItems.forEach(el => el.classList.add('visible'));

  // Magnetic buttons: nudges toward the pointer within range, springs back on leave
  document.querySelectorAll('.btn, .nav-cta').forEach(btn => {
    if (window.matchMedia('(hover: none)').matches) return;
    btn.addEventListener('pointermove', e => {
      const r = btn.getBoundingClientRect();
      const x = e.clientX - (r.left + r.width / 2);
      const y = e.clientY - (r.top + r.height / 2);
      btn.style.transform = `translate(${x * 0.18}px, ${y * 0.35 - 3}px)`;
    });
    btn.addEventListener('pointerleave', () => { btn.style.transform = ''; });
  });

  // Forms loading state
  document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', () => {
      const btn = form.querySelector('button[type="submit"]');
      if (btn && !btn.disabled) {
        btn.disabled = true;
        btn.dataset.originalText = btn.innerHTML;
        btn.innerHTML = '<span class="button-spinner"></span> Processing...';
      }
      loader?.classList.remove('hidden');
    });
  });

  // File dropzone
  const fileInput = document.querySelector('input[type="file"]');
  const dropzone = document.getElementById('dropzone');
  const selectedFile = document.getElementById('selectedFile');
  const setFile = files => {
    if (!files?.length) return;
    const file = files[0];
    selectedFile && (selectedFile.textContent = `✓ ${file.name}`);
    dropzone?.classList.add('has-file');
  };
  fileInput?.addEventListener('change', e => setFile(e.target.files));
  ['dragenter','dragover'].forEach(type => dropzone?.addEventListener(type, e => { e.preventDefault(); dropzone.classList.add('drag-over'); }));
  ['dragleave','drop'].forEach(type => dropzone?.addEventListener(type, e => { e.preventDefault(); dropzone.classList.remove('drag-over'); }));
  dropzone?.addEventListener('drop', e => { if (fileInput && e.dataTransfer.files.length) { fileInput.files = e.dataTransfer.files; setFile(e.dataTransfer.files); } });

  // Template selector
  const templateStatus = document.getElementById('templateStatus');
  document.querySelectorAll('.template-option input').forEach(input => input.addEventListener('change', () => {
    document.querySelectorAll('.template-option').forEach(x => x.classList.remove('selected'));
    input.closest('.template-option')?.classList.add('selected');
    if (templateStatus) templateStatus.textContent = input.value.charAt(0).toUpperCase() + input.value.slice(1);
  }));

  // Character counter
  document.querySelectorAll('[data-count]').forEach(field => {
    const target = document.getElementById(field.dataset.count);
    const update = () => { if (target) target.textContent = `${field.value.length} characters`; };
    field.addEventListener('input', update); update();
  });

  // Flash close
  document.querySelector('.flash-close')?.addEventListener('click', e => e.currentTarget.parentElement.remove());

  // Subtle card tilt
  document.querySelectorAll('.feature-card, .hero-card').forEach(card => {
    card.addEventListener('pointermove', e => {
      if (window.innerWidth < 900) return;
      const r = card.getBoundingClientRect();
      const x = (e.clientX - r.left) / r.width - .5;
      const y = (e.clientY - r.top) / r.height - .5;
      card.style.transform = `perspective(900px) rotateX(${(-y * 3).toFixed(2)}deg) rotateY(${(x * 4).toFixed(2)}deg) translateY(-5px)`;
    });
    card.addEventListener('pointerleave', () => card.style.transform = '');
  });
});
