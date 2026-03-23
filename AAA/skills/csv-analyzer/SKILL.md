---
description: Analyze CSV/TSV files with statistics, data profiling, and ASCII visualizations.
---

# CSV Analyzer

Analyze CSV/TSV files: statistics, data profiling, and visualizations.

## Instructions

1. **Read and detect**: Identify delimiter (comma, tab, pipe), encoding, row count
2. **Preview**: Show first 5 rows as a formatted table
3. **Profile each column**:

   **Numeric columns**: count, mean, median, min, max, std dev, null count
   **String columns**: count, unique values, top 5 most frequent, avg length
   **Date columns**: min date, max date, range

4. **Summary report**:
   ```
   📊 CSV Analysis — data.csv
   Rows: 10,432 | Columns: 8 | Size: 2.1 MB

   | Column    | Type    | Non-null | Unique | Summary            |
   |-----------|---------|----------|--------|--------------------|
   | name      | string  | 10,432   | 8,721  | top: "John" (42)   |
   | age       | numeric | 10,210   | 82     | mean=34.2, σ=12.1  |
   | signup    | date    | 10,432   | 1,203  | 2020-01 to 2025-01 |
   ```

5. **Visualizations** (ASCII):
   ```bash
   # Histogram
   awk -F',' 'NR>1{print int($3/10)*10}' data.csv | sort -n | uniq -c | awk '{printf "%3d-%3d: %s (%d)\n", $2, $2+9, substr("████████████████████",1,$1/5), $1}'

   # Top values bar chart
   awk -F',' 'NR>1{print $2}' data.csv | sort | uniq -c | sort -rn | head -10
   ```

## Edge Cases

- **Large files (>100MB)**: Sample first 10,000 rows; report that sampling was used
- **Quoted fields**: Handle `"field, with comma"` correctly — use proper CSV parsing
- **Mixed types**: If a column has mixed numeric/string, classify as string
- **Empty file**: Report immediately; don't error out
- **Encoding issues**: Try UTF-8 first, fall back to Latin-1; report if issues detected

## Requirements

- Standard Unix tools: `awk`, `sort`, `uniq`, `wc`, `head`
- No API keys or external dependencies
