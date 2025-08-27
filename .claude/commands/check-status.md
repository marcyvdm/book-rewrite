# Check Processing Status

Check the status of modular book processing pipeline.

**Usage**: `/check-status [processing-dir]`

## What This Checks

1. **Overall Progress**: Current phase and completion percentage
2. **Agent Status**: Which agents completed, failed, or are in progress  
3. **Output Validation**: Verify agent outputs exist and are valid
4. **Dependency Status**: Check if agents can proceed based on prerequisites
5. **Error Detection**: Identify any failed agents or missing outputs

## Example Usage

```bash
# Check current book processing status
/check-status processing/

# Check specific processing directory
/check-status "processed-books/game-feel/processing/"
```

## Status Report Format

The command will show:
- **Overall**: 65% complete, Phase 3 (paragraph enhancement)
- **Voice Analysis**: ✅ Completed (confidence: 91%)
- **Chapter Processing**: ✅ Completed (15 chapters analyzed)  
- **Paragraph Enhancement**: 🔄 In Progress (45/156 paragraphs)
- **Mapping Validation**: ⏳ Waiting for prerequisites
- **Refinement Analysis**: ⏳ Waiting for prerequisites

## Error Indicators
- ❌ Failed agents with error details
- ⚠️ Missing output files
- 🔄 Agents running too long (potential hang)
- 📁 Corrupted or invalid output files

Please check processing status for: $ARGUMENTS

Read the progress.json file and validate all agent outputs exist and are properly formatted.