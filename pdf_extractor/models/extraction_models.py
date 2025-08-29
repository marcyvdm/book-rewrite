"""
Pydantic models for PDF extraction data structures.
Based on the schema defined in src/types/schema.ts
"""

from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Any
from pydantic import BaseModel, Field, validator, ConfigDict, field_validator
import json


class DocumentType(str, Enum):
    ACADEMIC = "academic"
    BUSINESS = "business" 
    TECHNICAL = "technical"
    BIOGRAPHY = "biography"
    SCIENCE = "science"
    SELF_HELP = "self-help"
    OTHER = "other"


class SourceFormat(str, Enum):
    PDF = "pdf"
    EPUB = "epub"
    TXT = "txt"
    COPYPASTE = "copypaste"


class ParagraphType(str, Enum):
    TEXT = "text"
    QUOTE = "quote"
    LIST = "list"
    HEADING = "heading"
    CAPTION = "caption"
    CODE = "code"


class ImageType(str, Enum):
    CHART = "chart"
    DIAGRAM = "diagram"
    PHOTO = "photo"
    ILLUSTRATION = "illustration"
    GRAPH = "graph"
    TABLE = "table"


class CitationType(str, Enum):
    FOOTNOTE = "footnote"
    ENDNOTE = "endnote"
    INLINE = "inline"
    BIBLIOGRAPHY = "bibliography"


class ImportanceLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TextPosition(str, Enum):
    INLINE = "inline"
    ABOVE = "above"
    BELOW = "below"
    SIDE = "side"
    FLOAT = "float"
    ISOLATED = "isolated"


class ColumnPosition(str, Enum):
    LEFT = "left"
    RIGHT = "right"
    CENTER = "center"
    SPAN = "span"


class BoundingBox(BaseModel):
    """Bounding box coordinates"""
    x: float
    y: float
    width: float
    height: float


class FlowContext(BaseModel):
    """How text flows around an image"""
    wrapping_style: str = Field(..., description="none, left, right, both")
    text_density_around: float = Field(..., ge=0.0, le=1.0)
    creates_column_break: bool = False


class ReferenceMention(BaseModel):
    """Reference to image in text"""
    text: str = Field(..., description="The reference text like 'See Figure 1'")
    type: str = Field(..., description="explicit_reference or implicit_reference")
    paragraph_id: str
    position_in_text: int
    reference_number: Optional[str] = None


class SpatialRelationships(BaseModel):
    """Spatial relationship counts"""
    paragraphs_above: int
    paragraphs_below: int
    paragraphs_alongside: int


class BookMetadata(BaseModel):
    """Book metadata information"""
    id: str
    title: str
    author: str
    isbn: Optional[str] = None
    publication_year: Optional[int] = None
    genre: str
    category: DocumentType
    language: str = "en"
    page_count: Optional[int] = None
    word_count: int
    reading_level: float = Field(..., description="Flesch-Kincaid grade level")
    source_format: SourceFormat = SourceFormat.PDF
    processing_date: str
    processing_version: str
    estimated_reading_time_minutes: int
    tags: List[str] = Field(default_factory=list)


class VoiceAnalysis(BaseModel):
    """Author voice analysis results"""
    average_sentence_length: float
    vocabulary_complexity: str = Field(..., description="simple, moderate, complex")
    tone_descriptors: List[str]
    rhetorical_devices: List[str] 
    perspective: str = Field(..., description="first-person, third-person, mixed")
    formality_level: int = Field(..., ge=1, le=10)
    technicality_level: int = Field(..., ge=1, le=10)
    personality_traits: List[str]
    style_fingerprint: str


class Citation(BaseModel):
    """Citation information"""
    id: str
    type: CitationType
    content: str
    page_number: Optional[int] = None
    url: Optional[str] = None


class Paragraph(BaseModel):
    """Paragraph with classification and metadata"""
    id: str
    chapter_id: str
    section_id: Optional[str] = None
    order_index: int
    content: str
    word_count: int
    type: ParagraphType
    importance: ImportanceLevel
    concepts: List[str] = Field(default_factory=list)
    technical_terms: List[str] = Field(default_factory=list)
    citations: List[Citation] = Field(default_factory=list)
    page_number: int
    bounding_box: Optional[BoundingBox] = None
    font_info: Optional[Dict[str, Any]] = None
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)


