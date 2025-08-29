"""
PDF analysis for document characteristics and strategy selection
"""

import re
from typing import Dict, List, Any
from collections import Counter

from ..models import PDFProfile, ExtractionConfig
from ..utils import logger


class PDFAnalyzer:
    """
    Analyze PDF characteristics for optimal extraction strategy
    """
    
    def __init__(self, config: ExtractionConfig):
        self.config = config
        self.logger = logger.bind(component="PDFAnalyzer")
        
        # Document type indicators
        self.document_indicators = {
            'academic': [
                'abstract', 'methodology', 'references', 'bibliography',
                'figure', 'table', 'et al.', 'doi:', 'isbn', 'journal',
                'research', 'study', 'analysis', 'hypothesis', 'conclusion'
            ],
            'business': [
                'executive summary', 'roi', 'kpi', 'strategy', 'market',
                'revenue', 'customer', 'competitive', 'analysis', 'profit',
                'business', 'company', 'industry', 'sales', 'management'
            ],
            'technical': [
                'algorithm', 'implementation', 'code', 'api', 'framework',
                'architecture', 'system', 'performance', 'optimization',
                'software', 'programming', 'development', 'technical', 'function'
            ],
            'biography': [
                'born', 'early life', 'childhood', 'education', 'career',
                'achievements', 'personal', 'family', 'death', 'legacy'
            ],
            'self_help': [
                'how to', 'self improvement', 'personal development', 'success',
                'motivation', 'habits', 'goals', 'mindset', 'change your life'
            ]
        }
    
    async def analyze_pdf_characteristics(self, pdf_doc) -> PDFProfile:
        """
        Comprehensive PDF analysis for strategy selection
        """
        self.logger.debug("Starting comprehensive PDF analysis")
        
        # Sample first few pages for analysis
        sample_text = await self._extract_sample_text(pdf_doc)
        
        # Document type classification
        document_type = self._classify_document_type(sample_text)
        
        # Structure complexity analysis
        structure_complexity = await self._analyze_structure_complexity(pdf_doc)
        
        # Text quality assessment
        text_quality = await self._assess_text_quality(pdf_doc, sample_text)
        
        # Layout pattern detection
        layout_type = await self._detect_layout_pattern(pdf_doc)
        
        # TOC detection
        has_toc = await self._detect_table_of_contents(pdf_doc, sample_text)
        
        # Chapter pattern recognition
        chapter_pattern = self._detect_chapter_pattern(sample_text)
        
        # Citation style detection
        citation_style = self._detect_citation_style(sample_text)
        
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
            "PDF analysis complete",
            document_type=document_type,
            complexity=structure_complexity,
            text_quality=text_quality,
            layout=layout_type
        )
        
        return profile
    
    async def _extract_sample_text(self, pdf_doc, max_pages: int = 10) -> str:
        """Extract sample text from first few pages"""
        sample_text = ""
        
        try:
            pages = list(pdf_doc.pages)[:max_pages]
            for page in pages:
                page_text = page.extract_text() if hasattr(page, 'extract_text') else ""
                if page_text:
                    sample_text += page_text + "\n"
        except Exception as e:
            self.logger.warning("Failed to extract sample text", error=str(e))
        
        return sample_text
    
    def _classify_document_type(self, sample_text: str) -> str:
        """
        Classify document type based on content analysis
        """
        text_lower = sample_text.lower()
        
        # Count indicator matches for each type
        type_scores = {}
        
        for doc_type, indicators in self.document_indicators.items():
            score = sum(1 for indicator in indicators if indicator in text_lower)
            # Weight by indicator strength
            weighted_score = score / len(indicators) if indicators else 0
            type_scores[doc_type] = weighted_score
        
        # Return type with highest score, or 'other' if no clear match
        if type_scores:
            best_type = max(type_scores.keys(), key=lambda k: type_scores[k])
            if type_scores[best_type] > 0.1:  # Minimum threshold
                return best_type
        
        return 'other'
    
    async def _analyze_structure_complexity(self, pdf_doc) -> float:
        """
        Analyze document structure complexity (0.0 - 1.0)
        """
        complexity_score = 0.0
        
        try:
            pages = list(pdf_doc.pages)
            
            # Factors contributing to complexity:
            # 1. Number of different font sizes used
            font_sizes = set()
            # 2. Presence of multi-column layouts
            multi_column_pages = 0
            # 3. Number of images/figures
            total_images = 0
            # 4. Presence of tables
            total_tables = 0
            
            for page in pages[:5]:  # Sample first 5 pages
                try:
                    # Font diversity
                    if hasattr(page, 'chars'):
                        chars = page.chars or []
                        page_font_sizes = {char.get('size', 12) for char in chars}
                        font_sizes.update(page_font_sizes)
                    
                    # Image count
                    if hasattr(page, 'images'):
                        total_images += len(page.images or [])
                    
                    # Multi-column detection (simplified)
                    if hasattr(page, 'extract_text'):
                        text = page.extract_text() or ""
                        # Very basic multi-column detection
                        if self._detect_multi_column(text):
                            multi_column_pages += 1
                
                except Exception as e:
                    self.logger.debug(f"Error analyzing page complexity: {e}")
                    continue
            
            # Calculate complexity score
            font_diversity = len(font_sizes) / 10.0  # Normalize to 0-1
            layout_complexity = multi_column_pages / max(1, len(pages[:5]))
            visual_complexity = min(1.0, (total_images + total_tables) / 20.0)
            
            complexity_score = min(1.0, (font_diversity + layout_complexity + visual_complexity) / 3.0)
        
        except Exception as e:
            self.logger.warning("Failed to analyze structure complexity", error=str(e))
            complexity_score = 0.5  # Default middle value
        
        return complexity_score
    
    async def _assess_text_quality(self, pdf_doc, sample_text: str) -> float:
        """
        Assess text extraction quality (0.0 - 1.0)
        """
        if not sample_text:
            return 0.0
        
        quality_score = 1.0
        
        # Check for common OCR/extraction issues
        issues = []
        
        # 1. Excessive whitespace or formatting artifacts
        if sample_text.count('\n\n\n') > len(sample_text) / 1000:
            issues.append("excessive_whitespace")
            quality_score -= 0.1
        
        # 2. Broken words (common in OCR)
        words = sample_text.split()
        if words:
            broken_words = sum(1 for word in words if len(word) == 1 and word.isalpha())
            if broken_words / len(words) > 0.05:  # More than 5% single-letter words
                issues.append("broken_words")
                quality_score -= 0.2
        
        # 3. Garbled characters
        garbled_chars = sum(1 for char in sample_text if not char.isprintable() and char not in '\n\t\r')
        if garbled_chars > len(sample_text) / 1000:
            issues.append("garbled_characters")
            quality_score -= 0.15
        
        # 4. Missing spaces (words run together)
        run_together = len(re.findall(r'[a-z][A-Z]', sample_text))
        if run_together > len(sample_text) / 500:
            issues.append("missing_spaces")
            quality_score -= 0.1
        
        # 5. Readable text ratio
        readable_chars = sum(1 for char in sample_text if char.isalnum() or char.isspace())
        readable_ratio = readable_chars / len(sample_text) if sample_text else 0
        if readable_ratio < 0.8:
            issues.append("low_readable_ratio")
            quality_score -= 0.2
        
        if issues:
            self.logger.debug("Text quality issues detected", issues=issues)
        
        return max(0.0, quality_score)
    
    async def _detect_layout_pattern(self, pdf_doc) -> str:
        """
        Detect document layout type
        """
        try:
            # Sample a few pages to determine layout
            pages = list(pdf_doc.pages)[:3]
            
            multi_column_count = 0
            
            for page in pages:
                if self._is_multi_column_page(page):
                    multi_column_count += 1
            
            # Determine layout type
            if multi_column_count >= len(pages) / 2:
                return "multi_column"
            elif multi_column_count > 0:
                return "mixed"
            else:
                return "single_column"
        
        except Exception as e:
            self.logger.debug("Layout detection failed", error=str(e))
            return "single_column"
    
    def _is_multi_column_page(self, page) -> bool:
        """
        Detect if a page has multi-column layout
        """
        try:
            if not hasattr(page, 'chars'):
                return False
            
            chars = page.chars or []
            if not chars:
                return False
            
            # Get x-coordinates of text
            x_positions = [char.get('x0', 0) for char in chars if char.get('text', '').strip()]
            
            if len(x_positions) < 50:  # Not enough text to determine
                return False
            
            # Look for clustering in x-positions (indicates columns)
            x_positions.sort()
            
            # Simple clustering: look for gaps in x-positions
            gaps = []
            for i in range(1, len(x_positions)):
                gap = x_positions[i] - x_positions[i-1]
                gaps.append(gap)
            
            # If there are significant gaps, likely multi-column
            avg_gap = sum(gaps) / len(gaps)
            large_gaps = [g for g in gaps if g > avg_gap * 5]
            
            return len(large_gaps) > 0
        
        except Exception:
            return False
    
    async def _detect_table_of_contents(self, pdf_doc, sample_text: str) -> bool:
        """
        Detect presence of table of contents
        """
        toc_indicators = [
            'table of contents', 'contents', 'index',
            'chapter 1', 'chapter i', '1.', 'i.'
        ]
        
        text_lower = sample_text.lower()
        
        # Check for TOC indicators
        has_indicators = any(indicator in text_lower for indicator in toc_indicators)
        
        # Check for page number patterns (common in TOC)
        page_patterns = re.findall(r'\.\s*\d+\s*$', sample_text, re.MULTILINE)
        has_page_numbers = len(page_patterns) > 3
        
        return has_indicators and has_page_numbers
    
    def _detect_chapter_pattern(self, sample_text: str) -> str:
        """
        Detect chapter numbering pattern
        """
        # Look for chapter patterns
        chapter_patterns = {
            'numbered': [r'chapter\s+\d+', r'^\d+\.', r'^\d+\s+[A-Z]'],
            'named': [r'chapter\s+[a-z]+', r'^[A-Z\s]+$'],
            'roman': [r'chapter\s+[ivx]+', r'^[IVX]+\.'],
        }
        
        text_lower = sample_text.lower()
        
        pattern_scores = {}
        for pattern_type, patterns in chapter_patterns.items():
            score = sum(len(re.findall(pattern, text_lower, re.MULTILINE)) for pattern in patterns)
            pattern_scores[pattern_type] = score
        
        if pattern_scores:
            dominant_pattern = max(pattern_scores.keys(), key=lambda k: pattern_scores[k])
            if pattern_scores[dominant_pattern] > 0:
                return dominant_pattern
        
        return 'mixed'
    
    def _detect_citation_style(self, sample_text: str) -> str:
        """
        Detect citation style used in document
        """
        citation_patterns = {
            'apa': [r'\([A-Z][a-z]+,\s+\d{4}\)', r'\([A-Z][a-z]+\s+&\s+[A-Z][a-z]+,\s+\d{4}\)'],
            'mla': [r'\([A-Z][a-z]+\s+\d+\)', r'[A-Z][a-z]+,\s+"[^"]+"\s+\d+'],
            'ieee': [r'\[\d+\]', r'\[\d+\-\d+\]'],
            'chicago': [r'[A-Z][a-z]+,\s+[^,]+,\s+\d+']
        }
        
        style_scores = {}
        for style, patterns in citation_patterns.items():
            score = sum(len(re.findall(pattern, sample_text)) for pattern in patterns)
            style_scores[style] = score
        
        if style_scores:
            dominant_style = max(style_scores.keys(), key=lambda k: style_scores[k])
            if style_scores[dominant_style] > 2:  # Minimum citations to determine style
                return dominant_style
        
        return 'mixed' if any(score > 0 for score in style_scores.values()) else 'none'
    
    async def _calculate_image_density(self, pdf_doc) -> float:
        """
        Calculate images per page ratio
        """
        try:
            pages = list(pdf_doc.pages)
            total_images = 0
            
            for page in pages[:5]:  # Sample first 5 pages
                if hasattr(page, 'images'):
                    total_images += len(page.images or [])
            
            return total_images / max(1, len(pages[:5]))
        
        except Exception:
            return 0.0
    
    async def _calculate_table_density(self, pdf_doc) -> float:
        """
        Calculate tables per page ratio
        """
        try:
            pages = list(pdf_doc.pages)
            total_tables = 0
            
            for page in pages[:5]:  # Sample first 5 pages
                if hasattr(page, 'extract_tables'):
                    tables = page.extract_tables()
                    if tables:
                        total_tables += len(tables)
            
            return total_tables / max(1, len(pages[:5]))
        
        except Exception:
            return 0.0
    
    async def _analyze_font_consistency(self, pdf_doc) -> float:
        """
        Analyze font usage consistency (0.0 - 1.0)
        """
        try:
            pages = list(pdf_doc.pages)
            all_fonts = []
            
            for page in pages[:5]:  # Sample first 5 pages
                if hasattr(page, 'chars'):
                    chars = page.chars or []
                    page_fonts = [(char.get('fontname', ''), char.get('size', 12)) for char in chars]
                    all_fonts.extend(page_fonts)
            
            if not all_fonts:
                return 0.5
            
            # Calculate font diversity
            unique_fonts = set(all_fonts)
            font_consistency = 1.0 - min(1.0, len(unique_fonts) / 20.0)  # Normalize
            
            return font_consistency
        
        except Exception:
            return 0.5
    
    def _detect_multi_column(self, text: str) -> bool:
        """
        Simple multi-column detection based on text patterns
        """
        lines = text.split('\n')
        
        # Look for lines that seem to be split across columns
        split_lines = 0
        for line in lines:
            line = line.strip()
            if len(line) > 10 and len(line) < 40:  # Suspiciously short lines
                # Check if line ends abruptly (no punctuation)
                if line and line[-1].isalnum():
                    split_lines += 1
        
        return split_lines > len(lines) / 10  # More than 10% split lines