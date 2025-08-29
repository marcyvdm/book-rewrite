# PDF Extractor Development Plan

## Library Research Summary

### Best Options for Our Use Case:
1. **pdfplumber** (MIT License) - Best for structured extraction with table support
2. **pypdf** (BSD License) - Fast, pure Python, good for basic extraction  
3. **pdfminer.six** (MIT License) - Most detailed text positioning control
4. **PyMuPDF** (AGPL License) - Fastest but requires commercial license

**Recommendation**: Start with **pdfplumber** for comprehensive extraction capabilities with fallback to **pypdf** for speed.

---

## Exact Workflow Requirements

Based on `src/types/schema.ts` and `process-book-workflow.md`, the PDF extractor must output:

### Required Output Structure:
```json
{
  "metadata": {
    "title": "string",
    "author": "string", 
    "isbn": "string?",
    "publicationYear": "number?",
    "pageCount": "number?",
    "wordCount": "number",
    "language": "string",
    "sourceFormat": "pdf"
  },
  "rawText": "string", // Full book text for voice analysis
  "tableOfContents": [
    {
      "id": "string",
      "title": "string", 
      "level": "number", // 1=chapter, 2=section
      "pageNumber": "number?",
      "children": "TableOfContentsEntry[]"
    }
  ],
  "chapters": [
    {
      "id": "string",
      "number": "number",
      "title": "string",
      "pageNumbers": "[number, number]", // start, end
      "rawContent": "string"
    }
  ],
  "paragraphs": [
    {
      "id": "string",
      "chapterId": "string",
      "orderIndex": "number",
      "content": "string",
      "pageNumber": "number",
      "boundingBox": "{ x: number, y: number, width: number, height: number }?",
      "type": "text | quote | list | heading | caption", // inferred from formatting
      "wordCount": "number"
    }
  ],
  "images": [
    {
      "id": "string",
      "chapterId": "string",
      "type": "chart | diagram | photo | illustration | graph | table",
      "fileName": "string",
      "fileSize": "number",
      "width": "number", 
      "height": "number",
      "pageNumber": "number",
      "boundingBox": "{ x: number, y: number, width: number, height: number }",
      "caption": "string?",
      "altText": "string", // AI-generated description
      "rawData": "base64 string" // embedded image data
    }
  ],
  "citations": [
    {
      "id": "string",
      "type": "footnote | endnote | inline | bibliography",
      "content": "string",
      "pageNumber": "number?",
      "url": "string?"
    }
  ],
  "processingReport": {
    "extractionTimeMs": "number",
    "totalPages": "number",
    "pagesProcessed": "number",
    "imagesExtracted": "number",
    "tablesDetected": "number",
    "errors": "ProcessingError[]",
    "warnings": "ProcessingWarning[]"
  }
}
```

### Performance Requirements:
- **Target Time**: 30-120 seconds for typical business book (200-400 pages)
- **Memory Usage**: < 1GB peak memory for large PDFs
- **Error Handling**: Graceful degradation for corrupted/protected PDFs
- **Formats**: Support PDF 1.4+ with text layer

---

## Phase 1: Python PDF Extractor Design

### Architecture Design

```python
# Core Structure
class PDFExtractor:
    def __init__(self, config: ExtractionConfig):
        self.primary_engine = pdfplumber
        self.fallback_engine = pypdf  
        self.image_processor = PILImageProcessor()
        self.text_analyzer = TextStructureAnalyzer()
        
    def extract(self, pdf_path: str) -> ExtractionResult:
        """Main extraction pipeline"""
        
    def _extract_metadata(self) -> BookMetadata:
        """Extract title, author, page count, etc."""
        
    def _extract_toc(self) -> List[TableOfContentsEntry]:
        """Extract table of contents from bookmarks/structure"""
        
    def _extract_text_structure(self) -> Tuple[List[Chapter], List[Paragraph]]:
        """Extract chapters and paragraphs with positioning"""
        
    def _extract_images(self) -> List[ImageData]:  
        """Extract and process images with metadata"""
        
    def _extract_citations(self) -> List[Citation]:
        """Detect footnotes, endnotes, and bibliography"""
        
    def _classify_paragraphs(self) -> None:
        """Classify paragraph types (text, heading, quote, list, caption)"""
```