class ImageData(BaseModel):
    """Enhanced image data with positioning"""
    id: str
    chapter_id: str
    paragraph_id: Optional[str] = None
    type: ImageType
    file_name: str
    file_size: int
    width: int
    height: int
    caption: Optional[str] = None
    alt_text: str
    description: str
    relevance_score: float = Field(..., ge=0.0, le=10.0)
    preservation_notes: str = ""
    improvement_suggestions: List[str] = Field(default_factory=list)
    
    # Enhanced positioning data
    page_number: int
    bounding_box: BoundingBox
    text_position: TextPosition
    paragraph_before_id: Optional[str] = None
    paragraph_after_id: Optional[str] = None
    column_position: ColumnPosition
    flow_context: FlowContext
    reference_mentions: List[ReferenceMention] = Field(default_factory=list)
    spatial_relationships: SpatialRelationships
    
    # Processing metadata
    raw_data: Optional[str] = None  # Base64 encoded image data
    description_confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    extracted_text: Optional[str] = None  # OCR text if applicable
    
    @field_validator('width', 'height')
    @classmethod
    def convert_float_to_int(cls, v):
        """Convert float values to integers for width and height"""
        if isinstance(v, float):
            return int(round(v))
        return v


class Chapter(BaseModel):
    """Chapter information"""
    id: str
    number: int
    title: str
    summary: str = ""
    key_points: List[str] = Field(default_factory=list)
    word_count: int
    section_ids: List[str] = Field(default_factory=list)
    paragraph_ids: List[str] = Field(default_factory=list)
    image_ids: List[str] = Field(default_factory=list)
    learning_objectives: Optional[List[str]] = None
    difficulty: str = Field(default="intermediate", description="beginner, intermediate, advanced")
    page_number: int
    page_range: Optional[Tuple[int, int]] = None
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)


class Section(BaseModel):
    """Document section"""
    id: str
    chapter_id: str
    title: Optional[str] = None
    order_index: int
    paragraph_ids: List[str] = Field(default_factory=list)
    type: str = Field(default="main-content", description="introduction, main-content, conclusion, example, case-study")


class TableOfContentsEntry(BaseModel):
    """Table of contents entry"""
    id: str
    title: str
    level: int = Field(..., description="1 for chapter, 2 for section, etc.")
    page_number: Optional[int] = None
    chapter_id: Optional[str] = None
    section_id: Optional[str] = None
    children: List['TableOfContentsEntry'] = Field(default_factory=list)


class PDFProfile(BaseModel):
    """PDF characteristics analysis"""
    document_type: str
    structure_complexity: float = Field(..., ge=0.0, le=1.0)
    text_quality: float = Field(..., ge=0.0, le=1.0) 
    layout_type: str = Field(..., description="single_column, two_column, complex")
    has_toc: bool
    chapter_pattern: str = Field(..., description="numbered, named, mixed")
    citation_style: str = Field(..., description="apa, mla, ieee, mixed, none")
    image_density: float = Field(..., ge=0.0)
    table_density: float = Field(..., ge=0.0)
    font_consistency: float = Field(..., ge=0.0, le=1.0)


class ProcessingError(BaseModel):
    """Processing error information"""
    phase: str
    error_code: str
    message: str
    severity: str = Field(..., description="low, medium, high, critical")
    timestamp: str
    affected_paragraph_ids: List[str] = Field(default_factory=list)
    resolution: Optional[str] = None


class ProcessingWarning(BaseModel):
    """Processing warning information"""  
    phase: str
    warning_code: str
    message: str
    timestamp: str
    affected_paragraph_ids: List[str] = Field(default_factory=list)
    recommendation: str


class QualityMetrics(BaseModel):
    """Quality assessment metrics"""
    overall_confidence: float = Field(..., ge=0.0, le=1.0)
    structure_confidence: float = Field(..., ge=0.0, le=1.0)
    content_confidence: float = Field(..., ge=0.0, le=1.0)
    image_confidence: float = Field(..., ge=0.0, le=1.0)
    citation_confidence: float = Field(..., ge=0.0, le=1.0)


