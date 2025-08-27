# Incremental Processing Procedure

## Overview
Process books incrementally with modular outputs, state tracking, and recovery capability.

## Phase Coordination
1. **Check State**: Read `processing/state/progress.json` to determine current status
2. **Agent Dependencies**: Ensure prerequisite agents completed before starting
3. **Output Validation**: Verify previous agent outputs exist and are valid
4. **Incremental Execution**: Process only what hasn't been completed
5. **State Updates**: Update progress after each agent completion

## Agent Dependency Chain
```
voice-analyzer (independent)
    ↓
chapter-processor (needs voice rules)
    ↓  
paragraph-rewriter (needs voice + chapter analysis)
    ↓
mapping-validator (needs all paragraph enhancements)
    ↓
refinement-analyzer (needs completed mappings)
```

## Recovery Procedures

### Agent Failure Recovery
1. Check agent output location for partial results
2. Determine failure point from status logs
3. Resume from last successful checkpoint
4. Re-run only failed components, not entire pipeline

### Resume From Interruption  
1. Read `processing/state/progress.json`
2. Identify completed vs. pending agents
3. Validate existing outputs haven't been corrupted
4. Continue from next pending agent in dependency chain

## Processing Commands

### Check Status
```bash
/check-processing-status processing/state/progress.json
```

### Resume Processing  
```bash
/resume-processing processing/state/progress.json
```

### Validate Pipeline
```bash
/validate-pipeline processing/
```

## Quality Gates
Each phase must pass validation before next phase begins:
- Voice analysis: Must generate valid preservation rules
- Chapter processing: Must identify improvement areas
- Paragraph enhancement: Must achieve >80% average confidence
- Mapping validation: Must achieve >90% accuracy for production