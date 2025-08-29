"""
Intelligent citation detection and processing
"""

import re
import uuid
from typing import List, Dict, Any

from ..models import Citation, CitationType, ExtractionConfig
from ..utils import logger


class CitationProcessor:
    """
    Intelligent citation detection with style recognition
    """
    
    def __init__(self, config: ExtractionConfig):
        self.config = config
        self.logger = logger.bind(component="CitationProcessor")
        
        self.style_detector = CitationStyleDetector()
        self.pattern_matcher = CitationPatternMatcher()
    
    async def detect_citations_intelligently(self, text_blocks: List[Dict[str, Any]]) -> List[Citation]:
        """
        Multi-algorithm citation detection
        """
        self.logger.info("Starting intelligent citation detection", text_blocks=len(text_blocks))
        
        # Combine all text for style detection
        full_text = " ".join([block.get('text', '') for block in text_blocks])
        
        # Step 1: Detect citation style
        citation_style = self.style_detector.detect_citation_style(full_text)
        self.logger.debug("Detected citation style", style=citation_style)
        
        # Step 2: Extract citations based on detected style
        if citation_style == 'apa':
            citations = self._extract_apa_citations(text_blocks)
        elif citation_style == 'mla':
            citations = self._extract_mla_citations(text_blocks)
        elif citation_style == 'ieee':
            citations = self._extract_ieee_citations(text_blocks)
        else:
            # Mixed or unknown style - use all methods
            citations = self._extract_mixed_citations(text_blocks)
        
        # Step 3: Validate and clean citations
        validated_citations = self._validate_citations(citations)
        
        self.logger.info("Citation detection complete", citations=len(validated_citations))
        return validated_citations
    
    def _extract_apa_citations(self, text_blocks: List[Dict[str, Any]]) -> List[Citation]:
        """Extract APA style citations"""
        citations = []
        
        apa_patterns = [
            (r'\(([A-Z][a-z]+,\s+\d{4})\)', CitationType.INLINE),
            (r'\(([A-Z][a-z]+\s+&\s+[A-Z][a-z]+,\s+\d{4})\)', CitationType.INLINE),
            (r'\(([A-Z][a-z]+\s+et\s+al\.,\s+\d{4})\)', CitationType.INLINE)
        ]
        
        for block in text_blocks:
            text = block.get('text', '')
            page_num = block.get('page_number', 1)
            
            for pattern, citation_type in apa_patterns:
                matches = re.finditer(pattern, text)
                for match in matches:
                    citation = Citation(
                        id=str(uuid.uuid4()),
                        type=citation_type,
                        content=match.group(1),
                        page_number=page_num
                    )
                    citations.append(citation)
        
        return citations
    
    def _extract_mla_citations(self, text_blocks: List[Dict[str, Any]]) -> List[Citation]:
        """Extract MLA style citations"""
        citations = []
        
        mla_patterns = [
            (r'\(([A-Z][a-z]+\s+\d+)\)', CitationType.INLINE),
            (r'\(([A-Z][a-z]+,\s+"[^"]+"\s+\d+)\)', CitationType.INLINE)
        ]
        
        for block in text_blocks:
            text = block.get('text', '')
            page_num = block.get('page_number', 1)
            
            for pattern, citation_type in mla_patterns:
                matches = re.finditer(pattern, text)
                for match in matches:
                    citation = Citation(
                        id=str(uuid.uuid4()),
                        type=citation_type,
                        content=match.group(1),
                        page_number=page_num
                    )
                    citations.append(citation)
        
        return citations
    
    def _extract_ieee_citations(self, text_blocks: List[Dict[str, Any]]) -> List[Citation]:
        """Extract IEEE style citations"""
        citations = []
        
        ieee_patterns = [
            (r'\[(\d+)\]', CitationType.INLINE),
            (r'\[(\d+\-\d+)\]', CitationType.INLINE)
        ]
        
        for block in text_blocks:
            text = block.get('text', '')
            page_num = block.get('page_number', 1)
            
            for pattern, citation_type in ieee_patterns:
                matches = re.finditer(pattern, text)
                for match in matches:
                    citation = Citation(
                        id=str(uuid.uuid4()),
                        type=citation_type,
                        content=match.group(1),
                        page_number=page_num
                    )
                    citations.append(citation)
        
        return citations
    
    def _extract_mixed_citations(self, text_blocks: List[Dict[str, Any]]) -> List[Citation]:
        """Extract citations using all methods (for mixed or unknown styles)"""
        all_citations = []
        
        # Try all styles
        all_citations.extend(self._extract_apa_citations(text_blocks))
        all_citations.extend(self._extract_mla_citations(text_blocks))
        all_citations.extend(self._extract_ieee_citations(text_blocks))
        
        # Also look for bibliography/reference sections
        all_citations.extend(self._extract_bibliography_citations(text_blocks))
        
        # Remove duplicates
        unique_citations = self._remove_duplicate_citations(all_citations)
        
        return unique_citations
    
    def _extract_bibliography_citations(self, text_blocks: List[Dict[str, Any]]) -> List[Citation]:
        """Extract bibliography/reference list citations"""
        citations = []
        
        # Look for bibliography/reference sections
        in_bibliography = False
        
        for block in text_blocks:
            text = block.get('text', '')
            text_lower = text.lower()
            page_num = block.get('page_number', 1)
            
            # Check if we're entering a bibliography section
            if any(keyword in text_lower for keyword in ['references', 'bibliography', 'works cited']):
                in_bibliography = True
                continue
            
            # Check if we're leaving bibliography (new chapter/section)
            if in_bibliography and any(keyword in text_lower for keyword in ['chapter', 'appendix', 'index']):
                in_bibliography = False
            
            if in_bibliography:
                # Extract individual references
                lines = text.split('\n')
                for line in lines:
                    line = line.strip()
                    if self._is_bibliography_entry(line):
                        citation = Citation(
                            id=str(uuid.uuid4()),
                            type=CitationType.BIBLIOGRAPHY,
                            content=line,
                            page_number=page_num
                        )
                        citations.append(citation)
        
        return citations
    
    def _is_bibliography_entry(self, line: str) -> bool:
        """Check if a line is a bibliography entry"""
        if len(line) < 20:  # Too short to be a proper citation
            return False
        
        # Common bibliography patterns
        patterns = [
            r'^[A-Z][a-z]+,\s+[A-Z]',  # "Author, A."
            r'^\d+\.\s+[A-Z]',         # "1. Author"
            r'^[A-Z][a-z]+,\s+[A-Z][a-z]+',  # "Author, Title"
        ]
        
        return any(re.match(pattern, line) for pattern in patterns)
    
    def _validate_citations(self, citations: List[Citation]) -> List[Citation]:
        """Validate and clean citations"""
        validated = []
        
        for citation in citations:
            # Skip very short citations
            if len(citation.content.strip()) < 3:
                continue
            
            # Clean up content
            citation.content = citation.content.strip()
            
            # Skip obvious false positives
            if self._is_false_positive(citation.content):
                continue
            
            validated.append(citation)
        
        return validated
    
    def _is_false_positive(self, content: str) -> bool:
        """Check if citation is likely a false positive"""
        # Common false positives
        false_positive_patterns = [
            r'^\d+$',  # Just a number
            r'^[A-Z]$',  # Just a letter
            r'^see\s+',  # "see page" references
            r'^page\s+\d+',  # Page references
        ]
        
        content_lower = content.lower()
        return any(re.match(pattern, content_lower) for pattern in false_positive_patterns)
    
    def _remove_duplicate_citations(self, citations: List[Citation]) -> List[Citation]:
        """Remove duplicate citations"""
        seen_content = set()
        unique_citations = []
        
        for citation in citations:
            if citation.content not in seen_content:
                seen_content.add(citation.content)
                unique_citations.append(citation)
        
        return unique_citations


