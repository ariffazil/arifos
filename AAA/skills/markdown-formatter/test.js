/**
 * Markdown-Formatter Test Suite
 */

const { formatMarkdown, formatBatch, lintMarkdown } = require('./index.js');

console.log('=== Markdown-Formatter Test Suite ===\n');

// Test 1: Simple Formatting
console.log('Test 1: Simple Markdown Formatting');
console.log('Testing basic formatting with CommonMark style...\n');

const result = formatMarkdown({
  markdown: '# My Document\n\n\nThis is a test document.\n\nIt has multiple paragraphs.\n\nAnd some bullet points:\n\n- Point one\n- Point two\n- Point three',
  style: 'commonmark'
});

console.log(`✓ Formatted:\n${result.formattedMarkdown.substring(0, 100)}...`);
console.log(`✓ Warnings: ${result.warnings.length}`);
console.log(`\nOriginal: ${result.stats.originalLength} chars`);
console.log(`\nFormatted: ${result.stats.formattedLength} chars`);

console.log('');