### Key Components:

#### 1. Text Structure Analysis
```python
class TextStructureAnalyzer:
    def detect_chapters(self, text_blocks: List[TextBlock]) -> List[Chapter]:
        # Heuristics: font size, "Chapter X", page breaks, TOC matching
        
    def detect_paragraphs(self, text_blocks: List[TextBlock]) -> List[Paragraph]:  
        # Group by spacing, indentation, font consistency
        
    def classify_paragraph_type(self, paragraph: Paragraph) -> ParagraphType:
        # Rules: font size (heading), indentation (quote), bullets (list)
```

#### 2. Multi-Engine Extraction
```python
class MultiEngineExtractor:
    def extract_with_fallback(self, pdf_path: str) -> RawExtractionData:
        try:
            return self._extract_pdfplumber(pdf_path)
        except Exception as e:
            logger.warning(f"pdfplumber failed: {e}, trying pypdf")
            return self._extract_pypdf(pdf_path)
```

#### 3. Image Processing
```python  
class ImageProcessor:
    def extract_images(self, pdf_path: str) -> List[ImageData]:
        # Extract images with positioning, classify type, generate alt text
        
    def classify_image_type(self, image_data: bytes) -> ImageType:
        # ML-based classification: chart, diagram, photo, etc.
        
    def generate_alt_text(self, image_data: bytes) -> str:
        # Use vision model for accessibility description
```

### Python Best Practices Implementation:

#### Project Structure:
```
pdf_extractor/
├── __init__.py
├── core/
│   ├── __init__.py  
│   ├── extractor.py         # Main PDFExtractor class
│   ├── engines/
│   │   ├── __init__.py
│   │   ├── pdfplumber_engine.py
│   │   └── pypdf_engine.py
│   ├── processors/
│   │   ├── __init__.py
│   │   ├── text_processor.py
│   │   ├── image_processor.py
│   │   └── citation_processor.py
│   └── analyzers/
│       ├── __init__.py
│       ├── structure_analyzer.py
│       └── content_classifier.py
├── models/
│   ├── __init__.py
│   └── extraction_models.py    # Pydantic models
├── utils/
│   ├── __init__.py
│   ├── logging_config.py
│   ├── error_handling.py
│   └── validation.py
├── tests/
│   ├── __init__.py
│   ├── test_extractor.py
│   ├── test_engines.py
│   └── fixtures/
│       └── sample_pdfs/
└── scripts/
    ├── extract_pdf.py          # CLI script
    └── benchmark.py
```

#### Configuration:
```python
# config.py
from pydantic import BaseSettings

class ExtractionConfig(BaseSettings):
    # Engine settings
    primary_engine: str = "pdfplumber"
    fallback_engine: str = "pypdf"
    
    # Performance settings
    max_memory_mb: int = 1024
    timeout_seconds: int = 300
    parallel_pages: bool = True
    
    # Quality settings
    min_paragraph_words: int = 3
    image_min_size: Tuple[int, int] = (50, 50)
    extract_tables: bool = True
    extract_images: bool = True
    
    # Output settings
    preserve_formatting: bool = True
    include_positioning: bool = True
    
    class Config:
        env_prefix = "PDF_EXTRACTOR_"
```

#### Error Handling & Logging:
```python
# error_handling.py
import logging
from enum import Enum
from typing import List, Optional

class ExtractionErrorType(Enum):
    PDF_CORRUPTED = "pdf_corrupted"
    PASSWORD_PROTECTED = "password_protected" 
    NO_TEXT_LAYER = "no_text_layer"
    MEMORY_LIMIT = "memory_limit"
    ENGINE_FAILURE = "engine_failure"

@dataclass
class ExtractionError:
    error_type: ExtractionErrorType
    message: str
    page_number: Optional[int] = None
    recoverable: bool = True
```

