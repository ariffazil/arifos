/* ============================================================
   arifosMCP Developer Documentation — app.js
   v2026.03.13-FORGED
   ============================================================ */

(function () {
  'use strict';

  // ---- DOM READY ----
  document.addEventListener('DOMContentLoaded', init);

  function init() {
    initCopyButtons();
    initSidebarCollapse();
    initSidebarSearch();
    initScrollSpy();
    initTOC();
    initMobileMenu();
    initTabs();
    initNavHighlight();
  }

  // ---- COPY BUTTONS ----
  function initCopyButtons() {
    document.querySelectorAll('.copy-btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var block = btn.closest('.code-block');
        if (!block) return;
        var code = block.querySelector('code');
        if (!code) return;
        var text = code.textContent;
        navigator.clipboard.writeText(text).then(function () {
          btn.textContent = 'Copied!';
          btn.classList.add('copied');
          setTimeout(function () {
            btn.textContent = 'Copy';
            btn.classList.remove('copied');
          }, 2000);
        }).catch(function () {
          // Fallback
          var ta = document.createElement('textarea');
          ta.value = text;
          ta.style.position = 'fixed';
          ta.style.opacity = '0';
          document.body.appendChild(ta);
          ta.select();
          document.execCommand('copy');
          document.body.removeChild(ta);
          btn.textContent = 'Copied!';
          btn.classList.add('copied');
          setTimeout(function () {
            btn.textContent = 'Copy';
            btn.classList.remove('copied');
          }, 2000);
        });
      });
    });
  }

  // ---- SIDEBAR SECTION COLLAPSE ----
  function initSidebarCollapse() {
    document.querySelectorAll('.sidebar-section-title').forEach(function (title) {
      title.addEventListener('click', function () {
        var section = title.closest('.sidebar-section');
        if (section) {
          section.classList.toggle('collapsed');
        }
      });
    });
  }

  // ---- SIDEBAR SEARCH ----
  function initSidebarSearch() {
    var input = document.getElementById('sidebarSearch');
    if (!input) return;

    input.addEventListener('input', function () {
      var q = input.value.toLowerCase().trim();
      var sections = document.querySelectorAll('.sidebar-section');

      sections.forEach(function (section) {
        var items = section.querySelectorAll('.sidebar-item');
        var anyVisible = false;

        items.forEach(function (item) {
          var text = item.textContent.toLowerCase();
          var match = !q || text.includes(q);
          item.style.display = match ? '' : 'none';
          if (match) anyVisible = true;
        });

        // Show/hide section
        section.style.display = anyVisible || !q ? '' : 'none';
        // Expand matching sections
        if (q && anyVisible) {
          section.classList.remove('collapsed');
        }
      });
    });
  }

  // ---- SCROLL SPY ----
  function initScrollSpy() {
    var sections = document.querySelectorAll('.doc-content section[id]');
    var sidebarItems = document.querySelectorAll('.sidebar-item[data-target]');
    var tocLinks = null; // will be set after TOC builds

    var headerOffset = 120;
    var ticking = false;

    function onScroll() {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        ticking = false;
        var scrollY = window.scrollY + headerOffset;
        var active = null;

        sections.forEach(function (sec) {
          if (sec.offsetTop <= scrollY) {
            active = sec.id;
          }
        });

        // Update sidebar
        sidebarItems.forEach(function (item) {
          var target = item.getAttribute('data-target');
          if (target === active) {
            item.classList.add('active');
            // Ensure parent section is expanded
            var parentSection = item.closest('.sidebar-section');
            if (parentSection) parentSection.classList.remove('collapsed');
          } else {
            item.classList.remove('active');
          }
        });

        // Update TOC
        if (!tocLinks) tocLinks = document.querySelectorAll('.doc-toc a[href]');
        tocLinks.forEach(function (link) {
          var href = link.getAttribute('href');
          if (href === '#' + active) {
            link.classList.add('active');
          } else {
            link.classList.remove('active');
          }
        });
      });
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    // Initial call
    setTimeout(onScroll, 100);
  }

  // ---- RIGHT TOC ----
  function initTOC() {
    var toc = document.getElementById('docToc');
    if (!toc) return;

    // Find all h2 and h3 in main content that have IDs
    var headings = document.querySelectorAll('.doc-content h1[id], .doc-content h2[id], .doc-content h3[id]');
    var frag = document.createDocumentFragment();

    // Keep the title
    var titleDiv = toc.querySelector('.doc-toc-title');

    headings.forEach(function (h) {
      if (!h.id) return;
      var a = document.createElement('a');
      a.href = '#' + h.id;
      a.textContent = h.textContent.trim();
      if (h.tagName === 'H3') {
        a.classList.add('toc-h3');
      }
      frag.appendChild(a);
    });

    // Clear existing links (keep title)
    while (toc.childNodes.length > 1) {
      toc.removeChild(toc.lastChild);
    }
    toc.appendChild(frag);

    // Smooth scroll for TOC links
    toc.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        e.preventDefault();
        var target = document.querySelector(e.target.getAttribute('href'));
        if (target) {
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
          history.pushState(null, '', e.target.getAttribute('href'));
        }
      }
    });
  }

  // ---- MOBILE MENU ----
  function initMobileMenu() {
    var hamburger = document.getElementById('hamburgerBtn');
    var sidebar = document.getElementById('docSidebar');
    var overlay = document.getElementById('sidebarOverlay');

    if (!hamburger || !sidebar) return;

    function toggle() {
      sidebar.classList.toggle('open');
      if (overlay) overlay.classList.toggle('active');
    }

    function close() {
      sidebar.classList.remove('open');
      if (overlay) overlay.classList.remove('active');
    }

    hamburger.addEventListener('click', toggle);
    if (overlay) overlay.addEventListener('click', close);

    // Close on sidebar link click (mobile)
    sidebar.addEventListener('click', function (e) {
      if (e.target.classList.contains('sidebar-item')) {
        if (window.innerWidth <= 860) {
          close();
        }
      }
    });
  }

  // ---- TABS ----
  function initTabs() {
    var tabContainers = document.querySelectorAll('.tabs');
    tabContainers.forEach(function (tabs) {
      var btns = tabs.querySelectorAll('.tab-btn');
      btns.forEach(function (btn) {
        btn.addEventListener('click', function () {
          var tabId = btn.getAttribute('data-tab');
          // Deactivate all
          btns.forEach(function (b) { b.classList.remove('active'); });
          // Hide all panels in same parent
          var parent = tabs.parentElement;
          parent.querySelectorAll('.tab-panel').forEach(function (p) { p.classList.remove('active'); });
          // Activate
          btn.classList.add('active');
          var panel = document.getElementById(tabId);
          if (panel) panel.classList.add('active');
        });
      });
    });
  }

  // ---- NAV HIGHLIGHT ----
  function initNavHighlight() {
    var navLinks = document.querySelectorAll('.doc-nav-center a');
    navLinks.forEach(function (link) {
      link.addEventListener('click', function (e) {
        navLinks.forEach(function (l) { l.classList.remove('active'); });
        link.classList.add('active');
      });
    });

    // Also update nav on scroll
    var sections = {
      'overview': 'Docs',
      'quick-start': 'Docs',
      'installation': 'Docs',
      'trinity-architecture': 'Docs',
      'metabolic-pipeline': 'Docs',
      'mgi-envelope': 'Docs',
      'service-topology': 'Docs',
      'tool-reference': 'Tools',
      'tool-arifos-kernel': 'Tools',
      'tool-reality-compass': 'Tools',
      'tool-reality-atlas': 'Tools',
      'tool-reality-dossier': 'Tools',
      'tool-init-anchor': 'Tools',
      'tool-check-vital': 'Tools',
      'tool-audit-rules': 'Tools',
      'tool-session-memory': 'Tools',
      'tool-verify-vault': 'Tools',
      'tool-apex-dashboard': 'Tools',
      'tool-search-reality': 'Tools',
      'tool-ingest-evidence': 'Tools',
      'constitutional-floors': 'Docs',
      'three-e-telemetry': 'Docs',
      'fault-codes': 'Docs',
      'integrations': 'Integrations',
      'self-hosting': 'Self-Hosting',
      'env-vars': 'Self-Hosting',
      'apex-theory': 'Docs'
    };

    var ticking = false;
    window.addEventListener('scroll', function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        ticking = false;
        var scrollY = window.scrollY + 140;
        var active = null;
        document.querySelectorAll('.doc-content section[id]').forEach(function (sec) {
          if (sec.offsetTop <= scrollY) active = sec.id;
        });
        if (active && sections[active]) {
          navLinks.forEach(function (l) {
            var text = l.textContent.trim();
            l.classList.toggle('active', text === sections[active]);
          });
        }
      });
    }, { passive: true });
  }

  // ---- SIDEBAR SMOOTH SCROLL ----
  document.addEventListener('click', function (e) {
    var item = e.target.closest('.sidebar-item');
    if (item) {
      e.preventDefault();
      var href = item.getAttribute('href');
      if (href) {
        var target = document.querySelector(href);
        if (target) {
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
          history.pushState(null, '', href);
        }
      }
    }
  });

})();
