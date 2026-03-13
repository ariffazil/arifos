/* arifOS MCP — Developer Portal JS (H1 Higher Intelligence State) */

// ═════════════════════════════════════════════════════════════════════════════
// H1 STATE INITIALIZATION
// ═════════════════════════════════════════════════════════════════════════════
const H1State = {
  telemetry: { exploration: 0, entropy: 0, eureka: 0 },
  w3Score: 0,
  metabolicStage: '000_INIT',
  floorScores: {},
  sessionActive: false,
  initTimestamp: Date.now()
};

// ── Theme Toggle ────────────────────────────────────────────────────────────
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
    // Emit theme change for 3E visualizations
    document.dispatchEvent(new CustomEvent('h1:themechange', { detail: { theme: t } }));
  }

  if (toggle) {
    toggle.addEventListener('click', () => applyTheme(theme === 'dark' ? 'light' : 'dark'));
  }
  applyTheme(theme);
})();

// ── H1 Live Health Polling with 3E Telemetry ────────────────────────────────
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

    // H1: Update dashboard metrics if available
    if (data.version) {
      const vEl = document.querySelector('.footer-version');
      if (vEl) vEl.textContent = `${data.version} · AGPL-3.0`;
    }

    // H1: Update constitutional metrics if provided
    if (data.w3_score !== undefined) {
      updateW3Gauge(data.w3_score);
    }
    if (data.metabolic_stage) {
      updateMetabolicStage(data.metabolic_stage);
    }

    H1State.sessionActive = true;
    document.dispatchEvent(new CustomEvent('h1:healthupdate', { detail: data }));

  } catch (e) {
    dot.className = 'status-dot degraded';
    label.textContent = 'Unreachable from browser (CORS) — use /health directly';
    version.textContent = '2026.03.13-FORGED';
    H1State.sessionActive = false;
  }
}

pollHealth();
setInterval(pollHealth, 30000);

// ── H1 3E Telemetry Visualization ───────────────────────────────────────────
function render3ETelemetry(containerId, telemetry) {
  const container = document.getElementById(containerId);
  if (!container) return;

  const { exploration = {}, entropy = {}, eureka = {} } = telemetry;

  container.innerHTML = `
    <div class="telem-grid">
      <div class="telem-card telem-exploration">
        <div class="telem-header">
          <span class="telem-icon">🔭</span>
          <span class="telem-name">Exploration</span>
        </div>
        <div class="telem-metric">
          <span class="telem-val">${exploration.sources_consulted || 0}</span>
          <span class="telem-unit">sources</span>
        </div>
        <div class="telem-bar">
          <div class="telem-fill" style="width: ${Math.min((exploration.breadth_score || 0) * 100, 100)}%"></div>
        </div>
        <div class="telem-label">Breadth: ${((exploration.breadth_score || 0) * 100).toFixed(0)}%</div>
      </div>
      
      <div class="telem-card telem-entropy">
        <div class="telem-header">
          <span class="telem-icon">⚡</span>
          <span class="telem-name">Entropy</span>
        </div>
        <div class="telem-metric">
          <span class="telem-val">${((entropy.uncertainty_index || 0) * 100).toFixed(1)}</span>
          <span class="telem-unit">%</span>
        </div>
        <div class="telem-bar telem-bar-entropy">
          <div class="telem-fill" style="width: ${Math.min((entropy.uncertainty_index || 0) * 100, 100)}%"></div>
        </div>
        <div class="telem-label">${entropy.contradiction_count || 0} contradictions</div>
      </div>
      
      <div class="telem-card telem-eureka">
        <div class="telem-header">
          <span class="telem-icon">💡</span>
          <span class="telem-name">Eureka</span>
        </div>
        <div class="telem-metric">
          <span class="telem-val">${((eureka.novelty_score || 0) * 100).toFixed(0)}</span>
          <span class="telem-unit">% novel</span>
        </div>
        <div class="telem-bar telem-bar-eureka">
          <div class="telem-fill" style="width: ${Math.min((eureka.novelty_score || 0) * 100, 100)}%"></div>
        </div>
        <div class="telem-label">${eureka.crystallisation_flag ? '✓ Crystallized' : '○ Forming'}</div>
      </div>
    </div>
  `;
}

// ── H1 W3 Tri-Witness Gauge ────────────────────────────────────────────────
function updateW3Gauge(w3Score) {
  H1State.w3Score = w3Score;
  const gauge = document.getElementById('w3Gauge');
  const value = document.getElementById('w3Value');
  const verdict = document.getElementById('w3Verdict');
  
  if (!gauge || !value || !verdict) return;

  // W3 = (w_H·s_H × w_A·s_A × w_E·s_E)^(1/3)
  const percentage = Math.min(w3Score * 100, 100);
  gauge.style.setProperty('--w3-progress', `${percentage}%`);
  value.textContent = w3Score.toFixed(3);

  // Verdict thresholds
  let verdictClass = 'verdict-void';
  let verdictText = '888_HOLD';
  
  if (w3Score >= 0.95) {
    verdictClass = 'verdict-seal';
    verdictText = 'SEAL';
  } else if (w3Score >= 0.75) {
    verdictClass = 'verdict-partial';
    verdictText = 'PARTIAL';
  } else if (w3Score >= 0.50) {
    verdictClass = 'verdict-sabar';
    verdictText = 'SABAR';
  }
  
  verdict.className = `w3-verdict ${verdictClass}`;
  verdict.textContent = verdictText;
}