#### Performance Optimization:
```python
# performance.py
from concurrent.futures import ThreadPoolExecutor
import psutil
from functools import lru_cache

class PerformanceOptimizer:
    @staticmethod
    def process_pages_parallel(pages: List[Page], processor_func) -> List[Result]:
        # Parallel processing with memory monitoring
        
    @staticmethod  
    @lru_cache(maxsize=128)
    def cached_font_analysis(font_key: str) -> FontMetadata:
        # Cache expensive font analysis
        
    @staticmethod
    def monitor_memory_usage() -> bool:
        # Return True if memory usage is acceptable
```

---

## Phase 2: Claude Subagent Assistance Plan

### Agent Model Constraints:
- **Fire-and-Forget**: Agents launch scripts and wait for completion
- **No Dynamic Interaction**: Cannot communicate with running processes
- **Output-Based Decisions**: Agents read final outputs and decide next actions
- **Iterative Enhancement**: Multiple script runs with refined inputs

### Multi-Pass Architecture:

#### Pass 1: Initial Extraction (Python Script)
```bash
# Command: python extract_pdf.py book.pdf --pass=initial
# Output: initial_extraction.json with confidence scores
```

#### Pass 2: Agent Enhancement (If Needed)
```python
# Agent reads initial_extraction.json and decides:
if extraction_result.chapter_confidence < 0.6:
    # Launch enhanced chapter detection
    run_script("extract_pdf.py", "book.pdf", "--pass=chapter-enhance", 
               "--chapter-hints=chapter_candidates.json")

if extraction_result.images_needing_descriptions > 0:
    # Launch image analysis pass
    run_script("extract_pdf.py", "book.pdf", "--pass=image-enhance",
               "--focus-images=low_confidence_images.json")
```

#### Pass 3: Final Assembly
```python
# Merge all enhancement passes into final result
run_script("extract_pdf.py", "book.pdf", "--pass=final-merge",
           "--merge-files=initial.json,chapter_enhanced.json,image_enhanced.json")
```

### Multi-Pass Script Architecture:

```python
class PDFExtractor:
    def extract(self, pdf_path: str, pass_type: str, **kwargs) -> ExtractionResult:
        match pass_type:
            case "initial":
                return self._initial_extraction(pdf_path)
            case "chapter-enhance":
                return self._enhance_chapters(pdf_path, kwargs.get('chapter_hints'))
            case "image-enhance":
                return self._enhance_images(pdf_path, kwargs.get('focus_images'))
            case "final-merge":
                return self._merge_results(pdf_path, kwargs.get('merge_files'))
            case _:
                return self._full_extraction(pdf_path)
    
    def _initial_extraction(self, pdf_path: str) -> ExtractionResult:
        # Full extraction with confidence scoring
        result = self._base_extract(pdf_path)
        result.confidence_report = self._analyze_confidence(result)
        return result
    
    def _enhance_chapters(self, pdf_path: str, hints_file: str) -> ExtractionResult:
        # Focused re-processing with agent-provided hints
        hints = load_json(hints_file)
        return self._extract_chapters_with_hints(pdf_path, hints)
        
    def _merge_results(self, pdf_path: str, merge_files: List[str]) -> ExtractionResult:
        # Intelligent merging of multiple extraction passes
        results = [load_json(f) for f in merge_files]
        return self._smart_merge(results)
```

### Agent Decision Logic:

#### Agent-Based Quality Assessment 

