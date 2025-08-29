"""
Intelligent image processing with positioning and context analysis
"""

import base64
import uuid
from typing import List, Dict, Any

from ..models import ImageData, ImageType, TextPosition, ColumnPosition, FlowContext, ReferenceMention, SpatialRelationships, BoundingBox, ExtractionConfig
from ..utils import logger


class ImageProcessor:
    """
    Intelligent image processor with context analysis and positioning
    """
    
    def __init__(self, config: ExtractionConfig):
        self.config = config
        self.logger = logger.bind(component="ImageProcessor")
    
    async def process_images_with_intelligence(self, images: List[Dict[str, Any]], paragraphs: List, chapters: List) -> List[ImageData]:
        """
        Process images with intelligent classification and description
        """
        self.logger.info("Starting intelligent image processing", images=len(images))
        
        processed_images = []
        
        for img_data in images:
            try:
                # Generate unique ID
                image_id = img_data.get('id', str(uuid.uuid4()))
                
                # Classify image type intelligently
                image_type = self._classify_image_type(img_data)
                
                # Get surrounding context
                context = self._extract_image_context(img_data, paragraphs)
                
                # Analyze positioning relative to text
                positioning = self._analyze_image_positioning(img_data, paragraphs)
                
                # Generate intelligent description
                description = self._generate_smart_description(img_data, image_type, context)
                
                # Calculate relevance score
                relevance = self._calculate_relevance_score(context, description)
                
                # Create bounding box
                bbox_data = img_data.get('bbox', {})
                bounding_box = BoundingBox(
                    x=bbox_data.get('x0', 0),
                    y=bbox_data.get('y0', 0),
                    width=bbox_data.get('x1', 0) - bbox_data.get('x0', 0),
                    height=bbox_data.get('y1', 0) - bbox_data.get('y0', 0)
                )
                
                # Find associated chapter
                chapter_id = self._find_associated_chapter(img_data, chapters)
                
                image = ImageData(
                    id=image_id,
                    chapter_id=chapter_id,
                    paragraph_id=positioning.get('paragraph_before_id'),
                    type=image_type,
                    file_name=f"{image_id}.png",
                    file_size=img_data.get('file_size', 0),
                    width=img_data.get('width', 0),
                    height=img_data.get('height', 0),
                    caption=context.get('caption'),
                    alt_text=description,
                    description=description,
                    relevance_score=relevance,
                    preservation_notes="",
                    improvement_suggestions=[],
                    page_number=img_data.get('page_number', 1),
                    bounding_box=bounding_box,
                    text_position=TextPosition(positioning['text_position']),
                    paragraph_before_id=positioning.get('paragraph_before_id'),
                    paragraph_after_id=positioning.get('paragraph_after_id'),
                    column_position=ColumnPosition(positioning.get('column_position', 'center')),
                    flow_context=FlowContext(**positioning['flow_context']),
                    reference_mentions=[ReferenceMention(**ref) for ref in positioning.get('reference_mentions', [])],
                    spatial_relationships=SpatialRelationships(**positioning['spatial_relationships']),
                    raw_data=img_data.get('raw_data'),
                    description_confidence=img_data.get('confidence', 0.8)
                )
                
                processed_images.append(image)
                
            except Exception as e:
                self.logger.warning(f"Failed to process image {img_data.get('id', 'unknown')}", error=str(e))
                continue
        
        self.logger.info("Image processing complete", processed_images=len(processed_images))
        return processed_images
    
    def _classify_image_type(self, img_data: Dict[str, Any]) -> ImageType:
        """Intelligent image type classification"""
        
        # Analyze image characteristics
        width = img_data.get('width', 0)
        height = img_data.get('height', 0)
        aspect_ratio = width / height if height > 0 else 1.0
        
        # Size-based heuristics
        if width > 400 and height > 300:
            # Likely a substantial image
            if 0.8 < aspect_ratio < 1.2:
                return ImageType.CHART  # Square-ish, likely a chart
            elif aspect_ratio > 1.5:
                return ImageType.DIAGRAM  # Wide, likely a process diagram
        
        # Small images are likely icons or simple graphics
        if width < 100 or height < 100:
            return ImageType.ILLUSTRATION
        
        # Analyze context if available (simplified)
        # In production, would use actual image analysis
        if self._has_chart_characteristics(img_data):
            return ImageType.CHART
        elif self._has_diagram_characteristics(img_data):
            return ImageType.DIAGRAM
        elif self._has_photo_characteristics(img_data):
            return ImageType.PHOTO
        elif self._has_table_characteristics(img_data):
            return ImageType.TABLE
        else:
            return ImageType.ILLUSTRATION
    
    def _has_chart_characteristics(self, img_data: Dict) -> bool:
        """Check if image has chart characteristics"""
        # This is a placeholder - in production would analyze actual image data
        return False
    
    def _has_diagram_characteristics(self, img_data: Dict) -> bool:
        """Check if image has diagram characteristics"""
        # Placeholder for actual image analysis
        return False
    
    def _has_photo_characteristics(self, img_data: Dict) -> bool:
        """Check if image has photo characteristics"""
        # Placeholder for actual image analysis
        return False
    
    def _has_table_characteristics(self, img_data: Dict) -> bool:
        """Check if image has table characteristics"""
        # Placeholder for actual image analysis
        return False
    
    def _extract_image_context(self, img_data: Dict, paragraphs: List) -> Dict[str, Any]:
        """Extract context around the image"""
        img_page = img_data.get('page_number', 1)
        context = {
            'preceding_text': "",
            'following_text': "",
            'caption': None
        }
        
        # Find paragraphs on the same page
        page_paragraphs = [p for p in paragraphs if hasattr(p, 'page_number') and p.page_number == img_page]
        
        if not page_paragraphs:
            return context
        
        # Sort by order index
        page_paragraphs.sort(key=lambda p: getattr(p, 'order_index', 0))
        
        # Get text before and after image (simplified approach)
        # In production, would use actual positioning data
        mid_point = len(page_paragraphs) // 2
        
        if page_paragraphs:
            # Preceding text
            preceding_paras = page_paragraphs[:mid_point]
            if preceding_paras:
                context['preceding_text'] = " ".join([getattr(p, 'content', '') for p in preceding_paras[-2:]])[:200]
            
            # Following text  
            following_paras = page_paragraphs[mid_point:]
            if following_paras:
                context['following_text'] = " ".join([getattr(p, 'content', '') for p in following_paras[:2]])[:200]
            
            # Look for captions (simplified)
            for para in page_paragraphs:
                para_content = getattr(para, 'content', '')
                if any(keyword in para_content.lower() for keyword in ['figure', 'table', 'image', 'chart']):
                    if len(para_content.split()) <= 20:  # Short, likely a caption
                        context['caption'] = para_content
                        break
        
        return context
    
    def _analyze_image_positioning(self, img_data: Dict, paragraphs: List) -> Dict[str, Any]:
        """Analyze image position relative to text"""
        
        img_bbox = img_data.get('bbox', {})
        img_page = img_data.get('page_number', 1)
        
        # Find paragraphs on the same page
        page_paragraphs = [p for p in paragraphs if hasattr(p, 'page_number') and p.page_number == img_page]
        
        # Basic positioning analysis (simplified)
        positioning = {
            'text_position': 'inline',  # Default
            'paragraph_before_id': None,
            'paragraph_after_id': None,
            'column_position': 'center',
            'flow_context': {
                'wrapping_style': 'none',
                'text_density_around': 0.5,
                'creates_column_break': False
            },
            'reference_mentions': [],
            'spatial_relationships': {
                'paragraphs_above': 0,
                'paragraphs_below': 0,
                'paragraphs_alongside': 0
            }
        }
        
        if page_paragraphs:
            # Simple before/after assignment based on order
            mid_index = len(page_paragraphs) // 2
            
            if mid_index > 0:
                positioning['paragraph_before_id'] = getattr(page_paragraphs[mid_index - 1], 'id', None)
            if mid_index < len(page_paragraphs) - 1:
                positioning['paragraph_after_id'] = getattr(page_paragraphs[mid_index], 'id', None)
            
            # Spatial relationships
            positioning['spatial_relationships'] = {
                'paragraphs_above': mid_index,
                'paragraphs_below': len(page_paragraphs) - mid_index,
                'paragraphs_alongside': 0
            }
            
            # Look for references to this image
            positioning['reference_mentions'] = self._find_image_references(page_paragraphs, img_data)
        
        return positioning
    
    def _find_image_references(self, paragraphs: List, img_data: Dict) -> List[Dict[str, Any]]:
        """Find textual references to the image"""
        references = []
        
        # Common reference patterns
        reference_patterns = [
            r'(?i)\b(?:figure|fig\.?)\s+(\d+|[a-z])\b',
            r'(?i)\b(?:chart|graph)\s+(\d+|[a-z])\b',
            r'(?i)\b(?:table)\s+(\d+|[a-z])\b',
            r'(?i)\b(?:image|picture)\s+(\d+|[a-z])\b',
            r'(?i)(?:above|below|following|preceding)\s+(?:figure|chart|graph|table|image|diagram)'
        ]
        
        for para in paragraphs:
            if not hasattr(para, 'content'):
                continue
                
            text = para.content
            
            for pattern in reference_patterns:
                import re
                matches = list(re.finditer(pattern, text))
                for match in matches:
                    reference = {
                        'text': match.group(0),
                        'type': 'explicit_reference' if match.groups() else 'implicit_reference',
                        'paragraph_id': para.id,
                        'position_in_text': match.start()
                    }
                    if match.groups():
                        reference['reference_number'] = match.group(1)
                    
                    references.append(reference)
        
        return references
    
    def _generate_smart_description(self, img_data: Dict, image_type: ImageType, context: Dict) -> str:
        """Generate intelligent image descriptions"""
        
        # Base description from type
        base_descriptions = {
            ImageType.CHART: 'Data visualization chart',
            ImageType.DIAGRAM: 'Process or conceptual diagram',
            ImageType.GRAPH: 'Statistical graph',
            ImageType.TABLE: 'Tabular data presentation',
            ImageType.PHOTO: 'Photographic image',
            ImageType.ILLUSTRATION: 'Illustrative graphic'
        }
        
        base_desc = base_descriptions.get(image_type, 'Image')
        
        # Enhance with context
        preceding_text = context.get('preceding_text', '').lower()
        
        if preceding_text:
            # Look for specific context clues
            if any(word in preceding_text for word in ['sales', 'revenue', 'profit']):
                if image_type == ImageType.CHART:
                    base_desc = 'Sales/revenue chart'
            elif any(word in preceding_text for word in ['process', 'workflow', 'steps']):
                if image_type == ImageType.DIAGRAM:
                    base_desc = 'Process workflow diagram'
            elif any(word in preceding_text for word in ['comparison', 'versus', 'compare']):
                if image_type == ImageType.CHART:
                    base_desc = 'Comparison chart'
        
        # Add caption if available
        caption = context.get('caption')
        if caption:
            return f"{base_desc}: {caption}"
        
        # Add size information for context
        width = img_data.get('width', 0)
        height = img_data.get('height', 0)
        if width and height:
            return f"{base_desc} ({width}x{height} pixels)"
        
        return base_desc
    
    def _calculate_relevance_score(self, context: Dict, description: str) -> float:
        """Calculate relevance score for the image"""
        relevance = 5.0  # Base score (1-10 scale)
        
        # Boost for having context
        if context.get('preceding_text') or context.get('following_text'):
            relevance += 1.0
        
        # Boost for having a caption
        if context.get('caption'):
            relevance += 1.5
        
        # Boost for detailed description
        if len(description.split()) > 5:
            relevance += 1.0
        
        # Cap at 10.0
        return min(10.0, relevance)
    
    def _find_associated_chapter(self, img_data: Dict, chapters: List) -> str:
        """Find which chapter this image belongs to"""
        img_page = img_data.get('page_number', 1)
        
        # Find the chapter that contains this page
        associated_chapter = None
        for chapter in chapters:
            if hasattr(chapter, 'page_number') and chapter.page_number <= img_page:
                if not associated_chapter or chapter.page_number > associated_chapter.page_number:
                    associated_chapter = chapter
        
        return associated_chapter.id if associated_chapter else ""