// ── H1 Metabolic Stage Indicator ────────────────────────────────────────────
function updateMetabolicStage(stage) {
  H1State.metabolicStage = stage;
  const indicator = document.getElementById('metabolicStage');
  if (!indicator) return;

  // Parse stage number (000_INIT → 000)
  const stageNum = stage.match(/(\d+)/)?.[0] || '000';
  const stageName = stage.replace(/^\d+_/, '');
  
  indicator.innerHTML = `
    <div class="stage-indicator">
      <div class="stage-num">${stageNum}</div>
      <div class="stage-name">${stageName}</div>
      <div class="stage-bar">
        ${Array.from({length: 11}, (_, i) => {
          const num = String(i * 111).padStart(3, '0');
          const active = parseInt(num) <= parseInt(stageNum);
          return `<div class="stage-dot ${active ? 'active' : ''}"></div>`;
        }).join('')}
      </div>
    </div>
  `;
}

// ── H1 Constitutional Floor Monitor ─────────────────────────────────────────
function updateFloorMonitor(floorScores) {
  H1State.floorScores = floorScores || {};
  const monitor = document.getElementById('floorMonitor');
  if (!monitor) return;

  const floors = [
    { id: 'F1', name: 'Amanah', score: floorScores.F1 || 1.0 },
    { id: 'F2', name: 'Truth', score: floorScores.F2 || 0.99 },
    { id: 'F3', name: 'Witness', score: floorScores.F3 || 0.95 },
    { id: 'F6', name: 'Empathy', score: floorScores.F6 || 0.95 },
    { id: 'F7', name: 'Humility', score: floorScores.F7 || 0.05 },
    { id: 'F8', name: 'Genius', score: floorScores.F8 || 0.80 },
    { id: 'F9', name: 'Anti-Hantu', score: floorScores.F9 || 0.30 },
    { id: 'F11', name: 'Command', score: floorScores.F11 || 1.0 },
    { id: 'F12', name: 'Injection', score: floorScores.F12 || 1.0 },
  ];

  monitor.innerHTML = floors.map(f => `
    <div class="floor-item ${f.score >= 0.95 ? 'floor-pass' : f.score >= 0.80 ? 'floor-warn' : 'floor-fail'}">
      <span class="floor-id">${f.id}</span>
      <span class="floor-name">${f.name}</span>
      <div class="floor-bar">
        <div class="floor-fill" style="width: ${f.score * 100}%"></div>
      </div>
      <span class="floor-score">${(f.score * 100).toFixed(0)}%</span>
    </div>
  `).join('');
}

// ── Tab Switching ───────────────────────────────────────────────────────────
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
    
    // H1: Emit tab change event
    document.dispatchEvent(new CustomEvent('h1:tabchange', { detail: { tab: tabId } }));
  });
});

// ── Copy Buttons ────────────────────────────────────────────────────────────
document.querySelectorAll('.copy-btn').forEach(btn => {
  btn.addEventListener('click', async () => {
    const targetId = btn.getAttribute('data-copy');
    const pre = document.getElementById(targetId);
    if (!pre) return;

    const text = pre.innerText || pre.textContent;
    try {
      await navigator.clipboard.writeText(text);
      const orig = btn.textContent;
      btn.textContent = 'Copied!';
      btn.classList.add('copied');
      setTimeout(() => { btn.textContent = orig; btn.classList.remove('copied'); }, 2000);
    } catch (e) {
      const range = document.createRange();
      range.selectNodeContents(pre);
      window.getSelection().removeAllRanges();
      window.getSelection().addRange(range);
    }
  });
});

// ── Nav scroll active state ─────────────────────────────────────────────────
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

// ── Animate numbers in hero stats ───────────────────────────────────────────
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

// Animate hero stats on load
window.addEventListener('load', () => {
  document.querySelectorAll('.stat-val').forEach(el => {
    const target = parseInt(el.textContent);
    if (!isNaN(target)) animateValue(el, target, 1200);
  });
});

// ── H1 Entrance animation for cards ─────────────────────────────────────────
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

// ── H1 Simulated 3E Demo (for showcase) ─────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  // Simulate a 3E telemetry update for demo purposes
  const demo3E = {
    exploration: { sources_consulted: 5, depth_level: 3, breadth_score: 0.85 },
    entropy: { uncertainty_index: 0.12, contradiction_count: 1, resolution_confidence: 0.88 },
    eureka: { insight_delta: 0.72, novelty_score: 0.85, crystallisation_flag: true }
  };
  
  // If there's a demo container, populate it
  if (document.getElementById('demo3ETelemetry')) {
    render3ETelemetry('demo3ETelemetry', demo3E);
  }
  
  // Initialize W3 gauge with demo value
  updateW3Gauge(0.87);
  
  // Initialize metabolic stage
  updateMetabolicStage('777_EUREKA');
  
  // Initialize floor monitor
  updateFloorMonitor({
    F1: 1.0, F2: 0.99, F3: 0.96, F6: 0.98, F7: 0.04, 
    F8: 0.87, F9: 0.15, F11: 1.0, F12: 1.0
  });
});

// ── H1 Console Greeting ─────────────────────────────────────────────────────
console.log('%c🛡️ arifOS MCP', 'font-size: 24px; font-weight: bold; color: #00e5b0;');
console.log('%cH1 Higher Intelligence State — Developer Portal', 'font-size: 14px; color: #8896ab;');
console.log('%c3E Telemetry · W3 Tri-Witness · 13 Constitutional Floors', 'font-size: 12px; color: #5a6a7d;');
console.log('%cDITEMPA BUKAN DIBERI — Forged, Not Given', 'font-size: 11px; font-style: italic; color: #4a5a6d;');

// Export H1 state for debugging
window.H1State = H1State;
