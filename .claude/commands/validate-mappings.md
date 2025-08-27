# Validate Paragraph Mappings

Launch mapping validation to ensure accurate traceability and quality metrics.

**Usage**: `/validate-mappings <processed-book-path>`

## Purpose

Quality assurance for completed book processing to ensure:
- All paragraphs have accurate mappings
- Quality metrics reflect actual improvements
- Double-tap functionality will work correctly
- No information loss or voice drift

## Process

1. Launch mapping-validator subagent
2. Validate all original→enhanced paragraph relationships
3. Verify quality metrics and confidence scores
4. Check for errors, inconsistencies, and missing mappings
5. Generate detailed validation report with corrections

## Arguments

- `<processed-book-path>`: Path to ProcessedBook JSON file

## Example Usage

```bash
# Validate completed book processing
/validate-mappings "processed-books/book-processed.json"
```

Launch mapping-validator subagent to validate: $ARGUMENTS

The agent will perform comprehensive quality assurance:
- Verify mapping accuracy and completeness
- Validate quality metrics and confidence scores  
- Check for information loss or voice drift
- Ensure user experience requirements are met
- Generate actionable correction recommendations

This ensures the processed book meets production quality standards.