class CitationStyleDetector:
    """Detect citation style used in document"""
    
    def detect_citation_style(self, text: str) -> str:
        """Detect the primary citation style"""
        
        # APA patterns
        apa_patterns = [
            r'\([A-Z][a-z]+,\s+\d{4}\)',  # (Smith, 2020)
            r'\([A-Z][a-z]+\s+&\s+[A-Z][a-z]+,\s+\d{4}\)',  # (Smith & Jones, 2020)
            r'\([A-Z][a-z]+\s+et\s+al\.,\s+\d{4}\)'  # (Smith et al., 2020)
        ]
        
        # MLA patterns
        mla_patterns = [
            r'\([A-Z][a-z]+\s+\d+\)',  # (Smith 45)
            r'\([A-Z][a-z]+,\s+"[^"]+"\s+\d+\)'  # (Smith, "Title" 45)
        ]
        
        # IEEE patterns
        ieee_patterns = [
            r'\[\d+\]',  # [1]
            r'\[\d+\-\d+\]'  # [1-3]
        ]
        
        # Count pattern matches
        apa_count = sum(len(re.findall(pattern, text)) for pattern in apa_patterns)
        mla_count = sum(len(re.findall(pattern, text)) for pattern in mla_patterns)
        ieee_count = sum(len(re.findall(pattern, text)) for pattern in ieee_patterns)
        
        # Determine dominant style
        if apa_count > mla_count and apa_count > ieee_count and apa_count > 2:
            return 'apa'
        elif mla_count > ieee_count and mla_count > 2:
            return 'mla'
        elif ieee_count > 2:
            return 'ieee'
        else:
            return 'mixed'


class CitationPatternMatcher:
    """Pattern matching for different citation styles"""
    
    def __init__(self):
        self.patterns = {
            'apa': [
                r'\(([A-Z][a-z]+,\s+\d{4})\)',
                r'\(([A-Z][a-z]+\s+&\s+[A-Z][a-z]+,\s+\d{4})\)',
                r'\(([A-Z][a-z]+\s+et\s+al\.,\s+\d{4})\)'
            ],
            'mla': [
                r'\(([A-Z][a-z]+\s+\d+)\)',
                r'\(([A-Z][a-z]+,\s+"[^"]+"\s+\d+)\)'
            ],
            'ieee': [
                r'\[(\d+)\]',
                r'\[(\d+\-\d+)\]'
            ],
            'chicago': [
                r'\(([A-Z][a-z]+\s+\d{4},\s+\d+)\)',
                r'([A-Z][a-z]+\s+\d{4},\s+\d+)'
            ]
        }
    
    def match_citations(self, text: str, style: str) -> List[str]:
        """Match citations for a specific style"""
        patterns = self.patterns.get(style, [])
        matches = []
        
        for pattern in patterns:
            found = re.findall(pattern, text)
            matches.extend(found)
        
        return matches