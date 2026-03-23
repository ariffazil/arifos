/**
 * Markdown-Formatter - Format and beautify markdown documents
 * Vernox v1.0 - Autonomous Revenue Agent
 */

const fs = require('fs');
const path = require('path');

// Pattern matches
const PATTERNS = {
  trailingWhitespace: /[ \t]+$/gm,
  multipleBlankLines: /\n{3,}/g,
  inconsistentListDash: /^\s{0,2}([*-])\s/g,
  inconsistentListAsterisk: /^\s{0,2}([*])\s/g,
  inconsistentListPlus: /^\s{0,2}([+])\s/g,
  inconsistentListTask: /^\s{0,2}(- \[ )\]\s/g,
  atxHeading: /^#{1,2}\s[^#]+/,
  setextHeading: /^#{1,2}\s[=-]+/,
  codeBlockFenced: /^```/g,
  codeBlockIndented: /^ {4}/,
  strikethrough: /~~(.+?)~~/g,
  autoLink: /<https?:\/\/[^>\s]+>/gi
};

// Constants for style guides
const STYLE_GUIDES = {
  commonmark: {
    headingLevels: ['#', '##', '###'],
    emphasis: {
      underscore: '__text__',
      asterisk: '**text**'
    },
    links: {
      inline: '[text](url)',
      reference: '[text][id]'
    }
  },
  github: {
    headingLevels: ['#', '##', '###'],
    emphasis: {
      underscore: '__text__',
      asterisk: '**text**'
    },
    links: {
      inline: '[text](url)',
      reference: '[text][id]'
    },
    codeBlocks: {
      fenced: '```',
      indented: '    '
    },
    lists: {
      unordered: '-',
      ordered: '1.',
      task: '- [ ]'
    },
    strikethrough: '~~text~~',
    autoLinks: '<https://url>'
    },
    tables: '| column | column | '
  },
  consistent: {
    headingLevels: ['#', '##', '###'],
    emphasis: {
      underscore: false,
      asterisk: true
    },
    links: {
      inline: '[text](url)'
    },
    lists: {
      unordered: '-',
      ordered: '1.'
    },
    codeBlocks: {
      fenced: '```'
    },
    tables: '| column | column | '
  }
};

/**
 * Format markdown content according to style guide
 */
function formatMarkdown(params) {
  const { markdown, style, options = {} } = params;

  if (!markdown) {
    throw new Error('markdown is required');
  }

  const styleGuide = STYLE_GUIDES[style] || STYLE_GUIDES.github;
  const opts = { ...STYLE_GUIDES.github, ...options };

  let formatted = markdown;
  const warnings = [];
  const startTime = Date.now();

  // 1. Normalize line endings
  formatted = formatted.replace(/\r\n/g, '\n');

  // 2. Remove trailing whitespace from each line
  const lines = formatted.split('\n');
  formatted = lines.map(line => line.trimRight()).join('\n');

  // 3. Fix inconsistent list markers
  if (opts.fixLists) {
    const fixedLists = fixListMarkers(lines, styleGuide);
    formatted = fixedLists.markdown;
    if (fixedLists.warnings.length > 0) {
      warnings.push(...fixedLists.warnings);
    }
  }

  // 4. Normalize heading styles
  if (styleGuide.headingLevels) {
    const fixedHeadings = normalizeHeadings(lines, styleGuide, opts.headingStyle);
    formatted = fixedHeadings.markdown;
    if (fixedHeadings.warnings.length > 0) {
      warnings.push(...fixedHeadings.warnings);
    }
  }

  // 5. Normalize emphasis
  if (styleGuide.emphasis) {
    const fixedEmphasis = normalizeEmphasis(formatted, styleGuide.emphasis);
    formatted = fixedEmphasis.markdown;
    if (fixedEmphasis.warnings.length > 0) {
      warnings.push(...fixedEmphasis.warnings);
    }
  }

  // 6. Fix code blocks
  if (styleGuide.codeBlocks) {
    const fixedCode = fixCodeBlocks(formatted, styleGuide.codeBlocks);
    formatted = fixedCode.markdown;
    if (fixedCode.warnings.length > 0) {
      warnings.push(...fixedCode.warnings);
    }
  }

  // 7. Fix tables
  if (styleGuide.tables) {
    const fixedTables = fixTables(formatted);
    formatted = fixedTables.markdown;
    if (fixedTables.warnings.length > 0) {
      warnings.push(...fixedTables.warnings);
    }
  }

  // 8. Remove multiple consecutive blank lines
  if (opts.normalizeSpacing) {
    formatted = formatted.replace(PATTERNS.multipleBlankLines, '\n\n\n');
  }

  // 9. Wrap long lines
  if (opts.maxWidth) {
    const wrappedLines = lines.map(line => wrapLine(line, opts.maxWidth));
    formatted = wrappedLines.join('\n');
  }

  // 10. Add spacing around emphasis
  if (styleGuide.emphasis && styleGuide.emphasis !== 'none') {
    formatted = addEmphasisSpacing(formatted, styleGuide.emphasis);
  }

  const endTime = Date.now();
  const stats = {
    originalLength: markdown.length,
    formattedLength: formatted.length,
    warnings: warnings.length
  };

  return {
    formattedMarkdown: formatted,
    warnings,
    stats,
    lintResult: {
      errors: [],
      warnings: warnings,
      fixed: markdown
    },
    processingTime: endTime - startTime
  };
}

