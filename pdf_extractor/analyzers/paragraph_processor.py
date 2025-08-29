"""
Paragraph processing with intelligent classification
"""

import re
import uuid
from typing import List, Dict, Any

from ..models import Paragraph, ParagraphType, ImportanceLevel, BoundingBox, ExtractionConfig
from ..utils import logger


class ParagraphProcessor:
    """
    Intelligent paragraph processor with classification
    """
    
    def __init__(self, config: ExtractionConfig):
        self.config = config
        self.logger = logger.bind(component="ParagraphProcessor")
    
    async def extract_paragraphs_with_classification(self, text_blocks: List[Dict[str, Any]]) -> List[Paragraph]:
        """
        Extract and intelligently classify paragraphs
        """
        self.logger.info("Starting paragraph processing", text_blocks=len(text_blocks))
        
        paragraphs = []
        paragraph_id_counter = 0
        
        for block in text_blocks:
            # Clean and normalize text
            text = self._clean_text(block.get('text', ''))
            
            if len(text.strip()) < 10:  # Skip very short blocks
                continue
            
            # Split block into paragraphs if it contains multiple paragraphs
            block_paragraphs = self._split_block_into_paragraphs(text)
            
            for para_text in block_paragraphs:
                if len(para_text.strip()) < 10:
                    continue
                
                # Classify paragraph type
                para_type = self._classify_paragraph_type(para_text, block)
                
                # Determine importance
                importance = self._assess_paragraph_importance(para_text, para_type, block)
                
                # Extract concepts and terms
                concepts = self._extract_key_concepts(para_text)
                technical_terms = self._extract_technical_terms(para_text)
                
                # Create bounding box if available
                bbox = self._create_bounding_box(block.get('bbox', {}))
                
                paragraph = Paragraph(
                    id=f"para_{paragraph_id_counter:04d}",
                    chapter_id="",  # Will be assigned later
                    order_index=paragraph_id_counter,
                    content=para_text,
                    word_count=len(para_text.split()),
                    type=para_type,
                    importance=importance,
                    concepts=concepts,
                    technical_terms=technical_terms,
                    citations=[],  # Will be populated by citation processor
                    page_number=block.get('page_number', 1),
                    bounding_box=bbox,
                    font_info=block.get('font_info'),
                    confidence=self._calculate_paragraph_confidence(para_text, block)
                )
                
                paragraphs.append(paragraph)
                paragraph_id_counter += 1
        
        self.logger.info("Paragraph processing complete", paragraphs=len(paragraphs))
        return paragraphs
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove page headers/footers patterns
        text = re.sub(r'^\d+\s*$', '', text, flags=re.MULTILINE)  # Standalone page numbers
        text = re.sub(r'^Page \d+ of \d+\s*$', '', text, flags=re.MULTILINE)  # "Page X of Y"
        
        # Fix common OCR issues
        text = text.replace('ﬁ', 'fi')  # Ligature fixes
        text = text.replace('ﬂ', 'fl')
        text = text.replace('–', '-')   # En dash to hyphen
        text = text.replace('\u2019', "'")   # Smart quote to straight quote
        text = text.replace('\u201c', '"').replace('\u201d', '"')  # Smart quotes
        
        return text.strip()
    
    def _split_block_into_paragraphs(self, text: str) -> List[str]:
        """Split text block into individual paragraphs"""
        # Split on double newlines (paragraph breaks)
        paragraphs = text.split('\n\n')
        
        # Further split on single newlines if paragraphs are very long
        final_paragraphs = []
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            # If paragraph is very long, try to split on sentence boundaries
            if len(para) > 1000:  # Very long paragraph
                sentences = re.split(r'(?<=[.!?])\s+', para)
                current_para = ""
                
                for sentence in sentences:
                    if len(current_para + sentence) > 500 and current_para:
                        final_paragraphs.append(current_para.strip())
                        current_para = sentence
                    else:
                        current_para += " " + sentence if current_para else sentence
                
                if current_para.strip():
                    final_paragraphs.append(current_para.strip())
            else:
                final_paragraphs.append(para)
        
        return final_paragraphs
    
    def _classify_paragraph_type(self, text: str, block: Dict) -> ParagraphType:
        """Intelligent paragraph type classification"""
        
        # Heading detection
        if self._is_heading(text, block):
            return ParagraphType.HEADING
        
        # Quote detection
        if self._is_quote(text, block):
            return ParagraphType.QUOTE
        
        # List detection
        if self._is_list(text, block):
            return ParagraphType.LIST
        
        # Caption detection
        if self._is_caption(text, block):
            return ParagraphType.CAPTION
        
        # Code block detection
        if self._is_code_block(text, block):
            return ParagraphType.CODE
        
        return ParagraphType.TEXT
    
    def _is_heading(self, text: str, block: Dict) -> bool:
        """Detect if text is a heading"""
        
        # Font-based detection
        font_info = block.get('font_info', {})
        if font_info:
            font_size = font_info.get('size', 12)
            is_bold = font_info.get('bold', False)
            
            # Typically headings are larger and/or bold
            if font_size > 14 or is_bold:
                # Additional validation
                if len(text.split()) < 20 and not text.endswith('.'):
                    return True
        
        # Pattern-based detection
        heading_patterns = [
            r'^\d+\.\d*\s+\w+',  # "1.1 Introduction"
            r'^[IVX]+\.\s+\w+',   # "II. Methodology"
            r'^[A-Z\s]{3,}$',     # "EXECUTIVE SUMMARY"
            r'^Chapter\s+\d+',    # "Chapter 1"
        ]
        
        for pattern in heading_patterns:
            if re.match(pattern, text.strip()):
                return True
        
        # Length and punctuation heuristics
        if len(text.split()) <= 10 and not text.endswith(('.', '!', '?')):
            # Check if it's all caps or title case
            if text.isupper() or text.istitle():
                return True
        
        return False
    
    def _is_quote(self, text: str, block: Dict) -> bool:
        """Detect if text is a quote"""
        
        # Quotation marks
        if (text.startswith('"') and text.endswith('"')) or \
           (text.startswith("'") and text.endswith("'")):
            return True
        
        # Block quote indicators
        if text.startswith('> ') or text.startswith('    '):  # Indented
            return True
        
        # Quote attribution patterns
        if re.search(r'—\s*[A-Z][a-z]+\s*[A-Z][a-z]+$', text):  # "— Author Name"
            return True
        
        return False
    
    def _is_list(self, text: str, block: Dict) -> bool:
        """Detect if text is a list"""
        
        lines = text.split('\n')
        
        # Check for bullet points or numbering
        list_patterns = [
            r'^\s*[\•\*\-\+]\s+',  # Bullet points
            r'^\s*\d+[\.\)]\s+',   # Numbered lists
            r'^\s*[a-z][\.\)]\s+', # Lettered lists
            r'^\s*[IVX]+[\.\)]\s+' # Roman numeral lists
        ]
        
        matching_lines = 0
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            for pattern in list_patterns:
                if re.match(pattern, line):
                    matching_lines += 1
                    break
        
        # If more than half the lines match list patterns
        non_empty_lines = len([line for line in lines if line.strip()])
        return matching_lines > non_empty_lines / 2 and matching_lines >= 2
    
    def _is_caption(self, text: str, block: Dict) -> bool:
        """Detect if text is an image/table caption"""
        
        # Caption keywords
        caption_patterns = [
            r'^Figure\s+\d+',
            r'^Table\s+\d+',
            r'^Image\s+\d+',
            r'^Diagram\s+\d+',
            r'^Chart\s+\d+',
            r'^Photo\s+\d+'
        ]
        
        for pattern in caption_patterns:
            if re.match(pattern, text, re.IGNORECASE):
                return True
        
        # Short text near images (would need image context)
        if len(text.split()) <= 20 and ':' in text:
            return True
        
        return False
    
    def _is_code_block(self, text: str, block: Dict) -> bool:
        """Detect if text is a code block"""
        
        # Code indicators
        code_indicators = [
            'function', 'class', 'def ', 'var ', 'let ', 'const ',
            '{', '}', '()', '=>', 'return', 'if (', 'for (', 'while ('
        ]
        
        # Check for monospace font
        font_info = block.get('font_info', {})
        font_name = font_info.get('name', '').lower()
        if any(mono in font_name for mono in ['mono', 'courier', 'consolas']):
            return True
        
        # Check for code patterns
        code_score = sum(1 for indicator in code_indicators if indicator in text)
        return code_score >= 3
    
    def _assess_paragraph_importance(self, text: str, para_type: ParagraphType, block: Dict) -> ImportanceLevel:
        """Assess paragraph importance"""
        
        # Headings are always high importance
        if para_type == ParagraphType.HEADING:
            return ImportanceLevel.HIGH
        
        # Check for importance keywords
        high_importance_keywords = [
            'important', 'critical', 'key', 'essential', 'fundamental',
            'conclusion', 'summary', 'result', 'finding'
        ]
        
        medium_importance_keywords = [
            'note', 'consider', 'remember', 'example', 'instance'
        ]
        
        text_lower = text.lower()
        
        if any(keyword in text_lower for keyword in high_importance_keywords):
            return ImportanceLevel.HIGH
        elif any(keyword in text_lower for keyword in medium_importance_keywords):
            return ImportanceLevel.MEDIUM
        
        # Font size based importance
        font_info = block.get('font_info', {})
        font_size = font_info.get('size', 12)
        
        if font_size > 13:
            return ImportanceLevel.HIGH
        elif font_size > 11:
            return ImportanceLevel.MEDIUM
        
        return ImportanceLevel.LOW
    
    def _extract_key_concepts(self, text: str) -> List[str]:
        """Extract key concepts from text"""
        concepts = []
        
        # Simple concept extraction based on capitalized terms
        capitalized_terms = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        
        # Filter out common words and keep meaningful terms
        common_words = {'The', 'This', 'That', 'These', 'Those', 'A', 'An'}
        concepts = [term for term in capitalized_terms if term not in common_words and len(term) > 3]
        
        # Remove duplicates and limit
        concepts = list(dict.fromkeys(concepts))[:10]
        
        return concepts
    
    def _extract_technical_terms(self, text: str) -> List[str]:
        """Extract technical terms from text"""
        technical_terms = []
        
        # Look for terms with specific patterns
        patterns = [
            r'\b[A-Z]{2,}\b',  # Acronyms
            r'\b\w+[_-]\w+\b',  # Compound terms with _ or -
            r'\b\w*[Tt]ech\w*\b',  # Terms containing 'tech'
            r'\b\w*[Aa]lgorithm\w*\b',  # Algorithm-related terms
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            technical_terms.extend(matches)
        
        # Remove duplicates and limit
        technical_terms = list(dict.fromkeys(technical_terms))[:15]
        
        return technical_terms
    
    def _create_bounding_box(self, bbox_data: Dict) -> BoundingBox:
        """Create BoundingBox object from bbox data"""
        if not bbox_data:
            return None
        
        return BoundingBox(
            x=bbox_data.get('x0', 0),
            y=bbox_data.get('y0', 0),
            width=bbox_data.get('x1', 0) - bbox_data.get('x0', 0),
            height=bbox_data.get('y1', 0) - bbox_data.get('y0', 0)
        )
    
    def _calculate_paragraph_confidence(self, text: str, block: Dict) -> float:
        """Calculate confidence score for paragraph classification"""
        confidence = 0.8  # Base confidence
        
        # Boost confidence for clean text
        if re.match(r'^[A-Za-z0-9\s\.,!?;:()\-"\']+$', text):
            confidence += 0.1
        
        # Penalize for very short or very long paragraphs
        word_count = len(text.split())
        if word_count < 5 or word_count > 500:
            confidence -= 0.1
        
        # Boost confidence if font info is available
        if block.get('font_info'):
            confidence += 0.05
        
        return max(0.1, min(1.0, confidence))