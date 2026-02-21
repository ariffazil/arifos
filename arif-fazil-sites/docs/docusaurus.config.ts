import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'arifOS Docs',
  tagline: 'Constitutional AI Governance System',
  favicon: 'img/favicon.ico',

  url: 'https://arifos.arif-fazil.com',
  baseUrl: '/docs/',

  organizationName: 'ariffazil',
  projectName: 'arifOS',

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/ariffazil/arifOS/tree/main/arif-fazil-sites/DOCS/',
          routeBasePath: '/', // Serve docs at the root of this sub-site
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    navbar: {
      title: 'arifOS',
      logo: {
        alt: 'arifOS Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Documentation',
        },
        {
          href: 'https://arifosmcp.arif-fazil.com/health',
          label: 'System Health',
          position: 'right',
        },
        {
          href: 'https://github.com/ariffazil/arifOS',
          label: 'GitHub',
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
            {
              label: 'Introduction',
              to: '/',
            },
            {
              label: 'MCP Integration',
              to: '/governance/mcp-integration',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'Main Site',
              href: 'https://arifos.arif-fazil.com',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Muhammad Arif bin Fazil. arifOS: Forged, Not Given.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