**Step 1**: Python script outputs extraction samples for agent review
```python
# initial_extraction.json includes samples for agent assessment
{
  "extraction_samples": {
    "chapter_detection_sample": {
      "detected_chapters": [
        {"title": "Introduction", "page": 1, "content_preview": "...first 200 chars..."},
        {"title": "Chapter 1", "page": 15, "content_preview": "..."},
        {"title": "Section 1.1", "page": 18, "content_preview": "..."}  # Possible false positive
      ],
      "ambiguous_boundaries": [
        {"page": 25, "possible_titles": ["Getting Started", "Chapter 2"], "context": "..."}
      ],
      "toc_comparison": "Table of Contents shows 8 chapters, detected 12 potential chapters"
    },
    "image_sample": [
      {
        "image_id": "img_p23_01", 
        "auto_description": "Chart with bars and numbers",
        "context_before": "Sales increased dramatically in Q3...",
        "context_after": "This trend continued into Q4...",
        "needs_review": true
      }
    ],
    "citation_sample": [
      {
        "text": "According to Smith (2019), the methodology...",
        "detected_type": "inline",
        "certainty": "high"
      },
      {
        "text": "1. Johnson, M. et al. Advanced Techniques...",
        "detected_type": "bibliography",
        "certainty": "medium"
      }
    ]
  },
  "extraction_stats": {
    "total_chapters_detected": 12,
    "total_paragraphs": 847,
    "total_images": 23,
    "total_citations": 156,
    "processing_warnings": ["Inconsistent heading styles", "Mixed citation formats"]
  }
}
```

**Step 2**: Agent evaluates samples and provides assessment
```markdown
# Agent analyzes samples and outputs: extraction_assessment.json
{
  "quality_assessment": {
    "chapter_detection": {
      "confidence": 0.4,  # Agent's assessment
      "issues": [
        "Incorrectly splitting sections into chapters",
        "Missing 'Conclusion' chapter mentioned in TOC",
        "Treating appendices as regular chapters"
      ],
      "needs_enhancement": true,
      "enhancement_priority": "high"
    },
    "image_analysis": {
      "confidence": 0.2,
      "issues": [
        "Generic descriptions like 'Chart with bars' not useful",
        "Missing context integration for technical diagrams", 
        "No classification of chart types"
      ],
      "needs_enhancement": true,
      "enhancement_priority": "high"
    },
    "citation_detection": {
      "confidence": 0.85,
      "issues": ["Mixed formats handled well"],
      "needs_enhancement": false
    }
  },
  "recommended_actions": [
    {
      "action": "chapter_reprocessing",
      "reason": "Current detection conflates sections with chapters",
      "expected_improvement": "Should reduce from 12 to 8 chapters per TOC"
    },
    {
      "action": "image_enhancement",
      "reason": "Technical diagrams need contextual descriptions",
      "expected_improvement": "Meaningful alt-text for accessibility"
    }
  ]
}
```

#### Agent-Specific Enhancement Passes:

##### chapter-master Pass
```markdown
# Agent reads: initial_extraction.json
# Agent generates: chapter_enhancement_hints.json with:
{
  "suggested_chapter_boundaries": [
    {"page": 15, "title": "Introduction to Systems Thinking", "confidence": 0.95},
    {"page": 42, "title": "Chapter 1: Core Principles", "confidence": 0.88}
  ],
  "reasoning": "Detected consistent heading patterns and topic shifts",
  "processing_notes": "Consider merging sections 2.1-2.3 into single chapter"
}

# Agent launches: python extract_pdf.py book.pdf --pass=chapter-enhance --hints=chapter_enhancement_hints.json
```

##### image-analyzer Pass  
```markdown
# Agent processes each low-confidence image individually
# Creates: image_descriptions.json
{
  "image_enhancements": [
    {
      "image_id": "img_page_23_01",
      "enhanced_description": "Flow diagram showing customer journey from awareness to purchase...",
      "content_type": "process_diagram",
      "key_insights": ["3-stage funnel", "conversion rates at each stage"]
    }
  ]
}

# Agent launches: python extract_pdf.py book.pdf --pass=image-enhance --descriptions=image_descriptions.json
```

### Agent-Driven Enhancement Flow:

