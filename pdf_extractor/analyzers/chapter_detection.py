"""
Intelligent chapter detection with multi-algorithm consensus
"""

import re
import uuid
from typing import List, Dict, Any, Optional, Tuple
from collections import defaultdict, Counter

from ..models import Chapter, TableOfContentsEntry, ExtractionConfig
from ..utils import logger


class ChapterDetectionEngine:
    """
    Multi-algorithm chapter detection with consensus building
    """
    
    def __init__(self, config: ExtractionConfig):
        self.config = config
        self.logger = logger.bind(component="ChapterDetection")
        
        # Chapter patterns for different document types
        self.patterns = ChapterPatterns()
        self.font_analyzer = FontAnalyzer()
        self.context_analyzer = ContextAnalyzer()
    
    async def detect_chapters_intelligently(
        self, 
        text_blocks: List[Dict[str, Any]], 
        toc_entries: List[Dict[str, Any]]
    ) -> List[Chapter]:
        """
        Multi-algorithm chapter detection with validation and consensus
        """
        self.logger.info(
            "Starting intelligent chapter detection",
            text_blocks=len(text_blocks),
            toc_entries=len(toc_entries)
        )
        
        # Algorithm 1: TOC-based detection (highest confidence)
        toc_chapters = self._extract_from_toc(toc_entries) if toc_entries else []
        self.logger.debug("TOC-based detection complete", chapters=len(toc_chapters))
        
        # Algorithm 2: Font-based detection
        font_chapters = self._detect_by_font_analysis(text_blocks)
        self.logger.debug("Font-based detection complete", chapters=len(font_chapters))
        
        # Algorithm 3: Pattern-based detection
        pattern_chapters = self._detect_by_patterns(text_blocks)
        self.logger.debug("Pattern-based detection complete", chapters=len(pattern_chapters))
        
        # Algorithm 4: Structural break detection
        break_chapters = self._detect_by_structural_breaks(text_blocks)
        self.logger.debug("Structural break detection complete", chapters=len(break_chapters))
        
        # Algorithm 5: Context-based detection
        context_chapters = self._detect_by_context_analysis(text_blocks)
        self.logger.debug("Context-based detection complete", chapters=len(context_chapters))
        
        # Build consensus from all algorithms
        consensus_chapters = self._build_consensus([
            ('toc', toc_chapters, 1.0),
            ('font', font_chapters, 0.8),
            ('pattern', pattern_chapters, 0.9),
            ('break', break_chapters, 0.6),
            ('context', context_chapters, 0.7)
        ])
        
        self.logger.debug("Consensus building complete", chapters=len(consensus_chapters))
        
        # Validate and refine results
        validated_chapters = self._validate_and_refine(consensus_chapters, text_blocks)
        
        self.logger.info(
            "Chapter detection complete",
            final_chapters=len(validated_chapters),
            avg_confidence=sum(ch.confidence for ch in validated_chapters) / max(1, len(validated_chapters))
        )
        
        return validated_chapters
    
    def _extract_from_toc(self, toc_entries: List[Dict[str, Any]]) -> List[Chapter]:
        """
        Extract chapters from table of contents (most reliable method)
        """
        chapters = []
        
        for entry in toc_entries:
            if entry.get('level', 1) == 1:  # Only top-level entries are chapters
                chapter_id = str(uuid.uuid4())
                
                chapter = Chapter(
                    id=chapter_id,
                    number=len(chapters) + 1,
                    title=entry.get('title', f'Chapter {len(chapters) + 1}'),
                    summary="",
                    word_count=0,  # Will be calculated later
                    page_number=entry.get('page', 1),
                    confidence=0.95  # High confidence for TOC-based detection
                )
                
                chapters.append(chapter)
        
        return chapters
    
    def _detect_by_font_analysis(self, text_blocks: List[Dict[str, Any]]) -> List[Chapter]:
        """
        Detect chapters by analyzing font size, weight, and consistency
        """
        chapters = []
        potential_headings = []
        
        # Analyze font patterns across all text blocks
        font_stats = self.font_analyzer.analyze_font_statistics(text_blocks)
        heading_criteria = self.font_analyzer.determine_heading_criteria(font_stats)
        
        for block in text_blocks:
            font_info = block.get('font_info', {})
            text = block.get('text', '').strip()
            
            if not text:
                continue
            
            # Check if this block matches heading criteria
            if self._is_likely_heading_font(font_info, heading_criteria):
                # Additional validation for chapter headings
                if self._is_chapter_heading_text(text):
                    potential_headings.append({
                        'text': text,
                        'page': block.get('page_number', 1),
                        'font_size': font_info.get('size', 12),
                        'font_name': font_info.get('name', ''),
                        'is_bold': font_info.get('bold', False),
                        'bbox': block.get('bbox', {}),
                        'confidence': self._calculate_font_confidence(font_info, heading_criteria)
                    })
        
        # Convert potential headings to chapters
        chapters = self._convert_headings_to_chapters(potential_headings, 'font')
        
        return chapters
    
    def _detect_by_patterns(self, text_blocks: List[Dict[str, Any]]) -> List[Chapter]:
        """
        Pattern-based chapter detection using regex and heuristics
        """
        chapters = []
        
        # Common chapter patterns with different priorities
        patterns = [
            (r'^Chapter\s+(\d+|[IVX]+)[\s\.:]\s*(.+)$', 1.0),
            (r'^CHAPTER\s+(\d+|[IVX]+)[\s\.:]\s*(.+)$', 1.0),
            (r'^(\d+)[\.\)\s]\s+(.+)$', 0.8),
            (r'^([IVX]+)[\.\)\s]\s+(.+)$', 0.7),
            (r'^Part\s+(\d+|[IVX]+)[\s\.:]\s*(.+)$', 0.9),
            (r'^Section\s+(\d+|[IVX]+)[\s\.:]\s*(.+)$', 0.6),
        ]
        
        for block in text_blocks:
            text = block.get('text', '').strip()
            if not text:
                continue
            
            # Check against each pattern
            for pattern, base_confidence in patterns:
                lines = text.split('\n')
                for line in lines:
                    line = line.strip()
                    match = re.match(pattern, line, re.IGNORECASE | re.MULTILINE)
                    
                    if match:
                        chapter_num = match.group(1) if match.groups() else str(len(chapters) + 1)
                        chapter_title = match.group(2) if len(match.groups()) > 1 else line
                        
                        # Validate chapter candidate
                        if self._validate_chapter_candidate(line, block):
                            chapter_id = str(uuid.uuid4())
                            
                            chapter = Chapter(
                                id=chapter_id,
                                number=self._normalize_chapter_number(chapter_num),
                                title=chapter_title.strip(),
                                summary="",
                                word_count=0,
                                page_number=block.get('page_number', 1),
                                confidence=base_confidence * self._calculate_pattern_confidence(pattern, line)
                            )
                            
                            chapters.append(chapter)
                        break
        
        # Remove duplicates and sort by page number
        chapters = self._deduplicate_and_sort_chapters(chapters)
        
        return chapters
    
    def _detect_by_structural_breaks(self, text_blocks: List[Dict[str, Any]]) -> List[Chapter]:
        """
        Detect chapters by analyzing structural breaks (page breaks, spacing, etc.)
        """
        chapters = []
        
        # Group text blocks by page
        pages = defaultdict(list)
        for block in text_blocks:
            page_num = block.get('page_number', 1)
            pages[page_num].append(block)
        
        # Analyze page breaks and content patterns
        for page_num in sorted(pages.keys()):
            page_blocks = pages[page_num]
            
            # Look for indicators of chapter starts
            first_block = page_blocks[0] if page_blocks else None
            if first_block:
                text = first_block.get('text', '').strip()
                
                # Check if page starts with potential chapter heading
                if self._looks_like_chapter_start(text, page_num, pages):
                    chapter_id = str(uuid.uuid4())
                    
                    # Extract title from first meaningful text
                    title = self._extract_title_from_text(text)
                    
                    chapter = Chapter(
                        id=chapter_id,
                        number=len(chapters) + 1,
                        title=title,
                        summary="",
                        word_count=0,
                        page_number=page_num,
                        confidence=0.6  # Moderate confidence for structural detection
                    )
                    
                    chapters.append(chapter)
        
        return chapters
    
    def _detect_by_context_analysis(self, text_blocks: List[Dict[str, Any]]) -> List[Chapter]:
        """
        Detect chapters by analyzing content context and topic shifts
        """
        chapters = []
        
        # Analyze content for topic boundaries
        topic_boundaries = self.context_analyzer.detect_topic_shifts(text_blocks)
        
        for boundary in topic_boundaries:
            if boundary['strength'] > 0.7:  # High confidence topic shift
                chapter_id = str(uuid.uuid4())
                
                chapter = Chapter(
                    id=chapter_id,
                    number=len(chapters) + 1,
                    title=boundary.get('suggested_title', f'Chapter {len(chapters) + 1}'),
                    summary="",
                    word_count=0,
                    page_number=boundary.get('page_number', 1),
                    confidence=boundary['strength']
                )
                
                chapters.append(chapter)
        
        return chapters
    
    def _build_consensus(self, algorithm_results: List[Tuple[str, List[Chapter], float]]) -> List[Chapter]:
        """
        Build consensus from multiple detection algorithms
        """
        all_chapters = []
        
        # Collect all detected chapters with their sources
        for algorithm_name, chapters, algorithm_weight in algorithm_results:
            for chapter in chapters:
                all_chapters.append({
                    'chapter': chapter,
                    'algorithm': algorithm_name,
                    'weight': algorithm_weight,
                    'weighted_confidence': chapter.confidence * algorithm_weight
                })
        
        if not all_chapters:
            return []
        
        # Group chapters by proximity (chapters within 2 pages of each other)
        chapter_groups = self._group_chapters_by_proximity(all_chapters, proximity=2)
        
        consensus_chapters = []
        
        for group in chapter_groups:
            # Find the best chapter in each group using weighted scoring
            best_chapter_data = max(group, key=lambda x: x['weighted_confidence'])
            best_chapter = best_chapter_data['chapter']
            
            # Enhance with information from other detections in the group
            enhanced_chapter = self._enhance_with_group_info(best_chapter, group)
            
            # Only include if confidence meets minimum threshold
            if enhanced_chapter.confidence >= self.config.min_chapter_confidence:
                consensus_chapters.append(enhanced_chapter)
        
        return consensus_chapters
    
    def _validate_and_refine(self, chapters: List[Chapter], text_blocks: List[Dict[str, Any]]) -> List[Chapter]:
        """
        Validate and refine final chapter list
        """
        if not chapters:
            return []
        
        # Sort by page number
        chapters.sort(key=lambda c: c.page_number)
        
        # Assign sequential numbers
        for i, chapter in enumerate(chapters):
            chapter.number = i + 1
        
        # Calculate word counts by assigning text blocks to chapters
        for chapter in chapters:
            chapter.word_count = self._calculate_chapter_word_count(chapter, text_blocks)
        
        # Remove chapters that are too short (likely false positives)
        min_words = 100  # Minimum words for a valid chapter
        validated_chapters = [ch for ch in chapters if ch.word_count >= min_words]
        
        # Final confidence adjustment based on chapter lengths and distribution
        self._adjust_final_confidences(validated_chapters)
        
        return validated_chapters
    
    # Helper methods
    def _is_likely_heading_font(self, font_info: Dict, criteria: Dict) -> bool:
        """Check if font matches heading criteria"""
        font_size = font_info.get('size', 12)
        is_bold = font_info.get('bold', False)
        
        return (
            font_size >= criteria.get('min_heading_size', 14) or
            (is_bold and font_size >= criteria.get('min_bold_heading_size', 12))
        )
    
    def _is_chapter_heading_text(self, text: str) -> bool:
        """Check if text looks like a chapter heading"""
        text = text.strip()
        
        # Too long to be a heading
        if len(text.split()) > 20:
            return False
        
        # Ends with period (unlikely for heading)
        if text.endswith('.') and not text.endswith('...'):
            return False
        
        # Contains chapter keywords
        chapter_keywords = ['chapter', 'section', 'part', 'introduction', 'conclusion']
        if any(keyword in text.lower() for keyword in chapter_keywords):
            return True
        
        # Numeric patterns
        if re.match(r'^\d+[\.\)\s]', text):
            return True
        
        # Roman numerals
        if re.match(r'^[IVX]+[\.\)\s]', text):
            return True
        
        # All caps (might be chapter title)
        if text.isupper() and len(text) > 3:
            return True
        
        return False
    
    def _validate_chapter_candidate(self, text: str, block: Dict) -> bool:
        """Validate if a text block is likely a chapter"""
        # Check text length
        if len(text.split()) > 25:  # Too long for heading
            return False
        
        # Check positioning (chapters often start near top of page)
        bbox = block.get('bbox', {})
        if bbox:
            # If we have positioning info, prefer headings near top of page
            y_position = bbox.get('y0', 0)
            page_height = 800  # Approximate page height
            relative_position = y_position / page_height if page_height > 0 else 0.5
            
            # Prefer headings in top 30% of page
            if relative_position > 0.7:
                return False
        
        return True
    
    def _normalize_chapter_number(self, chapter_num: str) -> int:
        """Convert chapter number to integer"""
        try:
            return int(chapter_num)
        except ValueError:
            # Handle roman numerals
            roman_map = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10}
            return roman_map.get(chapter_num.upper(), 1)
    
    def _calculate_pattern_confidence(self, pattern: str, text: str) -> float:
        """Calculate confidence based on pattern match quality"""
        confidence = 0.8  # Base confidence
        
        # Boost confidence for explicit "Chapter" mentions
        if 'chapter' in pattern.lower():
            confidence += 0.1
        
        # Boost for numeric patterns
        if r'\d+' in pattern:
            confidence += 0.05
        
        # Penalty for very short text
        if len(text.split()) < 2:
            confidence -= 0.1
        
        return max(0.1, min(1.0, confidence))
    
    def _group_chapters_by_proximity(self, chapters: List[Dict], proximity: int) -> List[List[Dict]]:
        """Group chapters that are close to each other (likely duplicates)"""
        if not chapters:
            return []
        
        # Sort by page number
        sorted_chapters = sorted(chapters, key=lambda x: x['chapter'].page_number)
        
        groups = []
        current_group = [sorted_chapters[0]]
        
        for chapter_data in sorted_chapters[1:]:
            prev_page = current_group[-1]['chapter'].page_number
            curr_page = chapter_data['chapter'].page_number
            
            if curr_page - prev_page <= proximity:
                current_group.append(chapter_data)
            else:
                groups.append(current_group)
                current_group = [chapter_data]
        
        groups.append(current_group)
        return groups
    
    def _enhance_with_group_info(self, best_chapter: Chapter, group: List[Dict]) -> Chapter:
        """Enhance chapter with information from other detections in group"""
        # Collect alternative titles
        titles = [item['chapter'].title for item in group if item['chapter'].title != best_chapter.title]
        
        # Use most common title or keep the best one
        if titles:
            title_counts = Counter([best_chapter.title] + titles)
            most_common_title = title_counts.most_common(1)[0][0]
            best_chapter.title = most_common_title
        
        # Boost confidence based on multiple detections
        detection_count = len(group)
        algorithm_diversity = len(set(item['algorithm'] for item in group))
        
        confidence_boost = min(0.3, detection_count * 0.05 + algorithm_diversity * 0.05)
        best_chapter.confidence = min(1.0, best_chapter.confidence + confidence_boost)
        
        return best_chapter
    
    def _calculate_chapter_word_count(self, chapter: Chapter, text_blocks: List[Dict[str, Any]]) -> int:
        """Calculate approximate word count for a chapter"""
        # This is simplified - in production would be more sophisticated
        next_chapter_page = chapter.page_number + 10  # Rough estimate
        
        word_count = 0
        for block in text_blocks:
            block_page = block.get('page_number', 1)
            if chapter.page_number <= block_page < next_chapter_page:
                text = block.get('text', '')
                word_count += len(text.split())
        
        return word_count
    
    def _adjust_final_confidences(self, chapters: List[Chapter]) -> None:
        """Adjust final confidence scores based on overall distribution"""
        if not chapters:
            return
        
        # Penalize chapters that are very short or very long compared to others
        word_counts = [ch.word_count for ch in chapters if ch.word_count > 0]
        if word_counts:
            avg_words = sum(word_counts) / len(word_counts)
            
            for chapter in chapters:
                if chapter.word_count > 0:
                    ratio = chapter.word_count / avg_words
                    if ratio < 0.3 or ratio > 3.0:  # Very short or very long
                        chapter.confidence *= 0.8
    
    def _deduplicate_and_sort_chapters(self, chapters: List[Chapter]) -> List[Chapter]:
        """Remove duplicate chapters and sort by page number"""
        # Remove duplicates based on page proximity
        unique_chapters = []
        
        for chapter in sorted(chapters, key=lambda c: c.page_number):
            # Check if this chapter is too close to an existing one
            is_duplicate = any(
                abs(chapter.page_number - existing.page_number) <= 1
                for existing in unique_chapters
            )
            
            if not is_duplicate:
                unique_chapters.append(chapter)
        
        return unique_chapters
    
    def _convert_headings_to_chapters(self, headings: List[Dict], source: str) -> List[Chapter]:
        """Convert heading candidates to Chapter objects"""
        chapters = []
        
        for heading in headings:
            chapter_id = str(uuid.uuid4())
            
            chapter = Chapter(
                id=chapter_id,
                number=len(chapters) + 1,
                title=heading['text'],
                summary="",
                word_count=0,
                page_number=heading['page'],
                confidence=heading['confidence']
            )
            
            chapters.append(chapter)
        
        return self._deduplicate_and_sort_chapters(chapters)
    
    def _looks_like_chapter_start(self, text: str, page_num: int, pages: Dict) -> bool:
        """Check if text looks like the start of a chapter"""
        # Check if this is the first text on a page (common for chapter starts)
        if not text:
            return False
        
        # Chapter-like patterns
        if self._is_chapter_heading_text(text):
            return True
        
        # Check if previous page ended with chapter-ending content
        prev_page = pages.get(page_num - 1, [])
        if prev_page:
            last_text = prev_page[-1].get('text', '')
            if any(ending in last_text.lower() for ending in ['the end', 'conclusion', 'summary']):
                return True
        
        return False
    
    def _calculate_font_confidence(self, font_info: Dict[str, Any], heading_criteria: Dict[str, Any]) -> float:
        """Calculate confidence score based on font characteristics"""
        confidence = 0.5  # Base confidence
        
        font_size = font_info.get('size', 12)
        is_bold = font_info.get('bold', False)
        
        # Size-based confidence boost
        min_heading_size = heading_criteria.get('min_heading_size', 14)
        large_threshold = heading_criteria.get('large_heading_threshold', 18)
        
        if font_size >= large_threshold:
            confidence += 0.4
        elif font_size >= min_heading_size:
            confidence += 0.2
        
        # Bold text bonus
        if is_bold:
            confidence += 0.2
        
        # Font name analysis (common heading fonts)
        font_name = font_info.get('name', '').lower()
        heading_fonts = ['arial', 'helvetica', 'calibri', 'times']
        if any(font in font_name for font in heading_fonts):
            confidence += 0.1
        
        return max(0.1, min(1.0, confidence))
    
    def _extract_title_from_text(self, text: str) -> str:
        """Extract a clean title from text"""
        lines = text.strip().split('\n')
        first_line = lines[0].strip()
        
        # Remove common prefixes
        prefixes = ['chapter', 'section', 'part']
        for prefix in prefixes:
            if first_line.lower().startswith(prefix):
                # Try to extract title after prefix
                parts = first_line.split(' ', 2)
                if len(parts) > 2:
                    return parts[2]
        
        # Return first meaningful line
        return first_line if first_line else f"Chapter {text[:20]}..."


