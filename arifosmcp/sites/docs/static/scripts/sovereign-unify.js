(function() {
  const SCRIPT_BASE = 'https://arifos.arif-fazil.com/scripts/';
  
  // 1. Inject CSS
  const link = document.createElement('link');
  link.rel = 'stylesheet';
  link.href = SCRIPT_BASE + 'sovereign-unify.css';
  document.head.appendChild(link);

  // 2. Identify Current Domain
  const hostname = window.location.hostname;
  let activeClass = '';
  if (hostname.includes('arif-fazil.com') && !hostname.includes('arifos') && !hostname.includes('apex')) activeClass = 'active-human';
  else if (hostname.includes('apex')) activeClass = 'active-theory';
  else if (hostname.includes('arifos')) activeClass = 'active-apps';
  else if (hostname.includes('arifosmcp')) activeClass = 'active-runtime';

  // 3. Create Header
  const header = document.createElement('header');
  header.id = 'sovereign-header';
  header.innerHTML = `
    <a href="https://arifos.arif-fazil.com" class="logo">ΔΩΨ arifOS</a>
    <div class="trinity-pill">
      <a href="https://arif-fazil.com" class="${activeClass === 'active-human' ? 'active-human' : ''}">Human</a>
      <a href="https://apex.arif-fazil.com" class="${activeClass === 'active-theory' ? 'active-theory' : ''}">Theory</a>
      <a href="https://arifos.arif-fazil.com" class="${activeClass === 'active-apps' ? 'active-apps' : ''}">Apps</a>
      <a href="https://arifosmcp.arif-fazil.com" class="${activeClass === 'active-runtime' ? 'active-runtime' : ''}">Runtime</a>
    </div>
    <div class="status-pulse">
      <div class="pulse-dot"></div>
      SYSTEM SEALED
    </div>
  `;
  document.body.prepend(header);

  // 3.5 Create Hero Banner (Only on Root/Theory if missing)
  if (!document.querySelector('.sovereign-hero') && (hostname.includes('apex') || Array.from(document.querySelectorAll('h1')).length === 0)) {
    const hero = document.createElement('section');
    hero.className = 'sovereign-hero';
    hero.style.cssText = `
      padding: 100px 24px;
      text-align: center;
      background: var(--sovereign-bg);
      border-bottom: 1px solid rgba(255,255,255,0.05);
      position: relative;
      overflow: hidden;
    `;
    hero.innerHTML = `
      <div style="position: absolute; inset: 0; background: radial-gradient(circle at center, rgba(0,122,255,0.05) 0%, transparent 70%); pointer-events: none;"></div>
      <h1 style="font-size: clamp(32px, 8vw, 64px); font-weight: 900; margin-bottom: 16px; background: linear-gradient(to bottom, #fff, #888); -webkit-background-clip: text; -webkit-text-fill-color: transparent; position: relative;">INTELLIGENCE IS ENTROPY REDUCTION</h1>
      <p style="color: #8E8E93; font-size: 18px; max-width: 600px; margin: 0 auto; font-style: italic; position: relative;">"Truth must cool before it rules. Ditempa bukan diberi."</p>
    `;
    header.after(hero);
  }

  // 4. Create Footer
  const footer = document.createElement('footer');
  footer.id = 'sovereign-footer';
  footer.innerHTML = `
    <div class="canon-box">
      <div class="canon-text">
        "Intelligence is not merely computation; it is entropy reduction under governance. 
        Truth must cool before it rules. Ditempa bukan diberi."
      </div>
      <div class="motto">ARIF OS — FORGED, NOT GIVEN</div>
    </div>
  `;
  document.body.appendChild(footer);

  // Adjust body padding to accommodate fixed header
  document.body.style.paddingTop = '60px';

  // 4.5 Suppress Docusaurus Announcement Bar (if present)
  const suppressOverlaps = () => {
    const docusaurusAnnouncement = document.querySelector('div[class*="announcementBar"]');
    if (docusaurusAnnouncement) docusaurusAnnouncement.style.display = 'none';
    
    // Also hide default Docusaurus navbar to avoid double headers
    const docusaurusNavbar = document.querySelector('.navbar');
    // if (docusaurusNavbar) docusaurusNavbar.style.top = '60px';
  };
  suppressOverlaps();
  setTimeout(suppressOverlaps, 1000); // Repeat after hydration

  // 5. Dynamic Status Fetching
  async function updateStatus() {
    const pulseContainer = header.querySelector('.status-pulse');
    const statusText = pulseContainer.lastChild;
    
    try {
      const response = await fetch('https://arifosmcp.arif-fazil.com/health');
      if (response.ok) {
        pulseContainer.className = 'status-pulse';
        statusText.textContent = ' SYSTEM SEALED';
      } else {
        pulseContainer.className = 'status-pulse warning';
        statusText.textContent = ' 888_HOLD ACTIVE';
      }
    } catch (e) {
      pulseContainer.className = 'status-pulse error';
      statusText.textContent = ' SYSTEM OFFLINE';
    }
  }

  updateStatus();
  setInterval(updateStatus, 30000); // Check every 30s
})();
