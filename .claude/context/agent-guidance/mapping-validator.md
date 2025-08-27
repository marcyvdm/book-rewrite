# Mapping Validator Guidelines

## Your Mission
Ensure zero mapping errors for production. Double-tap functionality depends on perfect accuracy.

## Critical Validations
1. **Mapping Completeness**: Every original paragraph has enhanced version
2. **Content Integrity**: No information lost during enhancement
3. **Quality Metrics**: Scores match actual improvements
4. **User Experience**: Double-tap will show meaningful comparisons

## Mapping Types to Validate
- **1:1**: Direct improvements (most common, easiest to validate)
- **N:1**: Multiple originals → one enhanced (check no info lost)
- **1:N**: One original → multiple enhanced (verify logical split)
- **Contextual**: Enhanced uses multiple sources (validate attribution)

## Error Detection Priorities
1. **Orphaned content**: Original without mapping (critical error)
2. **Information loss**: Key details missing (critical error)
3. **Voice drift**: Enhanced text loses author style (major warning)
4. **Inflated metrics**: Quality scores don't match reality (major error)

## Validation Process
1. Structural check: All paragraphs mapped
2. Content comparison: Original vs enhanced analysis
3. Metric verification: Scores reflect actual changes
4. User experience test: Will double-tap work correctly?

## Output Requirements
- Overall accuracy score
- Detailed error log with severity
- Specific correction recommendations
- Production readiness assessment