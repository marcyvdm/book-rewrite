# Claude Code Instructions

## Workflow Synchronization Protocol

When the `process-book-workflow.md` is modified, follow these steps to keep all agents and commands in sync:

### 1. Workflow Change Detection
- **Always check** `process-book-workflow.md` before modifying any process-book related files
- **Compare current implementation** with the workflow document to identify discrepancies
- **Prioritize the workflow document** as the single source of truth

### 2. Agent Update Procedure

When workflow changes are detected, update agents in this order:

#### Step 1: Update Main Command
```bash
# File: .claude/commands/process-book.md
# Update based on: "Phase Definitions" and "Agent Dependencies" sections
# Ensure agent launch sequence matches workflow dependencies
```

#### Step 2: Update Individual Agents
For each agent mentioned in the workflow, check and update:

```bash
# Core Processing Agents:
.claude/agents/voice-analyzer.md        # Phase 2: Voice Analysis
.claude/agents/chapter-master.md        # Phase 2: Chapter Extraction  
.claude/agents/chapter-processor.md     # Phase 3: Parallel Processing
.claude/agents/paragraph-rewriter.md    # Phase 4: Enhancement
.claude/agents/mapping-validator.md     # Phase 4: Quality Validation
.claude/agents/refinement-analyzer.md   # Phase 5: Selective Refinement
```

#### Step 3: Verify Input/Output Contracts
- Check that each agent's expected inputs match the workflow's "Input" column
- Verify that each agent's outputs match the workflow's "Output" column
- Update agent prompts if input/output specifications have changed

#### Step 4: Update Time Estimates
- Use workflow "Time Est." column to set realistic timeout expectations
- Update any progress reporting to reflect new timing estimates
- Adjust parallel processing limits based on updated estimates

### 3. Configuration Sync

#### Command Arguments
```bash
# Sync CLI argument parsing with workflow "Configuration Options"
# File: .claude/commands/process-book.md
# Ensure all optional parameters from workflow are supported
```

#### Quality Gates
```bash
# Sync quality thresholds with workflow "Quality Gates" section
# Files to update:
# - .claude/agents/mapping-validator.md
# - .claude/context/core/quality-standards.md
```

#### Parallel Processing Rules
```bash
# Sync parallelization settings with workflow "Agent Dependencies"
# Update task scheduling logic in main command
```

### 4. Testing Protocol

After any workflow changes:

1. **Dry Run Test**: Process a small test file (--max-pages 5)
2. **Timing Validation**: Verify actual times are within workflow estimates
3. **Quality Gate Test**: Ensure quality thresholds are properly enforced
4. **Agent Communication Test**: Verify all input/output contracts work correctly

### 5. Change Documentation

When making workflow changes:

1. **Update this file** if new synchronization steps are needed
2. **Document the reason** for workflow changes in git commit messages
3. **Test thoroughly** before committing changes
4. **Update README.md** if user-facing behavior changes

## Quick Sync Command

Use this checklist when updating after workflow changes:

```markdown
- [ ] Read latest process-book-workflow.md
- [ ] Update .claude/commands/process-book.md
- [ ] Update all agent files listed in workflow
- [ ] Verify input/output contracts match
- [ ] Update time estimates and timeouts
- [ ] Sync configuration options
- [ ] Sync quality gates and thresholds
- [ ] Test with small sample file
- [ ] Update user documentation if needed
```

## Automated Sync Commands

When possible, use these commands to maintain consistency:

```bash
# Validate workflow compliance
/check-workflow-sync

# Update all agents from workflow
/sync-agents-to-workflow

# Test workflow with sample file
/test-workflow "sample.pdf" --max-pages 3
```

## Important Notes

- **Never modify agents without checking the workflow first**
- **Always update the workflow document before implementing changes**
- **Keep timing estimates realistic based on actual performance**
- **Quality gates are non-negotiable - maintain high standards**
- **Document any deviations from the workflow with clear reasoning**