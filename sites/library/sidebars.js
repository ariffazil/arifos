// @ts-check
// sidebars.js - arifOS Docs Navigation
// All operator-focused paths; theory links out to GitHub.

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  docsSidebar: [
    {
      type: 'doc',
      id: 'intro',
      label: ' Introduction',
    },
    {
      type: 'category',
      label: ' MCP Server',
      collapsed: false,
      items: [
        'mcp-server',
        'deployment',
        'api',
      ],
    },
    {
      type: 'category',
      label: ' Governance',
      collapsed: false,
      items: [
        'governance',
        'theory-000',
      ],
    },
    {
      type: 'category',
      label: ' 🔻 0_KERNEL (Mind)',
      collapsed: false,
      items: [
        '0_KERNEL/README',
        {
          type: 'category',
          label: 'ROOT (Foundations)',
          items: [
            '0_KERNEL/ROOT/000_CANON_MAP',
            '0_KERNEL/ROOT/K000_ROOT',
            '0_KERNEL/ROOT/K111_PHYSICS',
            '0_KERNEL/ROOT/K222_MATH',
            '0_KERNEL/ROOT/K333_CODE',
          ],
        },
        {
          type: 'category',
          label: 'FLOORS (Law)',
          items: [
            '0_KERNEL/FLOORS/K000_LAW',
            '0_KERNEL/FLOORS/F01_AMANAH',
            '0_KERNEL/FLOORS/F02_TRUTH',
            '0_KERNEL/FLOORS/F03_WITNESS',
            '0_KERNEL/FLOORS/F13_SOVEREIGN',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: ' 🤖 AGENTS (Protocols)',
      collapsed: false,
      items: [
        'AGENTS/A000_HUB',
        'AGENTS/A100_ARCHITECT',
        'AGENTS/A120_TOPOGRAPHY',
        'AGENTS/A200_ENGINEER',
      ],
    },
    {
      type: 'category',
      label: ' Architecture',
      collapsed: true,
      items: [
        'architecture',
        'advanced-roadmap',
      ],
    },
    {
      type: 'category',
      label: 'Bot Crawlers & LLMs',
      collapsed: true,
      items: [
        'crawlers',
      ],
    },
    {
      type: 'category',
      label: '🤖 Platform Integrations',
      collapsed: false,
      items: [
        'integration-claude',
        'integration-gemini',
        'integration-chatgpt',
      ],
    },
  ],
};

module.exports = sidebars;