/**
 * Fix inconsistent list markers
 */
function fixListMarkers(lines, styleGuide) {
  const warnings = [];
  let markdown = lines.join('\n');

  // Find and standardize unordered lists
  if (styleGuide.lists) {
    const unorderedPattern = /^\s{0,2}([*-])\s/g;
    const matches = markdown.match(unorderedPattern);

    if (matches) {
      const replacement = opts.lists === 'asterisk' ? '- ' : opts.lists === 'plus' ? '+ ' : '-';
      markdown = markdown.replace(unorderedPattern, `$1$2$3`);
    } else if (styleGuide.lists === 'dash') {
      markdown = markdown.replace(/^\s{0,2}([*-])\s/g, '$1$2$3');
    }
  }

  return { markdown, warnings };
}

/**
 * Normalize heading styles
 */
function normalizeHeadings(lines, styleGuide, headingStyle) {
  const warnings = [];
  let markdown = lines.join('\n');

  if (headingStyle === 'atx') {
    // Ensure ATX headings (### instead of #)
    const atxCount = (markdown.match(/#+\s+/g) || []).length;
    if (atxCount > 0) {
      warnings.push(`${atxCount} ATX-style headings found (should use ###)`);
      markdown = markdown.replace(/#+\s+/g, '### ');
    }
  } else if (headingStyle === 'setext') {
    // Ensure Setext headings (==== instead of #)
    const setextCount = (markdown.match(/^={4,}\s/g) || []).length;
    if (setextCount > 0) {
      warnings.push(`${setextCount} Setext headings found (should use #)`);
      markdown = markdown.replace(/^={4,}\s/g, '#');
    }
  } else if (headingStyle === 'underlined') {
    // Ensure underlined headings (=== or ---)
    const underlinePattern = /^(={3,}|-{3,})\n/gm;
    const underlineCount = (markdown.match(underlinePattern) || []).length;
    if (underlineCount > 0) {
      warnings.push(`${underlineCount} underline headings found (should use #)`);
      markdown = markdown.replace(underlinePattern, '#$1');
    }
  }

  return { markdown, warnings };
}

/**
 * Normalize emphasis
 */
function normalizeEmphasis(markdown, emphasis) {
  const warnings = [];

  if (emphasis === 'asterisk') {
    markdown = markdown.replace(/\*\*(?!.*?\*)/g, '*');
    markdown = markdown.replace(/_{2,}/g, '_');
    markdown = markdown.replace(/__{2,}/g, '__');
  } else if (emphasis === 'underscore') {
    markdown = markdown.replace(/__(.+?)__/g, '*$1*');
  }

  return { markdown, warnings };
}

/**
 * Fix code blocks
 */
function fixCodeBlocks(markdown, codeBlockStyle) {
  const warnings = [];

  if (codeBlockStyle === 'fenced') {
    const lines = markdown.split('\n');
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      if (/^```\s*$/.test(line) && !line.endsWith('```')) {
        warnings.push(`Unclosed fenced code block at line ${i + 1}`);
        lines[i] = line + '```';
      }
    }
    markdown = lines.join('\n');
  } else if (codeBlockStyle === 'indented') {
    markdown = markdown.replace(/^ {4}/gm, '    ');
  }

  return { markdown, warnings };
}

/**
 * Fix tables
 */
function fixTables(markdown) {
  const warnings = [];
  const headerPattern = /\|[^|\n]+?\|/g;
  markdown = markdown.replace(headerPattern, '| ');

  return { markdown, warnings };
}

/**
 * Wrap line at maxWidth
 */
function wrapLine(line, maxWidth) {
  if (line.length <= maxWidth) return line;
  return line.substring(0, maxWidth) + '\n' + line.substring(maxWidth);
}

/**
 * Add spacing around emphasis
 */
function addEmphasisSpacing(markdown, emphasis) {
  if (emphasis === 'asterisk') {
    return markdown.replace(/([^\s\*])(\*)([^\s])/g, '$1 $2$3');
  }
  return markdown;
}

/**
 * Lint markdown for issues
 */
function lintMarkdown(params) {
  const { markdown, style, options = {} } = params;
  const styleGuide = STYLE_GUIDES[style] || STYLE_GUIDES.github;
  const opts = { ...STYLE_GUIDES.github, ...options };

  const warnings = [];
  const errors = [];

  // Check heading levels
  if (opts.checkHeadingLevels) {
    const lines = markdown.split('\n');
    const headings = lines.filter(line => /^#+\s/.test(line));

    let prevLevel = 0;
    headings.forEach((heading, index) => {
      const match = heading.match(/^(#{1,2})\s+(.*)/);
      const level = match[1].length;

      if (index > 0 && level > prevLevel + 1) {
        errors.push({
          type: 'heading_skip',
          message: `Heading skipped ${level - prevLevel - 1} levels at line ${index + 1}`,
          line: heading
        });
      }

      prevLevel = level;
    });
  }

  const stats = {
    headingLevels: (markdown.match(/#+/g) || []).length,
    listMarkers: (markdown.match(/[-*+]/g) || []).length,
    emphasisMarkers: (markdown.match(/[*_]/g) || []).length,
    codeBlocks: (markdown.match(/```/g) || []).length / 2,
    tables: (markdown.match(/\|[^|\n]+?\|/g) || []).length / 3
  };

  return { errors, warnings, stats, suggestions: [] };
}

/**
 * Format multiple markdown files
 */
function formatBatch(params) {
  const { markdownFiles, style, options = {} } = params;

  if (!markdownFiles || !Array.isArray(markdownFiles)) {
    throw new Error('markdownFiles must be an array of file paths');
  }

  const startTime = Date.now();
  const results = [];
  const totalWarnings = [];

  for (const filePath of markdownFiles) {
    try {
      const content = fs.readFileSync(filePath, 'utf8');
      const result = formatMarkdown({
        markdown: content,
        style,
        options
      });

      results.push({
        file: filePath,
        formattedMarkdown: result.formattedMarkdown,
        warnings: result.warnings,
        stats: result.stats
      });

      totalWarnings.push(...result.warnings);
    } catch (error) {
      results.push({
        file: filePath,
        error: error.message || error
      });
    }
  }

  const endTime = Date.now();

  return {
    results,
    totalFiles: markdownFiles.length,
    totalWarnings: totalWarnings.length,
    processingTime: endTime - startTime
  };
}

/**
 * Main function - handles tool invocations
 */
function main(action, params) {
  switch (action) {
    case 'formatMarkdown':
      return formatMarkdown(params);
    case 'formatBatch':
      return formatBatch(params);
    case 'lintMarkdown':
      return lintMarkdown(params);
    default:
      throw new Error(`Unknown action: ${action}`);
  }
}

// CLI interface
if (require.main === module) {
  const args = process.argv.slice(2);
  const action = args[0];

  try {
    const params = JSON.parse(args[1] || '{}');
    const result = main(action, params);
    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    console.error(JSON.stringify({
      error: error.message || error
    }, null, 2));
    process.exit(1);
  }
}

module.exports = { main, formatMarkdown, formatBatch, lintMarkdown };
