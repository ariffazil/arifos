#!/bin/bash

# Script to commit and push the enhanced APPS site changes

cd /tmp/arif-fazil-sites

# Check if there are changes to commit
echo "Checking for changes..."
git status

# Add the modified files
echo "Adding updated files..."
git add APPS/index.html APPS/src/App.tsx APPS/README.md

# Commit the changes
echo "Committing changes..."
git commit -m "feat: transform APPS site to product-focused implementation hub

- Update index.html with product-focused meta tags and descriptions
- Enhance App.tsx with product showcase, business value sections, and implementation metrics
- Add 7-layer product stack with business value, implementation time, and ROI metrics
- Include product showcase section with measurable outcomes
- Add implementation guide with clear business value propositions
- Update MCP tools section with use cases and business value
- Enhance navigation with product-focused terminology
- Add structured data for product discoverability
- Update README with product overview and implementation guide

The APPS site now focuses purely on arifOS products, implementations, and actionable items rather than just documentation."

# Show the commit
echo "Latest commit:"
git log -1 --oneline

echo "Changes prepared for push to repository."
echo "To push to main branch, run: git push origin main"