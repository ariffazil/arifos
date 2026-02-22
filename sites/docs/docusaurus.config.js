// @ts-check
// docusaurus.config.js — arifOS Docs Site
// Target: https://arifos.arif-fazil.com/
// Source: https://github.com/ariffazil/arifOS

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'arifOS',
  tagline: 'The System That Knows It Doesn\'t Know',
  favicon: 'img/favicon.ico',

  url: 'https://arifos.arif-fazil.com',
  baseUrl: '/',

  organizationName: 'ariffazil',
  projectName: 'arifOS',
  trailingSlash: false,

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          // Serve docs at the site root
          routeBasePath: '/',
          sidebarPath: './sidebars.js',
          editUrl: 'https://github.com/ariffazil/arifOS/edit/main/sites/docs/',
          showLastUpdateTime: true,
          showLastUpdateAuthor: false,
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
        sitemap: {
          changefreq: 'weekly',
          priority: 0.5,
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Dark-first colour palette (matches arifOS identity)
      colorMode: {
        defaultMode: 'dark',
        disableSwitch: false,
        respectPrefersColorScheme: true,
      },

      image: 'img/arifos-og.png',

      navbar: {
        title: 'arifOS',
        logo: {
          alt: 'arifOS Logo',
          src: 'img/logo.svg',
          href: '/intro',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'docsSidebar',
            position: 'left',
            label: 'Docs',
          },
          {
            href: 'https://github.com/ariffazil/arifOS',
            label: 'GitHub',
            position: 'right',
          },
          {
            href: 'https://pypi.org/project/arifos/',
            label: 'PyPI',
            position: 'right',
          },
          {
            href: 'https://arifosmcp.arif-fazil.com',
            label: 'Status',
            position: 'right',
          },
        ],
      },

      footer: {
        style: 'dark',
        links: [
          {
            title: 'Docs',
            items: [
              { label: 'Introduction', to: '/intro' },
              { label: 'MCP Server', to: '/mcp-server' },
              { label: 'Governance', to: '/governance' },
              { label: 'API Reference', to: '/api' },
            ],
          },
          {
            title: 'Source',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/ariffazil/arifOS',
              },
              {
                label: 'PyPI',
                href: 'https://pypi.org/project/arifos/',
              },
              {
                label: 'CHANGELOG',
                href: 'https://github.com/ariffazil/arifOS/blob/main/CHANGELOG.md',
              },
            ],
          },
          {
            title: 'Governance',
            items: [
              {
                label: 'Live Health',
                href: 'https://arifosmcp.arif-fazil.com',
              },
              {
                label: '000_THEORY',
                href: 'https://github.com/ariffazil/arifOS/tree/main/000_THEORY',
              },
              {
                label: 'License (AGPL-3.0)',
                href: 'https://github.com/ariffazil/arifOS/blob/main/LICENSE',
              },
            ],
          },
        ],
        copyright: `arifOS — <em>Ditempa Bukan Diberi</em> (Forged, Not Given)<br/>Built ${new Date().getFullYear()} · Muhammad Arif bin Fazil · AGPL-3.0`,
      },

      prism: {
        theme: require('prism-react-renderer').themes.dracula,
        darkTheme: require('prism-react-renderer').themes.dracula,
        additionalLanguages: ['bash', 'python', 'json', 'nginx', 'docker'],
      },

      // Announcement bar for live status
      announcementBar: {
        id: 'live_status',
        content:
          '🟢 arifOS MCP is <a href="https://arifosmcp.arif-fazil.com">LIVE</a> — <a href="/mcp-server">Connect in 30 seconds</a>',
        backgroundColor: '#1a1a2e',
        textColor: '#00ff88',
        isCloseable: true,
      },
    }),
};

module.exports = config;
