# Book Processing System - How It Works

The `/process-book` command is a Claude Code slash command that transforms PDF books into enhanced, rewritten versions while preserving the author's voice and style.

## What It Does

The command takes a PDF book and creates an improved version with:
- **Better clarity** - Makes complex ideas easier to understand
- **Enhanced flow** - Improves transitions between paragraphs and ideas
- **Preserved voice** - Keeps the author's unique writing style intact
- **Smart structure** - Maintains the original organization and meaning

## How to Use It

```bash
# Basic usage - process an entire book
/process-book "path/to/your/book.pdf"

# Process only first 50 pages (good for testing)
/process-book "path/to/your/book.pdf" --max-pages 50

# Process specific chapters only
/process-book "path/to/your/book.pdf" --chapters 1,2,3

# Skip image processing for faster results
/process-book "path/to/your/book.pdf" --skip-images
```

## What Happens Behind the Scenes

The system uses multiple AI agents working together:

1. **PDF Extractor** - Pulls out text, images, and structure from the PDF
2. **Voice Analyzer** - Studies the author's writing style to create a "voice fingerprint"
3. **Chapter Processors** - Work on different chapters simultaneously for speed
4. **Paragraph Rewriter** - Improves individual paragraphs while keeping the author's voice
5. **Quality Checker** - Validates that changes maintain accuracy and quality
6. **Refinement Analyzer** - Makes final improvements based on the overall results

## The Result

You get a JSON file containing:
- **Original version** - The extracted book content
- **Rewritten version** - The improved version
- **Mappings** - Shows which original paragraphs became which rewritten ones
- **Quality reports** - Metrics on how well the process worked
- **Processing details** - Information about what was changed and why

## File Structure

The processed book follows a detailed schema (`src/types/schema.ts`) that includes:
- Book metadata (title, author, etc.)
- Chapter and paragraph organization
- Voice analysis results
- Quality metrics and improvement tracking
- Reading progress and user preferences

This system is designed for creating enhanced reading experiences while maintaining the integrity and voice of the original work.