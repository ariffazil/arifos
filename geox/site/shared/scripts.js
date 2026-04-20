/**
 * GEOX Command Center - Shared JavaScript Utilities
 * ================================================
 */

// ============================================
// Initialize Lucide Icons
// ============================================
document.addEventListener('DOMContentLoaded', function() {
  // Initialize Lucide icons
  if (typeof lucide !== 'undefined') {
    lucide.createIcons();
  }

  // Initialize navigation
  initNavigation();

  // Initialize scroll animations
  initScrollAnimations();

  // Initialize dropdowns
  initDropdowns();
});

// ============================================
// Navigation Utilities
// ============================================

/**
 * Initialize navigation functionality
 * - Highlights current page in nav
 * - Sets up mobile menu toggle
 */
function initNavigation() {
  // Get current page from URL
  const currentPath = window.location.pathname;
  const currentPage = currentPath.split('/').pop() || 'index.html';

  // Highlight active nav link
  highlightActiveNav(currentPage);

  // Close mobile menu on window resize (if going to desktop)
  window.addEventListener('resize', throttle(function() {
    if (window.innerWidth >= 768) {
      closeMobileMenu();
    }
  }, 250));
}

/**
 * Highlight the active navigation link based on current page
 * @param {string} currentPage - Current page filename
 */
function highlightActiveNav(currentPage) {
  // Map page filenames to nav data attributes
  const pageToNav = {
    'index.html': 'index',
    '': 'index',
    'ac-risk.html': 'ac-risk',
    'ratlas.html': 'ratlas',
    'basin-explorer.html': 'basin',
    'seismic-viewer.html': 'seismic',
    'well-context-desk.html': 'well'
  };

  const navKey = pageToNav[currentPage];
  if (!navKey) return;

  // Find and highlight matching nav links
  const navLinks = document.querySelectorAll('[data-nav]');
  navLinks.forEach(link => {
    if (link.dataset.nav === navKey) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });
}

// ============================================
// Mobile Menu Toggle
// ============================================

/**
 * Toggle mobile menu open/closed
 */
function toggleMobileMenu() {
  const mobileMenu = document.getElementById('mobile-menu');
  const menuToggle = document.getElementById('mobile-menu-toggle');
  const iconOpen = document.getElementById('menu-icon-open');
  const iconClose = document.getElementById('menu-icon-close');

  if (!mobileMenu) return;

  const isOpen = mobileMenu.classList.contains('active');

  if (isOpen) {
    closeMobileMenu();
  } else {
    openMobileMenu();
  }
}

/**
 * Open mobile menu
 */
function openMobileMenu() {
  const mobileMenu = document.getElementById('mobile-menu');
  const menuToggle = document.getElementById('mobile-menu-toggle');
  const iconOpen = document.getElementById('menu-icon-open');
  const iconClose = document.getElementById('menu-icon-close');

  if (mobileMenu) {
    mobileMenu.classList.add('active');
    document.body.style.overflow = 'hidden'; // Prevent body scroll
  }

  if (menuToggle) {
    menuToggle.setAttribute('aria-expanded', 'true');
  }

  if (iconOpen && iconClose) {
    iconOpen.classList.add('hidden');
    iconClose.classList.remove('hidden');
  }
}

/**
 * Close mobile menu
 */
function closeMobileMenu() {
  const mobileMenu = document.getElementById('mobile-menu');
  const menuToggle = document.getElementById('mobile-menu-toggle');
  const iconOpen = document.getElementById('menu-icon-open');
  const iconClose = document.getElementById('menu-icon-close');

  if (mobileMenu) {
    mobileMenu.classList.remove('active');
    document.body.style.overflow = ''; // Restore body scroll
  }

  if (menuToggle) {
    menuToggle.setAttribute('aria-expanded', 'false');
  }

  if (iconOpen && iconClose) {
    iconOpen.classList.remove('hidden');
    iconClose.classList.add('hidden');
  }
}

// ============================================
// Dropdown Utilities
// ============================================

/**
 * Initialize dropdown functionality
 */
function initDropdowns() {
  // Close dropdowns when clicking outside
  document.addEventListener('click', function(event) {
    const dropdowns = document.querySelectorAll('.dropdown-menu.active');
    dropdowns.forEach(dropdown => {
      const parent = dropdown.closest('.dropdown');
      if (parent && !parent.contains(event.target)) {
        dropdown.classList.remove('active');
        const chevron = parent.querySelector('#tools-chevron');
        if (chevron) {
          chevron.style.transform = 'rotate(0deg)';
        }
      }
    });
  });
}

/**
 * Toggle dropdown menu
 * @param {Event} event - Click event
 */
