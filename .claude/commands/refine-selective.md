# Selective Refinement (Phase 5)

Launch Phase 5 selective refinement analysis to identify paragraphs needing targeted improvements.

**Usage**: `/refine-selective <processed-book-path>`

## Purpose

Implements our advanced Phase 5 refinement process that analyzes completed mappings to identify selective improvement opportunities that only become apparent after seeing the full book context.

## Process

1. Launch refinement-analyzer subagent
2. Analyze all mappings for systematic patterns and issues
3. Identify paragraphs meeting refinement criteria
4. Prioritize improvements by impact and feasibility
5. Execute selective refinements only where beneficial
6. Update mappings with refinement history

## Refinement Criteria

Only refine paragraphs meeting specific thresholds:
- Information loss >15%
- Voice drift >25% 
- Broken cross-references
- Significant terminology inconsistencies
- Confidence improvement potential >10 points

## Arguments

- `<processed-book-path>`: Path to ProcessedBook JSON with completed initial processing

## Example Usage

```bash
# Run selective refinement analysis
/refine-selective "processed-books/book-processed.json"
```

Launch refinement-analyzer subagent for: $ARGUMENTS

The agent will:
- Analyze mapping patterns for systematic issues
- Identify selective refinement opportunities  
- Prioritize improvements by reader impact
- Execute targeted refinements with surgical precision
- Update ProcessedBook with refinement history and improved metrics

This represents our most advanced quality enhancement phase.