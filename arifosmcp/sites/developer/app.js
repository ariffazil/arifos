/* arifOS MCP — Developer Portal JS */

// ── Theme Toggle ──────────────────────────────────────────
(function () {
  const html = document.documentElement;
  const toggle = document.querySelector('[data-theme-toggle]');
  let theme = html.getAttribute('data-theme') || 'dark';

  function applyTheme(t) {
    theme = t;
    html.setAttribute('data-theme', t);
    if (toggle) {
      toggle.setAttribute('aria-label', `Switch to ${t === 'dark' ? 'light' : 'dark'} mode`);
      toggle.innerHTML = t === 'dark'
        ? '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>'
        : '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
    }
  }

  if (toggle) {
    toggle.addEventListener('click', () => applyTheme(theme === 'dark' ? 'light' : 'dark'));
  }
  applyTheme(theme);
})();

// ── Live Health Polling ───────────────────────────────────
async function pollHealth() {
  const dot = document.getElementById('statusDot');
  const label = document.getElementById('statusLabel');
  const version = document.getElementById('statusVersion');
  if (!dot) return;

  try {
    const res = await fetch('https://arifosmcp.arif-fazil.com/health', {
      method: 'GET',
      mode: 'cors',
      cache: 'no-store',
      signal: AbortSignal.timeout(5000)
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    dot.className = 'status-dot healthy';
    label.textContent = `${data.status || 'healthy'} · ${data.tools_loaded || 12} tools`;
    version.textContent = data.version || '2026.03.13-FORGED';

    // Update dashboard metrics if data available
    if (data.version) {
      const vEl = document.querySelector('.footer-version');
      if (vEl) vEl.textContent = `${data.version} · AGPL-3.0`;
    }
  } catch (e) {
    dot.className = 'status-dot degraded';
    label.textContent = 'Unreachable from browser (CORS) — use /health directly';
    version.textContent = '2026.03.13-FORGED';
  }
}

pollHealth();
setInterval(pollHealth, 30000);

// ── Tab Switching ─────────────────────────────────────────
document.querySelectorAll('[data-tab]').forEach(btn => {
  btn.addEventListener('click', () => {
    const tabId = btn.getAttribute('data-tab');
    const parent = btn.closest('.tabs');
    if (!parent) return;

    parent.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('tab-btn--active'));
    parent.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('tab-panel--active'));

    btn.classList.add('tab-btn--active');
    const panel = document.getElementById(`tab-${tabId}`);
    if (panel) panel.classList.add('tab-panel--active');
  });
});

// ── Copy Buttons ──────────────────────────────────────────
document.querySelectorAll('.copy-btn').forEach(btn => {
  btn.addEventListener('click', async () => {
    const targetId = btn.getAttribute('data-copy');
    const pre = document.getElementById(targetId);
    if (!pre) return;

    // Strip HTML tags to get plain text
    const text = pre.innerText || pre.textContent;
    try {
      await navigator.clipboard.writeText(text);
      const orig = btn.textContent;
      btn.textContent = 'Copied!';
      btn.classList.add('copied');
      setTimeout(() => { btn.textContent = orig; btn.classList.remove('copied'); }, 2000);
    } catch (e) {
      // Fallback: select text
      const range = document.createRange();
      range.selectNodeContents(pre);
      window.getSelection().removeAllRanges();
      window.getSelection().addRange(range);
    }
  });
});

// ── Nav scroll active state ───────────────────────────────
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav-link:not(.nav-link-external)');

const observer = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      const id = e.target.id;
      navLinks.forEach(link => {
        link.style.color = link.getAttribute('href') === `#${id}`
          ? 'var(--color-accent)' : '';
      });
    }
  });
}, { rootMargin: '-20% 0px -70% 0px' });

sections.forEach(s => observer.observe(s));

// ── Animate numbers in hero stats ────────────────────────
function animateValue(el, target, duration = 800) {
  if (!el || isNaN(target)) return;
  const start = 0;
  const startTime = performance.now();
  function update(now) {
    const progress = Math.min((now - startTime) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    el.textContent = Math.round(start + (target - start) * eased).toString();
    if (progress < 1) requestAnimationFrame(update);
  }
  requestAnimationFrame(update);
}

// ── Entrance animation for cards ─────────────────────────
const cardObserver = new IntersectionObserver(entries => {
  entries.forEach((e, i) => {
    if (e.isIntersecting) {
      e.target.style.opacity = '1';
      e.target.style.transform = 'translateY(0)';
      cardObserver.unobserve(e.target);
    }
  });
}, { threshold: 0, rootMargin: '0px 0px -5% 0px' });

document.querySelectorAll('.tool-card, .floor-card, .doc-card, .endpoint-card').forEach((card, i) => {
  card.style.opacity = '0';
  card.style.transform = 'translateY(16px)';
  card.style.transition = `opacity 0.4s ease ${i * 0.04}s, transform 0.4s ease ${i * 0.04}s, border-color 180ms cubic-bezier(0.16,1,0.3,1), box-shadow 180ms cubic-bezier(0.16,1,0.3,1)`;
  cardObserver.observe(card);
});