function toggleDropdown(event) {
  event.preventDefault();
  event.stopPropagation();

  const dropdown = event.currentTarget.closest('.dropdown');
  if (!dropdown) return;

  const menu = dropdown.querySelector('.dropdown-menu');
  const chevron = dropdown.querySelector('#tools-chevron');

  if (menu) {
    const isOpen = menu.classList.contains('active');

    // Close all other dropdowns first
    document.querySelectorAll('.dropdown-menu.active').forEach(d => {
      d.classList.remove('active');
    });
    document.querySelectorAll('#tools-chevron').forEach(c => {
      c.style.transform = 'rotate(0deg)';
    });

    // Toggle current dropdown
    if (!isOpen) {
      menu.classList.add('active');
      if (chevron) {
        chevron.style.transform = 'rotate(180deg)';
      }
    }
  }
}

// ============================================
// Scroll Animations (Intersection Observer)
// ============================================

/**
 * Initialize scroll animations using IntersectionObserver
 */
function initScrollAnimations() {
  const animatedElements = document.querySelectorAll('.scroll-animate');

  if (animatedElements.length === 0) return;

  // Check if IntersectionObserver is supported
  if (!('IntersectionObserver' in window)) {
    // Fallback: show all elements
    animatedElements.forEach(el => {
      el.classList.add('animated');
    });
    return;
  }

  const observerOptions = {
    root: null,
    rootMargin: '0px 0px -50px 0px',
    threshold: 0.1
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animated');
        // Optionally unobserve after animation
        // observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  animatedElements.forEach(el => {
    observer.observe(el);
  });
}

/**
 * Manually trigger scroll animation check
 * Useful for dynamically added content
 */
function refreshScrollAnimations() {
  initScrollAnimations();
  // Re-initialize Lucide icons for new content
  if (typeof lucide !== 'undefined') {
    lucide.createIcons();
  }
}

// ============================================
// Utility Functions
// ============================================

/**
 * Throttle function execution
 * @param {Function} func - Function to throttle
 * @param {number} limit - Time limit in milliseconds
 * @returns {Function} Throttled function
 */
function throttle(func, limit) {
  let inThrottle;
  return function(...args) {
    if (!inThrottle) {
      func.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

/**
 * Debounce function execution
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {Function} Debounced function
 */
function debounce(func, wait) {
  let timeout;
  return function(...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, args), wait);
  };
}

/**
 * Smooth scroll to element
 * @param {string} selector - CSS selector for target element
 * @param {number} offset - Optional offset from top (default: 80px for header)
 */
function scrollToElement(selector, offset = 80) {
  const element = document.querySelector(selector);
  if (element) {
    const elementPosition = element.getBoundingClientRect().top;
    const offsetPosition = elementPosition + window.pageYOffset - offset;

    window.scrollTo({
      top: offsetPosition,
      behavior: 'smooth'
    });
  }
}

/**
 * Copy text to clipboard
 * @param {string} text - Text to copy
 * @returns {Promise<boolean>} Success status
 */
async function copyToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (err) {
    console.error('Failed to copy:', err);
    return false;
  }
}

/**
 * Format number with commas
 * @param {number} num - Number to format
 * @returns {string} Formatted number
 */
function formatNumber(num) {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

/**
 * Format bytes to human readable string
 * @param {number} bytes - Bytes to format
 * @param {number} decimals - Decimal places (default: 2)
 * @returns {string} Formatted string
 */
function formatBytes(bytes, decimals = 2) {
  if (bytes === 0) return '0 Bytes';

  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];

  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

// ============================================
// Theme Utilities (for future dark/light toggle)
// ============================================

/**
 * Get current theme
 * @returns {string} Current theme ('dark' or 'light')
 */
function getTheme() {
  return document.documentElement.getAttribute('data-theme') || 'dark';
}

/**
 * Set theme
 * @param {string} theme - Theme to set ('dark' or 'light')
 */
function setTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('geox-theme', theme);
}

/**
 * Toggle between dark and light themes
 */
function toggleTheme() {
  const currentTheme = getTheme();
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  setTheme(newTheme);
}

/**
 * Initialize theme from localStorage
 */
function initTheme() {
  const savedTheme = localStorage.getItem('geox-theme') || 'dark';
  setTheme(savedTheme);
}

// ============================================
// Export for module usage (if needed)
// ============================================
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    throttle,
    debounce,
    scrollToElement,
    copyToClipboard,
    formatNumber,
    formatBytes,
    getTheme,
    setTheme,
    toggleTheme,
    initTheme,
    refreshScrollAnimations
  };
}