```python
class AgentCoordinatedExtractor:
    def coordinate_extraction(self, pdf_path: str) -> ExtractionResult:
        # Pass 1: Initial extraction with samples
        initial = self._run_extraction_pass(pdf_path, "initial-with-samples")
        
        # Pass 2: Agent assessment (agent reads samples, outputs assessment)
        assessment = self._agent_assess_quality(initial.samples_file)
        
        enhancement_passes = []
        
        # Pass 3+: Enhancement passes based on agent decisions
        for action in assessment.recommended_actions:
            if action.action == "chapter_reprocessing":
                # Agent creates enhancement hints
                hints = self._agent_generate_chapter_hints(
                    initial.samples_file, 
                    action.specific_guidance
                )
                enhanced = self._run_extraction_pass(
                    pdf_path, "chapter-enhance", hints=hints
                )
                enhancement_passes.append(enhanced)
            
            elif action.action == "image_enhancement":
                # Agent creates detailed descriptions
                descriptions = self._agent_generate_image_descriptions(
                    initial.samples_file,
                    focus_images=action.target_images
                )
                enhanced = self._run_extraction_pass(
                    pdf_path, "image-enhance", descriptions=descriptions
                )
                enhancement_passes.append(enhanced)
        
        # Final pass: Merge all results
        if enhancement_passes:
            final_result = self._run_extraction_pass(
                pdf_path, "final-merge",
                base_file=initial.output_file,
                enhancement_files=[p.output_file for p in enhancement_passes]
            )
        else:
            final_result = initial
            
        return final_result

    def _agent_assess_quality(self, samples_file: str) -> AssessmentResult:
        """
        Agent reads samples and provides quality assessment.
        This is where the agent uses its intelligence to evaluate
        extraction quality rather than relying on hardcoded thresholds.
        """
        # Agent task: read samples_file, analyze quality, output assessment
        return self._launch_agent("extraction-assessor", {
            "samples_file": samples_file,
            "task": "assess_extraction_quality_and_recommend_actions"
        })
```

### Sample-Based Assessment Strategy:

```python
class SampleGenerator:
    def generate_assessment_samples(self, extraction_result: ExtractionResult) -> SamplesFile:
        """Generate representative samples for agent assessment"""
        
        samples = {
            "chapter_analysis": self._sample_chapter_detection(extraction_result),
            "image_analysis": self._sample_image_extraction(extraction_result), 
            "citation_analysis": self._sample_citation_detection(extraction_result),
            "paragraph_analysis": self._sample_paragraph_structure(extraction_result),
            "metadata_analysis": self._sample_metadata_extraction(extraction_result)
        }
        
        return SamplesFile(samples)
    
    def _sample_chapter_detection(self, result: ExtractionResult) -> Dict:
        """Provide chapter detection samples with context for agent review"""
        return {
            "toc_vs_detected": {
                "toc_chapters": result.table_of_contents,
                "detected_chapters": result.chapters[:10],  # First 10 for review
                "discrepancies": result.detect_toc_discrepancies()
            },
            "boundary_confidence": [
                # Show uncertain chapter boundaries for agent review
                ch for ch in result.chapters if ch.boundary_confidence < 0.8
            ],
            "context_samples": [
                # Show text around chapter boundaries
                self._get_boundary_context(ch) for ch in result.chapters[:5]
            ]
        }
    
    def _sample_image_extraction(self, result: ExtractionResult) -> Dict:
        """Provide image samples focusing on those needing better descriptions"""
        return {
            "low_quality_descriptions": [
                img for img in result.images 
                if len(img.auto_description.split()) < 5  # Generic descriptions
            ],
            "technical_diagrams": [
                img for img in result.images 
                if img.detected_type in ["chart", "diagram", "graph"]
            ],
            "context_integration": [
                {
                    "image": img,
                    "preceding_text": self._get_text_before(img, 100),
                    "following_text": self._get_text_after(img, 100)
                }
                for img in result.images[:5]
            ]
        }
```

---

## Phase 3: Build and Integration Plan

### Step 1: Core Python Implementation (Week 1)
```bash
# Implementation order:
1. Set up project structure with pydantic models
2. Implement pdfplumber engine with basic extraction
3. Add pypdf fallback engine  
4. Create text structure analyzer
5. Add image extraction capabilities
6. Implement basic citation detection
7. Add comprehensive error handling and logging
```

