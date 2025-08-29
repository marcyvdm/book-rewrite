"""
Main PDF extraction class with multi-algorithm intelligence
"""

import asyncio
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

from ..models import (
    ExtractionResult,
    BookContent,
    BookMetadata,
    ProcessingReport,
    QualityMetrics,
    PDFProfile,
    ExtractionConfig,
    DocumentType,
    SourceFormat,
)
from ..engines import PDFEngineFactory
from ..analyzers import (
    PDFAnalyzer,
    ChapterDetectionEngine,
    ParagraphProcessor,
    ImageProcessor,
    CitationProcessor,
)
from ..processors import QualityAssessmentEngine
from ..utils import logger


class IntelligentPDFExtractor:
    """
    Main PDF extraction class with multi-algorithm consensus and adaptive intelligence
    """
    
    def __init__(self, config: ExtractionConfig):
        self.config = config
        self.logger = logger.bind(component="PDFExtractor")
        
        # Initialize components
        self.engine_factory = PDFEngineFactory(config)
        self.pdf_analyzer = PDFAnalyzer(config)
        self.chapter_detector = ChapterDetectionEngine(config)
        self.paragraph_processor = ParagraphProcessor(config)
        self.image_processor = ImageProcessor(config)
        self.citation_processor = CitationProcessor(config)
        self.quality_engine = QualityAssessmentEngine(config)
        
        # Processing state
        self.current_pdf_path: Optional[Path] = None
        self.pdf_profile: Optional[PDFProfile] = None
        self.processing_start_time: Optional[float] = None
    
    async def extract(self, pdf_path: Union[str, Path]) -> ExtractionResult:
        """
        Main extraction method with full intelligence pipeline
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Complete extraction result with quality metrics
        """
        pdf_path = Path(pdf_path)
        self.current_pdf_path = pdf_path
        self.processing_start_time = time.time()
        
        self.logger.info(
            "Starting intelligent PDF extraction",
            pdf_path=str(pdf_path),
            file_size_mb=round(pdf_path.stat().st_size / (1024 * 1024), 2)
        )
        
        try:
            # Phase 1: PDF Analysis & Strategy Selection
            self.logger.info("Phase 1: Analyzing PDF characteristics")
            self.pdf_profile = await self._analyze_pdf_characteristics(pdf_path)
            
            # Phase 2: Multi-Engine Extraction
            self.logger.info("Phase 2: Multi-engine extraction", strategy=self.pdf_profile.document_type)
            raw_extraction_data = await self._extract_with_optimal_strategy(pdf_path)
            
            # Phase 3: Intelligent Structure Detection
            self.logger.info("Phase 3: Intelligent structure detection")
            structured_content = await self._apply_intelligent_structuring(raw_extraction_data)
            
            # Phase 4: Quality Enhancement & Validation
            self.logger.info("Phase 4: Quality enhancement and validation")
            enhanced_content = await self._enhance_and_validate(structured_content)
            
            # Phase 5: Final Result Assembly
            self.logger.info("Phase 5: Final result assembly")
            final_result = await self._assemble_final_result(enhanced_content)
            
            processing_time = time.time() - self.processing_start_time
            self.logger.info(
                "PDF extraction completed successfully",
                processing_time_s=round(processing_time, 2),
                overall_confidence=final_result.overall_confidence,
                chapters_found=len(final_result.book_content.chapters),
                paragraphs_found=len(final_result.book_content.paragraphs),
                images_found=len(final_result.book_content.images)
            )
            
            return final_result
            
        except Exception as e:
            processing_time = time.time() - (self.processing_start_time or time.time())
            self.logger.error(
                "PDF extraction failed",
                error=str(e),
                processing_time_s=round(processing_time, 2),
                exc_info=True
            )
            raise
    
    async def _analyze_pdf_characteristics(self, pdf_path: Path) -> PDFProfile:
        """
        Comprehensive PDF analysis for optimal extraction strategy
        """
        self.logger.debug("Analyzing PDF characteristics for strategy selection")
        
        # Use primary engine for analysis
        engine = self.engine_factory.get_primary_engine()
        
        try:
            with engine.open_pdf(pdf_path) as pdf_doc:
                # Document structure analysis
                structure_complexity = await self._analyze_document_structure(pdf_doc)
                
                # Text quality assessment
                text_quality = await self._assess_text_quality(pdf_doc)
                
                # Layout pattern detection
                layout_type = await self._detect_layout_pattern(pdf_doc)
                
                # Content type classification
                document_type = await self._classify_document_type(pdf_doc)
                
                # TOC detection
                has_toc = await self._detect_table_of_contents(pdf_doc)
                
                # Chapter pattern recognition
                chapter_pattern = await self._detect_chapter_pattern(pdf_doc)
                
                # Citation style detection
                citation_style = await self._detect_citation_style(pdf_doc)
                
                # Density calculations
                image_density = await self._calculate_image_density(pdf_doc)
                table_density = await self._calculate_table_density(pdf_doc)
                font_consistency = await self._analyze_font_consistency(pdf_doc)
                
                profile = PDFProfile(
                    document_type=document_type,
                    structure_complexity=structure_complexity,
                    text_quality=text_quality,
                    layout_type=layout_type,
                    has_toc=has_toc,
                    chapter_pattern=chapter_pattern,
                    citation_style=citation_style,
                    image_density=image_density,
                    table_density=table_density,
                    font_consistency=font_consistency
                )
                
                self.logger.info(
                    "PDF profile analysis complete",
                    document_type=document_type,
                    layout_type=layout_type,
                    has_toc=has_toc,
                    structure_complexity=structure_complexity,
                    text_quality=text_quality
                )
                
                return profile
                
        except Exception as e:
            self.logger.error("Failed to analyze PDF characteristics", error=str(e))
            # Return default profile on failure
            return PDFProfile(
                document_type="other",
                structure_complexity=0.5,
                text_quality=0.7,
                layout_type="single_column",
                has_toc=False,
                chapter_pattern="mixed",
                citation_style="none",
                image_density=0.0,
                table_density=0.0,
                font_consistency=0.5
            )
    
    async def _extract_with_optimal_strategy(self, pdf_path: Path) -> Dict[str, Any]:
        """
        Extract PDF content using optimal strategy based on profile
        """
        strategy = self._select_extraction_strategy()
        self.logger.debug("Selected extraction strategy", strategy=strategy)
        
        # Try primary engine first
        try:
            engine = self.engine_factory.get_engine(self.config.primary_engine)
            raw_data = await self._extract_with_engine(pdf_path, engine, strategy)
            
            self.logger.debug("Primary engine extraction successful")
            return raw_data
            
        except Exception as e:
            self.logger.warning(
                "Primary engine failed, trying fallback",
                primary_engine=self.config.primary_engine,
                error=str(e)
            )
            
            # Try fallback engines
            for fallback_engine_name in self.config.fallback_engines:
                try:
                    engine = self.engine_factory.get_engine(fallback_engine_name)
                    raw_data = await self._extract_with_engine(pdf_path, engine, strategy)
                    
                    self.logger.info(
                        "Fallback engine extraction successful",
                        engine=fallback_engine_name
                    )
                    return raw_data
                    
                except Exception as fallback_error:
                    self.logger.warning(
                        "Fallback engine failed",
                        engine=fallback_engine_name,
                        error=str(fallback_error)
                    )
                    continue
            
            # If all engines fail, raise the original error
            raise Exception(f"All extraction engines failed. Last error: {e}")
    
    def _select_extraction_strategy(self) -> str:
        """
        Select optimal extraction strategy based on PDF profile
        """
        if not self.pdf_profile:
            return "default"
        
        # Strategy selection logic based on document characteristics
        if self.pdf_profile.document_type == "academic":
            if self.pdf_profile.structure_complexity > 0.7:
                return "academic_complex"
            else:
                return "academic_standard"
        
        elif self.pdf_profile.document_type == "business":
            if self.pdf_profile.image_density > 0.1:
                return "business_visual"
            else:
                return "business_text_heavy"
        
        elif self.pdf_profile.document_type == "technical":
            return "technical_detailed"
        
        else:
            if self.pdf_profile.structure_complexity > 0.6:
                return "complex_document"
            else:
                return "standard_document"
    
    async def _extract_with_engine(self, pdf_path: Path, engine, strategy: str) -> Dict[str, Any]:
        """
        Extract content using specific engine and strategy
        """
        with engine.open_pdf(pdf_path) as pdf_doc:
            # Extract basic content
            pages = list(pdf_doc.pages)
            
            # Extract text content
            text_blocks = []
            for page_num, page in enumerate(pages):
                page_text_blocks = engine.extract_text_blocks(page)
                for block in page_text_blocks:
                    block['page_number'] = page_num + 1
                text_blocks.extend(page_text_blocks)
            
            # Extract images
            images = []
            for page_num, page in enumerate(pages):
                page_images = engine.extract_images(page)
                for img in page_images:
                    img['page_number'] = page_num + 1
                images.extend(page_images)
            
            # Extract table of contents
            toc_entries = engine.extract_table_of_contents(pdf_doc)
            
            # Extract metadata
            pdf_metadata = engine.extract_metadata(pdf_doc)
            
            return {
                'pages': pages,
                'text_blocks': text_blocks,
                'images': images,
                'toc_entries': toc_entries,
                'metadata': pdf_metadata,
                'page_count': len(pages),
                'extraction_strategy': strategy
            }
    
    async def _apply_intelligent_structuring(self, raw_data: Dict[str, Any]) -> BookContent:
        """
        Apply intelligent structure detection algorithms
        """
        self.logger.debug("Applying intelligent structure detection")
        
        # Generate unique IDs
        book_id = str(uuid.uuid4())
        
        # Extract and structure chapters
        chapters = await self.chapter_detector.detect_chapters_intelligently(
            raw_data['text_blocks'], 
            raw_data.get('toc_entries', [])
        )
        
        # Process paragraphs with classification
        paragraphs = await self.paragraph_processor.extract_paragraphs_with_classification(
            raw_data['text_blocks']
        )
        
        # Assign paragraphs to chapters
        paragraphs = self._assign_paragraphs_to_chapters(paragraphs, chapters)
        
        # Process images with intelligent context analysis
        images = await self.image_processor.process_images_with_intelligence(
            raw_data['images'],
            paragraphs,
            chapters
        )
        
        # Process citations
        citations = await self.citation_processor.detect_citations_intelligently(
            raw_data['text_blocks']
        )
        
        # Generate metadata
        metadata = self._generate_book_metadata(raw_data, book_id)
        
        # Build table of contents structure
        toc_entries = self._build_structured_toc(raw_data.get('toc_entries', []), chapters)
        
        return BookContent(
            metadata=metadata,
            chapters=chapters,
            sections=[],  # Will be populated by section detection
            paragraphs=paragraphs,
            images=images,
            table_of_contents=toc_entries,
            citations=citations
        )
    
    async def _enhance_and_validate(self, content: BookContent) -> BookContent:
        """
        Apply quality enhancement and validation
        """
        self.logger.debug("Applying quality enhancement and validation")
        
        # Run quality assessment
        quality_report = await self.quality_engine.calculate_final_quality_metrics(content)
        
        # Apply self-corrections if needed
        if quality_report.overall_confidence < self.config.min_overall_confidence:
            if self.config.enable_self_correction:
                self.logger.info(
                    "Applying self-corrections",
                    current_confidence=quality_report.overall_confidence,
                    target_confidence=self.config.min_overall_confidence
                )
                content = await self._apply_self_corrections(content, quality_report)
        
        return content
    
    async def _assemble_final_result(self, content: BookContent) -> ExtractionResult:
        """
        Assemble final extraction result with complete metadata
        """
        processing_time = int((time.time() - self.processing_start_time) * 1000)
        
        # Generate final quality metrics
        quality_metrics = await self.quality_engine.calculate_final_quality_metrics(content)
        
        # Build processing report
        processing_report = ProcessingReport(
            total_processing_time_ms=processing_time,
            pdf_profile=self.pdf_profile,
            extraction_strategy=getattr(self, '_extraction_strategy', 'default'),
            quality_metrics=quality_metrics,
            errors=[],  # Will be populated by error tracking
            warnings=[],  # Will be populated by warning tracking
            performance_stats={
                'memory_usage_mb': self._get_memory_usage(),
                'processing_phases': {
                    'analysis': 0,  # Will be tracked in production
                    'extraction': 0,
                    'structuring': 0,
                    'validation': 0
                }
            },
            agent_enhancements_used=[]  # Will be populated by agent coordination
        )
        
        return ExtractionResult(
            id=content.metadata.id,
            pdf_path=str(self.current_pdf_path),
            processing_timestamp=datetime.now(),
            book_content=content,
            processing_report=processing_report
        )
    
    def _assign_paragraphs_to_chapters(self, paragraphs: List, chapters: List) -> List:
        """
        Intelligently assign paragraphs to chapters based on page numbers and content
        """
        # Simple assignment based on page numbers
        # In production, this would be more sophisticated
        for paragraph in paragraphs:
            # Find the chapter this paragraph belongs to
            assigned_chapter = None
            for chapter in chapters:
                if paragraph.page_number >= chapter.page_number:
                    if not assigned_chapter or chapter.page_number > assigned_chapter.page_number:
                        assigned_chapter = chapter
            
            if assigned_chapter:
                paragraph.chapter_id = assigned_chapter.id
                if paragraph.id not in assigned_chapter.paragraph_ids:
                    assigned_chapter.paragraph_ids.append(paragraph.id)
        
        return paragraphs
    
    def _generate_book_metadata(self, raw_data: Dict[str, Any], book_id: str) -> BookMetadata:
        """
        Generate book metadata from raw extraction data
        """
        pdf_metadata = raw_data.get('metadata', {})
        
        # Extract title and author from metadata or first page
        title = pdf_metadata.get('Title', 'Extracted Document')
        author = pdf_metadata.get('Author', 'Unknown Author')
        
        # Calculate word count
        total_word_count = sum(
            len(block.get('text', '').split()) 
            for block in raw_data.get('text_blocks', [])
        )
        
        # Estimate reading time (average 200 words per minute)
        reading_time = max(1, total_word_count // 200)
        
        return BookMetadata(
            id=book_id,
            title=title,
            author=author,
            genre="Unknown",
            category=DocumentType(self.pdf_profile.document_type if self.pdf_profile else "other"),
            language="en",
            page_count=raw_data.get('page_count', 0),
            word_count=total_word_count,
            reading_level=8.0,  # Will be calculated by text analysis
            source_format=SourceFormat.PDF,
            processing_date=datetime.now().isoformat(),
            processing_version="1.0.0",
            estimated_reading_time_minutes=reading_time,
            tags=[]
        )
    
    def _build_structured_toc(self, toc_entries: List, chapters: List):
        """
        Build structured table of contents
        """
        # Convert raw TOC entries to structured format
        # This is a simplified implementation
        structured_toc = []
        
        for i, entry in enumerate(toc_entries):
            structured_entry = {
                'id': f"toc_{i}",
                'title': entry.get('title', f'Chapter {i+1}'),
                'level': entry.get('level', 1),
                'page_number': entry.get('page', 1),
                'chapter_id': None,  # Will be matched to actual chapters
                'children': []
            }
            structured_toc.append(structured_entry)
        
        return structured_toc
    
    async def _apply_self_corrections(self, content: BookContent, quality_report) -> BookContent:
        """
        Apply self-corrections based on quality assessment
        """
        # Placeholder for self-correction logic
        # In production, this would attempt to fix identified issues
        self.logger.debug("Self-correction not implemented yet, returning original content")
        return content
    
    def _get_memory_usage(self) -> float:
        """
        Get current memory usage in MB
        """
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss / (1024 * 1024)
        except ImportError:
            return 0.0
    
    # Placeholder methods for PDF analysis - will be implemented in analyzers
    async def _analyze_document_structure(self, pdf_doc) -> float:
        return 0.5
    
    async def _assess_text_quality(self, pdf_doc) -> float:
        return 0.8
    
    async def _detect_layout_pattern(self, pdf_doc) -> str:
        return "single_column"
    
    async def _classify_document_type(self, pdf_doc) -> str:
        return "business"
    
    async def _detect_table_of_contents(self, pdf_doc) -> bool:
        return True
    
    async def _detect_chapter_pattern(self, pdf_doc) -> str:
        return "numbered"
    
    async def _detect_citation_style(self, pdf_doc) -> str:
        return "mixed"
    
    async def _calculate_image_density(self, pdf_doc) -> float:
        return 0.05
    
    async def _calculate_table_density(self, pdf_doc) -> float:
        return 0.02
    
    async def _analyze_font_consistency(self, pdf_doc) -> float:
        return 0.7