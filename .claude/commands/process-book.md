# Process Book Workflow

Launch a complete book processing workflow using specialized subagents.

**Usage**: `/process-book <json-path> [options]`

## Workflow Steps

This command orchestrates the complete book processing pipeline:

1. **Load JSON**: Load pre-processed chapter data from JSON file
2. **Voice Analysis**: Analyze author's writing style and create voice fingerprint
3. **Chapter Processing**: Process chapters in parallel with specialized agents
4. **Paragraph Enhancement**: Enhance individual paragraphs while preserving voice
5. **Mapping Validation**: Validate all mappings and quality metrics
6. **Selective Refinement**: Apply Phase 5 refinement based on mapping insights
7. **Final Assembly**: Generate complete ProcessedBook JSON

## Arguments

- `<json-path>`: Path to the JSON file containing pre-processed chapters
- `--chapters`: Specific chapter numbers to process (comma-separated)
- `--output-dir`: Custom output directory
- `--parallel-chapters`: Number of chapters to process in parallel (default: 3)
- `--voice-sample-size`: Number of words to sample for voice analysis (default: 5000)

## Expected JSON Structure

The input JSON should contain chapter data with content items:

```json
{
  "chapter_title": "Chapter Title",
  "content": [
    {
      "type": "paragraph",
      "text": "Paragraph text..."
    },
    {
      "type": "heading",
      "level": 2,
      "text": "Section heading..."
    },
    {
      "type": "image",
      "src": "image.png",
      "caption": "Image caption..."
    },
    {
      "type": "list",
      "items": ["Item 1", "Item 2"]
    }
  ]
}
```

## Example Usage

```bash
# Process full book
/process-book "to-be-processed/book.json"

# Process specific chapters
/process-book "to-be-processed/book.json" --chapters 1,2,3

# Custom output directory
/process-book "to-be-processed/book.json" --output-dir "./output"

# Adjust parallel processing
/process-book "to-be-processed/book.json" --parallel-chapters 5
```

Please analyze the JSON file at: $ARGUMENTS

Launch the following subagents in sequence and parallel as needed:
1. Load and validate JSON structure
2. Launch voice-analyzer agent to create author style fingerprint from chapter samples
3. Launch chapter-processor agents for each chapter (parallel processing)
4. Launch paragraph-rewriter agent for enhancement
5. Launch mapping-validator agent for quality assurance
6. Launch refinement-analyzer agent for Phase 5 improvements

Coordinate all agents and generate final ProcessedBook JSON with complete mappings and quality reports.