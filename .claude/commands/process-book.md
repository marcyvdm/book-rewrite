# Process Book Workflow

Launch a complete book processing workflow using specialized subagents.

**Usage**: `/process-book <pdf-path> [options]`

## Workflow Steps

This command orchestrates the complete book processing pipeline:

1. **PDF Extraction**: Extract text, images, and structure from PDF
2. **Voice Analysis**: Analyze author's writing style and create voice fingerprint
3. **Chapter Processing**: Process chapters in parallel with specialized agents
4. **Paragraph Enhancement**: Enhance individual paragraphs while preserving voice
5. **Mapping Validation**: Validate all mappings and quality metrics
6. **Selective Refinement**: Apply Phase 5 refinement based on mapping insights
7. **Final Assembly**: Generate complete ProcessedBook JSON

## Arguments

- `<pdf-path>`: Path to the PDF file to process
- `--max-pages`: Limit pages processed (for testing)
- `--chapters`: Specific chapter numbers to process (comma-separated)
- `--skip-images`: Skip image extraction
- `--output-dir`: Custom output directory

## Example Usage

```bash
# Process full book
/process-book "to-be-processed/book.pdf"

# Process first 50 pages only
/process-book "to-be-processed/book.pdf" --max-pages 50

# Process specific chapters
/process-book "to-be-processed/book.pdf" --chapters 1,2,3

# Skip image processing for faster iteration
/process-book "to-be-processed/book.pdf" --skip-images
```

Please analyze the PDF at: $ARGUMENTS

Launch the following subagents in parallel:
1. Extract PDF content using the PDF extractor script
2. Launch voice-analyzer agent to create author style fingerprint
3. Launch chapter-processor agents for each chapter (parallel processing)
4. Launch paragraph-rewriter agent for enhancement
5. Launch mapping-validator agent for quality assurance
6. Launch refinement-analyzer agent for Phase 5 improvements

Coordinate all agents and generate final ProcessedBook JSON with complete mappings and quality reports.