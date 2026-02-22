// @ts-check
// sidebars.js — arifOS Docs Navigation
// All operator-focused paths; theory links out to GitHub.

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  docsSidebar: [
    {
      type: 'doc',
      id: 'intro',
      label: '🏛️ Introduction',
    },
    {
      type: 'category',
      label: '⚙️ MCP Server',
      collapsed: false,
      items: [
        'mcp-server',
        'deployment',
        'api',
      ],
    },
    {
      type: 'category',
      label: '🛡️ Governance',
      collapsed: false,
      items: [
        'governance',
        'theory-000',
      ],
    },
    {
      type: 'category',
      label: '📜 000_THEORY Canon',
      collapsed: false,
      items: [
        'canon/canon-foundation',
        'canon/canon-law',
        'canon/canon-ignition',
        'canon/canon-witness',
        'canon/canon-trinity-organs',
      ],
    },
    {
      type: 'category',
      label: '🏗️ Architecture',
      collapsed: true,
      items: [
        'architecture',
      ],
    },
    {
      type: 'category',
      label: '🤖 Crawlers & LLMs',
      collapsed: true,
      items: [
        'llms-and-robots',
      ],
    },
  ],
};

module.exports = sidebars;
