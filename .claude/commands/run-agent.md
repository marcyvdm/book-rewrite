# Run Individual Agent

Execute a specific agent in the book processing pipeline with proper state management.

**Usage**: `/run-agent <agent-name> <input-path> [processing-dir]`

## Available Agents

- **voice-analyzer**: Analyze author's writing style and create voice fingerprint
- **chapter-processor**: Process individual chapters for structure and improvement areas
- **paragraph-rewriter**: Enhance paragraphs while preserving author voice
- **mapping-validator**: Validate all paragraph mappings for quality assurance
- **refinement-analyzer**: Identify selective refinement opportunities

## Prerequisites Checking

The command will automatically:
1. Check if prerequisite agents have completed
2. Validate required input files exist
3. Ensure processing directory structure exists
4. Update state tracking before and after execution

## Example Usage

```bash
# Run voice analysis on extracted book content
/run-agent voice-analyzer "extracted-content/book-extracted.json"

# Run paragraph rewriter (requires voice analysis completed)  
/run-agent paragraph-rewriter "extracted-content/book-extracted.json" "processing/"

# Run mapping validation (requires paragraph enhancement completed)
/run-agent mapping-validator "processing/" "processing/"
```

## State Management

Before running:
- Validates prerequisites are met
- Updates `processing/state/progress.json` to mark agent as "in-progress"

After completion:
- Validates agent output was created successfully  
- Updates progress status to "completed" or "failed"
- Logs execution time and confidence scores

## Error Handling

If agent fails:
- Status marked as "failed" with error details
- Partial outputs preserved for debugging
- Clear instructions provided for manual recovery

Please run the **$ARGUMENTS** agent with proper prerequisite checking and state management.