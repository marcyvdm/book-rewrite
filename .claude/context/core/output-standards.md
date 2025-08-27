# Agent Output Standards

## Core Principle
Each agent outputs to its own modular location. No massive files. No overwrites.

## Output Structure
```
processing/
├── state/              # Progress tracking
├── voice-analysis/     # Voice analyzer outputs
├── chapter-analysis/   # Chapter processor outputs  
├── paragraph-enhancement/ # Paragraph rewriter outputs
├── mappings/           # Mapping validator outputs
└── final/              # Final assembled results
```

## Naming Conventions
- **Individual items**: `item-{ID}.json` (e.g., `enhanced-p001.json`)
- **Summaries**: `{type}-summary.json` (e.g., `enhancement-summary.json`)  
- **Status tracking**: `progress.json`, `agent-status.json`

## Required Output Fields
Every agent output must include:
```json
{
  "agentType": "voice-analyzer",
  "inputId": "source-identifier", 
  "status": "completed|failed|in-progress",
  "timestamp": "2025-01-01T00:00:00Z",
  "confidenceScore": 85,
  "processingTimeMs": 1500
}
```

## File Size Limits
- Individual outputs: <50KB recommended
- Summary files: <200KB maximum
- Break large outputs into multiple files

## Error Handling
- Failed outputs must include error details
- Partial results should be saved before failure
- Status must be updated to reflect actual state