class ChapterPatterns:
    """Chapter pattern definitions for different document types"""
    
    def __init__(self):
        self.patterns = {
            'academic': [
                r'^Chapter\s+(\d+)[\s\.:]\s*(.+)$',
                r'^(\d+)\.\s+(.+)$',
                r'^Section\s+(\d+)[\s\.:]\s*(.+)$',
            ],
            'business': [
                r'^Chapter\s+(\d+)[\s\.:]\s*(.+)$',
                r'^(\d+)[\.\)\s]\s+(.+)$',
                r'^Part\s+(\d+)[\s\.:]\s*(.+)$',
            ],
            'technical': [
                r'^(\d+)\.\s+(.+)$',
                r'^(\d+)\.(\d+)\s+(.+)$',
                r'^Chapter\s+(\d+)[\s\.:]\s*(.+)$',
            ]
        }


class FontAnalyzer:
    """Font analysis for heading detection"""
    
    def analyze_font_statistics(self, text_blocks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze font usage patterns across document"""
        font_sizes = []
        font_names = []
        bold_usage = []
        
        for block in text_blocks:
            font_info = block.get('font_info', {})
            if font_info:
                font_sizes.append(font_info.get('size', 12))
                font_names.append(font_info.get('name', 'unknown'))
                bold_usage.append(font_info.get('bold', False))
        
        # Calculate statistics
        if font_sizes:
            avg_size = sum(font_sizes) / len(font_sizes)
            max_size = max(font_sizes)
            size_counts = Counter(font_sizes)
            most_common_size = size_counts.most_common(1)[0][0]
        else:
            avg_size = max_size = most_common_size = 12
        
        return {
            'avg_font_size': avg_size,
            'max_font_size': max_size,
            'most_common_size': most_common_size,
            'size_distribution': Counter(font_sizes),
            'font_names': Counter(font_names),
            'bold_percentage': sum(bold_usage) / len(bold_usage) if bold_usage else 0
        }
    
    def determine_heading_criteria(self, font_stats: Dict[str, Any]) -> Dict[str, Any]:
        """Determine criteria for identifying headings"""
        avg_size = font_stats.get('avg_font_size', 12)
        max_size = font_stats.get('max_font_size', 12)
        
        return {
            'min_heading_size': max(avg_size + 2, avg_size * 1.2),
            'min_bold_heading_size': max(avg_size, 12),
            'large_heading_threshold': max_size * 0.9
        }


class ContextAnalyzer:
    """Context analysis for topic shift detection"""
    
    def detect_topic_shifts(self, text_blocks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect major topic shifts that might indicate chapter boundaries"""
        # This is a simplified implementation
        # In production, this would use NLP techniques for topic modeling
        
        topic_boundaries = []
        
        # Look for content transition indicators
        transition_indicators = [
            'now we turn to', 'in the next chapter', 'moving on to',
            'let us now examine', 'we will now discuss', 'turning our attention to'
        ]
        
        for i, block in enumerate(text_blocks):
            text = block.get('text', '').lower()
            
            # Check for explicit transition phrases
            for indicator in transition_indicators:
                if indicator in text:
                    topic_boundaries.append({
                        'page_number': block.get('page_number', 1),
                        'strength': 0.8,
                        'suggested_title': f'Chapter {len(topic_boundaries) + 1}',
                        'reason': f'Transition phrase: {indicator}'
                    })
                    break
        
        return topic_boundaries