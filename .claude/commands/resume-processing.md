# Resume Processing

Resume book processing from where it left off using modular state tracking.

**Usage**: `/resume-processing <processing-dir>`

## What This Does

1. **Read Current State**: Load `processing/state/progress.json` to determine where processing stopped
2. **Validate Existing Work**: Verify completed agent outputs haven't been corrupted  
3. **Check Prerequisites**: Ensure all dependencies are met for next agent
4. **Continue Pipeline**: Execute next pending agent in dependency chain
5. **Update State**: Track progress as agents complete

## Processing Pipeline Order
```
voice-analyzer → chapter-processor → paragraph-rewriter → mapping-validator → refinement-analyzer
```

## Recovery Scenarios

**Clean Resume**: All previous work valid, continue from next pending agent
**Partial Recovery**: Some outputs corrupted, re-run affected agents only  
**Full Recovery**: Major corruption detected, restart from last known good state

## Example Usage

```bash
# Resume processing from current state
/resume-processing "processing/"

# Resume processing with specific book
/resume-processing "processed-books/game-feel/processing/"
```

## Safety Checks

Before resuming:
- ✅ Validate all completed agent outputs are properly formatted
- ✅ Check file integrity and required fields  
- ✅ Verify dependency chain is intact
- ✅ Confirm no agents are currently running (prevent conflicts)

## Progress Reporting

Shows real-time progress:
- **Current Phase**: Which agent is running
- **Completion %**: Overall pipeline progress
- **ETA**: Estimated time to completion based on previous agent performance
- **Quality Metrics**: Running average of confidence scores

## Failure Handling

If resume fails:
- Detailed error report with specific failure point
- Recommendations for manual intervention  
- Options to restart from earlier checkpoint
- Preservation of all valid work completed so far

Please resume processing from: $ARGUMENTS

Read the current state, validate existing outputs, and continue the pipeline from the next pending agent.