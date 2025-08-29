"""
Quality assessment engine for extraction validation
"""

from typing import Dict, Any

from ..models import BookContent, QualityMetrics, ExtractionConfig
from ..utils import logger


class QualityAssessmentEngine:
    """
    Quality assessment and validation engine
    """
    
    def __init__(self, config: ExtractionConfig):
        self.config = config
        self.logger = logger.bind(component="QualityAssessment")
    
    async def comprehensive_quality_check(self, content: BookContent) -> Dict[str, Any]:
        """
        Comprehensive quality assessment of extraction results
        """
        self.logger.debug("Starting comprehensive quality check")
        
        # Calculate individual metrics
        structure_confidence = self._assess_structure_quality(content)
        content_confidence = self._assess_content_quality(content)
        image_confidence = self._assess_image_quality(content)
        citation_confidence = self._assess_citation_quality(content)
        
        # Calculate overall confidence
        overall_confidence = (
            structure_confidence * 0.3 +
            content_confidence * 0.4 +
            image_confidence * 0.2 +
            citation_confidence * 0.1
        )
        
        quality_report = {
            'overall_confidence': overall_confidence,
            'structure_confidence': structure_confidence,
            'content_confidence': content_confidence,
            'image_confidence': image_confidence,
            'citation_confidence': citation_confidence,
            'issues': [],
            'recommendations': []
        }
        
        # Add issues and recommendations based on low scores
        if structure_confidence < 0.8:
            quality_report['issues'].append('Low structure confidence - chapters may need validation')
            quality_report['recommendations'].append('Review chapter boundaries and hierarchy')
        
        if content_confidence < 0.8:
            quality_report['issues'].append('Low content confidence - text extraction may have issues')
            quality_report['recommendations'].append('Verify text quality and paragraph classification')
        
        if image_confidence < 0.7:
            quality_report['issues'].append('Low image confidence - image descriptions may be generic')
            quality_report['recommendations'].append('Enhance image descriptions with context')
        
        self.logger.info(
            "Quality assessment complete",
            overall_confidence=overall_confidence,
            issues=len(quality_report['issues'])
        )
        
        return quality_report
    
    async def calculate_final_quality_metrics(self, content: BookContent) -> QualityMetrics:
        """
        Calculate final quality metrics for the extraction
        """
        quality_check = await self.comprehensive_quality_check(content)
        
        return QualityMetrics(
            overall_confidence=quality_check['overall_confidence'],
            structure_confidence=quality_check['structure_confidence'],
            content_confidence=quality_check['content_confidence'],
            image_confidence=quality_check['image_confidence'],
            citation_confidence=quality_check['citation_confidence']
        )
    
    def _assess_structure_quality(self, content: BookContent) -> float:
        """Assess structural quality of the extraction"""
        confidence = 0.8  # Base confidence
        
        # Check chapter consistency
        if content.chapters:
            # Sequential numbering
            chapter_numbers = [ch.number for ch in content.chapters if ch.number]
            if chapter_numbers:
                expected = list(range(1, len(chapter_numbers) + 1))
                if chapter_numbers == expected:
                    confidence += 0.1
                else:
                    confidence -= 0.1
            
            # Reasonable chapter lengths
            word_counts = [ch.word_count for ch in content.chapters if ch.word_count > 0]
            if word_counts:
                avg_words = sum(word_counts) / len(word_counts)
                # Check for chapters that are too short or too long
                outliers = [wc for wc in word_counts if wc < avg_words * 0.3 or wc > avg_words * 3]
                if len(outliers) / len(word_counts) > 0.2:  # More than 20% outliers
                    confidence -= 0.1
        else:
            confidence -= 0.3  # No chapters detected
        
        return max(0.0, min(1.0, confidence))
    
    def _assess_content_quality(self, content: BookContent) -> float:
        """Assess content extraction quality"""
        confidence = 0.8  # Base confidence
        
        # Check paragraph quality
        if content.paragraphs:
            # Reasonable paragraph lengths
            word_counts = [p.word_count for p in content.paragraphs]
            very_short = sum(1 for wc in word_counts if wc < 5)
            very_long = sum(1 for wc in word_counts if wc > 500)
            
            # Too many very short or very long paragraphs indicates issues
            total_paras = len(content.paragraphs)
            if (very_short + very_long) / total_paras > 0.3:
                confidence -= 0.2
            
            # Check for reasonable paragraph confidence scores
            para_confidences = [p.confidence for p in content.paragraphs if hasattr(p, 'confidence')]
            if para_confidences:
                avg_confidence = sum(para_confidences) / len(para_confidences)
                confidence *= avg_confidence  # Weight by paragraph confidence
        else:
            confidence -= 0.4  # No paragraphs extracted
        
        return max(0.0, min(1.0, confidence))
    
    def _assess_image_quality(self, content: BookContent) -> float:
        """Assess image extraction quality"""
        if not content.images:
            return 0.7  # Neutral score for no images
        
        confidence = 0.8  # Base confidence
        
        # Check image description quality
        generic_descriptions = 0
        for image in content.images:
            desc = image.description.lower()
            if any(generic in desc for generic in ['image', 'chart', 'diagram']) and len(desc.split()) < 5:
                generic_descriptions += 1
        
        if generic_descriptions > 0:
            penalty = min(0.3, generic_descriptions / len(content.images))
            confidence -= penalty
        
        # Check for image context
        images_with_context = sum(1 for img in content.images 
                                 if img.reference_mentions or img.relevance_score > 7)
        context_ratio = images_with_context / len(content.images)
        confidence *= (0.7 + 0.3 * context_ratio)  # Boost for good context
        
        return max(0.0, min(1.0, confidence))
    
    def _assess_citation_quality(self, content: BookContent) -> float:
        """Assess citation extraction quality"""
        if not content.citations:
            return 0.8  # Neutral score for no citations
        
        confidence = 0.8  # Base confidence
        
        # Check citation completeness
        valid_citations = sum(1 for cit in content.citations 
                            if len(cit.content.strip()) > 10)
        
        if len(content.citations) > 0:
            completeness_ratio = valid_citations / len(content.citations)
            confidence *= completeness_ratio
        
        return max(0.0, min(1.0, confidence))