### Step 2: Agent Integration (Week 2)  
```bash
# Integration tasks:
1. Create AgentOrchestrator class
2. Implement quality gates and trigger conditions
3. Create Claude agent specifications for:
   - Enhanced chapter detection
   - Image analysis and alt text generation
   - Citation processing
   - Table extraction enhancement
4. Add async agent communication
5. Implement result merging logic
```

### Step 3: Workflow Integration (Week 3)
```bash
# Integration with process-book command:
1. Update process-book-workflow.md with new extraction specs
2. Create pdf-extractor CLI script  
3. Update .claude/commands/process-book.md to use new extractor
4. Add extraction validation and quality reporting
5. Integration testing with sample PDFs
6. Performance optimization and benchmarking
```

### Integration Points:

#### 1. Command Line Interface
```python
# scripts/extract_pdf.py
import click
from pdf_extractor import PDFExtractor, ExtractionConfig

@click.command()
@click.argument('pdf_path', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output JSON file')
@click.option('--use-agents/--no-agents', default=True, help='Use Claude agents for enhancement')
@click.option('--config', type=click.Path(), help='Configuration file')
def extract_pdf(pdf_path: str, output: str, use_agents: bool, config: str):
    """Extract structured content from PDF for book processing workflow."""
    
    # Load configuration
    if config:
        extraction_config = ExtractionConfig.parse_file(config)
    else:
        extraction_config = ExtractionConfig()
    
    # Initialize extractor
    extractor = PDFExtractor(extraction_config)
    
    # Extract content
    result = extractor.extract(pdf_path, use_claude_agents=use_agents)
    
    # Save results
    output_path = output or f"{pdf_path.stem}_extracted.json"
    result.save_json(output_path)
    
    click.echo(f"✅ Extraction complete: {output_path}")
    click.echo(f"📊 Stats: {len(result.chapters)} chapters, {len(result.paragraphs)} paragraphs, {len(result.images)} images")
```

#### 2. Process Book Integration
```markdown
# Update to .claude/commands/process-book.md

## Phase 2: Content Extraction  
| Step | Agent | Input | Output | Time Est. |
|------|-------|-------|--------|-----------|
| Extract PDF Content | pdf-extractor-script | PDF file + config | StructuredExtractionResult.json | 30-120s |
| Validate Extraction | extraction-validator | Extraction result | Quality report + fixes | 15-30s |
| Analyze Author Voice | voice-analyzer | Raw text from extraction | VoiceAnalysis object | 60-180s |
| Process Chapters | chapter-master | Structured chapters from extraction | Enhanced chapter boundaries | 15-45s |
```

### Testing Strategy:

#### 1. Unit Tests
```python
# tests/test_extractor.py
class TestPDFExtractor:
    def test_basic_text_extraction(self):
        # Test with simple PDF
        
    def test_chapter_detection(self):
        # Test chapter boundary detection
        
    def test_image_extraction(self):  
        # Test image processing
        
    def test_citation_detection(self):
        # Test citation parsing
        
    def test_fallback_engine(self):
        # Test engine switching on failure
```

#### 2. Integration Tests
```python  
# tests/test_integration.py
class TestWorkflowIntegration:
    def test_end_to_end_extraction(self):
        # Full extraction pipeline test
        
    def test_claude_agent_integration(self):
        # Test agent enhancement workflow
        
    def test_process_book_command_integration(self):
        # Test integration with main workflow
```

### Performance Benchmarks:

#### Target Metrics:
- **Small PDF** (< 50 pages): < 30 seconds
- **Medium PDF** (50-200 pages): 30-90 seconds  
- **Large PDF** (200+ pages): 60-120 seconds
- **Memory Usage**: < 1GB peak
- **Accuracy**: > 95% paragraph detection, > 90% chapter detection

This plan provides a comprehensive roadmap for building a production-ready PDF extractor that integrates seamlessly with your existing book processing workflow while leveraging Claude agents only when necessary for enhanced quality.