class ProcessingReport(BaseModel):
    """Comprehensive processing report"""
    total_processing_time_ms: int
    pdf_profile: PDFProfile
    extraction_strategy: str
    quality_metrics: QualityMetrics
    errors: List[ProcessingError] = Field(default_factory=list)
    warnings: List[ProcessingWarning] = Field(default_factory=list)
    performance_stats: Dict[str, Any] = Field(default_factory=dict)
    agent_enhancements_used: List[str] = Field(default_factory=list)


class BookContent(BaseModel):
    """Complete book content structure"""
    metadata: BookMetadata
    voice_analysis: Optional[VoiceAnalysis] = None
    chapters: List[Chapter] = Field(default_factory=list)
    sections: List[Section] = Field(default_factory=list)
    paragraphs: List[Paragraph] = Field(default_factory=list)
    images: List[ImageData] = Field(default_factory=list)
    table_of_contents: List[TableOfContentsEntry] = Field(default_factory=list)
    citations: List[Citation] = Field(default_factory=list)


class ExtractionResult(BaseModel):
    """Complete PDF extraction result"""
    id: str
    pdf_path: str
    processing_timestamp: datetime
    book_content: BookContent
    processing_report: ProcessingReport
    
    # File paths for coordination system
    samples_file: Optional[str] = None
    assessment_file: Optional[str] = None
    enhancement_files: Dict[str, str] = Field(default_factory=dict)
    
    model_config = ConfigDict(
        # Allow arbitrary types for complex objects
        arbitrary_types_allowed=True,
        # Use enum values in serialization
        use_enum_values=True
    )
    
    def save_to_file(self, file_path: Union[str, Path]) -> None:
        """Save extraction result to JSON file"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.model_dump(), f, indent=2, ensure_ascii=False, default=str)
    
    @classmethod
    def load_from_file(cls, file_path: Union[str, Path]) -> 'ExtractionResult':
        """Load extraction result from JSON file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.model_validate(data)
    
    @property
    def overall_confidence(self) -> float:
        """Overall extraction confidence score"""
        return self.processing_report.quality_metrics.overall_confidence


# Enable forward references
TableOfContentsEntry.model_rebuild()


# Configuration models
class ExtractionConfig(BaseModel):
    """Configuration for PDF extraction"""
    # Engine preferences
    primary_engine: str = "pdfplumber"
    fallback_engines: List[str] = Field(default_factory=lambda: ["pypdf", "pdfminer.six"])
    
    # Quality thresholds
    min_chapter_confidence: float = 0.7
    min_paragraph_confidence: float = 0.8
    min_image_confidence: float = 0.6
    min_overall_confidence: float = 0.8
    
    # Processing options
    enable_ocr_fallback: bool = True
    max_processing_time: int = 300  # seconds
    enable_self_correction: bool = True
    max_correction_attempts: int = 2
    
    # Agent coordination
    enable_agent_enhancements: bool = True
    max_enhancement_passes: int = 3
    parallel_agent_processing: bool = True
    
    # Output options
    include_positioning_data: bool = True
    include_font_information: bool = True
    generate_confidence_scores: bool = True
    create_processing_report: bool = True
    include_raw_image_data: bool = False
    
    # Performance tuning
    parallel_processing: bool = True
    max_workers: int = 4
    memory_limit_mb: int = 2048
    
    # Adaptive behavior
    learn_from_patterns: bool = True
    cache_strategies: bool = True
    optimize_for_document_type: bool = True
    
    model_config = ConfigDict(
        env_prefix="PDF_EXTRACTOR_",
        case_sensitive=False
    )


# Sample generation models for agent coordination
class ExtractionSamples(BaseModel):
    """Samples generated for agent assessment"""
    metadata: Dict[str, Any]
    extraction_samples: Dict[str, Any]
    extraction_warnings: List[str]
    performance_metrics: Dict[str, Any]


class AssessmentResult(BaseModel):
    """Result from extraction-assessor agent"""
    overall_assessment: Dict[str, Any]
    area_assessments: Dict[str, Any]
    enhancement_recommendations: List[Dict[str, Any]]
    processing_decision: Dict[str, Any]
    
    @property
    def needs_enhancement(self) -> bool:
        return self.processing_decision.get("proceed_with_enhancements", False)


class EnhancementHints(BaseModel):
    """Enhancement hints from agents"""
    agent_type: str
    enhancement_data: Dict[str, Any]
    confidence_boost_potential: float
    processing_notes: List[str] = Field(default_factory=list)