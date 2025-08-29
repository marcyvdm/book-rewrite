"""
PDFPlumber-based PDF extraction engine
"""

import base64
from pathlib import Path
from typing import List, Dict, Any, ContextManager
from contextlib import contextmanager

try:
    import pdfplumber
except ImportError:
    raise ImportError("pdfplumber is required. Install with: pip install pdfplumber")

from .base_engine import BasePDFEngine
from ..utils import logger


class PDFPlumberEngine(BasePDFEngine):
    """
    PDF extraction engine using pdfplumber library
    """
    
    def __init__(self, config):
        super().__init__(config)
        self.logger = logger.bind(component="PDFPlumberEngine")
    
    @contextmanager
    def open_pdf(self, pdf_path: Path) -> ContextManager[pdfplumber.PDF]:
        """
        Open PDF file using pdfplumber
        """
        self.logger.debug("Opening PDF with pdfplumber", path=str(pdf_path))
        
        try:
            pdf = pdfplumber.open(pdf_path)
            yield pdf
        except Exception as e:
            self.logger.error("Failed to open PDF", error=str(e))
            raise
        finally:
            try:
                pdf.close()
            except:
                pass
    
    def extract_text_blocks(self, page: pdfplumber.page.Page) -> List[Dict[str, Any]]:
        """
        Extract text blocks with detailed positioning from pdfplumber page
        """
        text_blocks = []
        
        try:
            # Extract characters with positioning
            chars = page.chars
            
            if not chars:
                # Fallback to basic text extraction
                text = page.extract_text()
                if text:
                    bbox = {
                        'x0': 0,
                        'y0': 0,
                        'x1': page.width,
                        'y1': page.height
                    }
                    text_blocks.append({
                        'text': text,
                        'bbox': bbox,
                        'font_info': {'size': 12, 'name': 'unknown'},
                        'confidence': 0.5
                    })
                return text_blocks
            
            # Group characters into text blocks based on positioning and fonts
            grouped_blocks = self._group_chars_into_blocks(chars, page)
            
            for block in grouped_blocks:
                text_blocks.append({
                    'text': block['text'],
                    'bbox': block['bbox'],
                    'font_info': block['font_info'],
                    'confidence': block['confidence']
                })
        
        except Exception as e:
            self.logger.warning("Failed to extract detailed text blocks", error=str(e))
            # Fallback to simple text extraction
            try:
                text = page.extract_text()
                if text:
                    text_blocks.append({
                        'text': text,
                        'bbox': {'x0': 0, 'y0': 0, 'x1': page.width, 'y1': page.height},
                        'font_info': {'size': 12, 'name': 'fallback'},
                        'confidence': 0.3
                    })
            except:
                pass
        
        return text_blocks
    
    def _group_chars_into_blocks(self, chars: List[Dict], page) -> List[Dict[str, Any]]:
        """
        Group individual characters into meaningful text blocks
        """
        if not chars:
            return []
        
        # Sort characters by vertical position first, then horizontal
        sorted_chars = sorted(chars, key=lambda c: (c.get('top', 0), c.get('x0', 0)))
        
        blocks = []
        current_block = {
            'chars': [],
            'font_size': None,
            'font_name': None,
            'bbox': {'x0': float('inf'), 'y0': float('inf'), 'x1': 0, 'y1': 0}
        }
        
        line_threshold = 5  # pixels
        
        for char in sorted_chars:
            char_top = char.get('top', 0)
            char_bottom = char.get('bottom', 0) 
            char_size = char.get('size', 12)
            char_font = char.get('fontname', 'unknown')
            
            # Check if this character should start a new block
            should_start_new_block = (
                current_block['chars'] and (
                    # Different line (vertical gap)
                    abs(char_top - current_block['chars'][-1].get('top', 0)) > line_threshold or
                    # Significant font size change
                    (current_block['font_size'] and abs(char_size - current_block['font_size']) > 2) or
                    # Font name change
                    (current_block['font_name'] and char_font != current_block['font_name'])
                )
            )
            
            if should_start_new_block:
                # Finish current block
                if current_block['chars']:
                    blocks.append(self._finalize_block(current_block))
                
                # Start new block
                current_block = {
                    'chars': [char],
                    'font_size': char_size,
                    'font_name': char_font,
                    'bbox': {
                        'x0': char.get('x0', 0),
                        'y0': char.get('top', 0),
                        'x1': char.get('x1', 0),
                        'y1': char.get('bottom', 0)
                    }
                }
            else:
                # Add to current block
                current_block['chars'].append(char)
                if not current_block['font_size']:
                    current_block['font_size'] = char_size
                if not current_block['font_name']:
                    current_block['font_name'] = char_font
                
                # Update bounding box
                current_block['bbox']['x0'] = min(current_block['bbox']['x0'], char.get('x0', 0))
                current_block['bbox']['y0'] = min(current_block['bbox']['y0'], char.get('top', 0))
                current_block['bbox']['x1'] = max(current_block['bbox']['x1'], char.get('x1', 0))
                current_block['bbox']['y1'] = max(current_block['bbox']['y1'], char.get('bottom', 0))
        
        # Finish last block
        if current_block['chars']:
            blocks.append(self._finalize_block(current_block))
        
        return blocks
    
    def _finalize_block(self, block: Dict) -> Dict[str, Any]:
        """
        Convert character group into final text block
        """
        # Extract text from characters
        text = ''.join(char.get('text', '') for char in block['chars'])
        
        # Calculate confidence based on character extraction quality
        confidence = min(1.0, len([c for c in block['chars'] if c.get('text', '').strip()]) / max(1, len(block['chars'])))
        
        return {
            'text': text.strip(),
            'bbox': block['bbox'],
            'font_info': {
                'size': block['font_size'] or 12,
                'name': block['font_name'] or 'unknown',
                'bold': self._is_bold_font(block['font_name'] or ''),
            },
            'confidence': confidence,
            'char_count': len(block['chars'])
        }
    
    def _is_bold_font(self, font_name: str) -> bool:
        """
        Determine if font is bold based on font name
        """
        bold_indicators = ['bold', 'black', 'heavy', 'medium']
        return any(indicator in font_name.lower() for indicator in bold_indicators)
    
    def extract_images(self, page: pdfplumber.page.Page) -> List[Dict[str, Any]]:
        """
        Extract images from pdfplumber page with metadata
        """
        images = []
        
        try:
            page_images = page.images
            
            for i, img in enumerate(page_images):
                try:
                    # Extract basic image metadata
                    image_data = {
                        'id': f"img_p{page.page_number:03d}_{i:02d}",
                        'bbox': {
                            'x0': img.get('x0', 0),
                            'y0': img.get('y0', 0), 
                            'x1': img.get('x1', 0),
                            'y1': img.get('y1', 0)
                        },
                        'width': int(round(img.get('width', 0))),
                        'height': int(round(img.get('height', 0))),
                        'stream_object': img.get('stream'),
                        'confidence': 0.8
                    }
                    
                    # Try to extract actual image data
                    try:
                        # This is a simplified approach - in production would handle different image formats
                        image_obj = img.get('stream')
                        if hasattr(image_obj, 'get_data'):
                            raw_data = image_obj.get_data()
                            image_data['raw_data'] = base64.b64encode(raw_data).decode('utf-8')
                            image_data['file_size'] = len(raw_data)
                        else:
                            image_data['raw_data'] = None
                            image_data['file_size'] = 0
                    except Exception as img_extract_error:
                        self.logger.debug("Could not extract image data", error=str(img_extract_error))
                        image_data['raw_data'] = None
                        image_data['file_size'] = 0
                    
                    images.append(image_data)
                    
                except Exception as img_error:
                    self.logger.warning(f"Failed to process image {i}", error=str(img_error))
                    continue
        
        except Exception as e:
            self.logger.warning("Failed to extract images from page", error=str(e))
        
        return images
    
    def extract_table_of_contents(self, document: pdfplumber.PDF) -> List[Dict[str, Any]]:
        """
        Extract table of contents using pdfplumber
        """
        toc_entries = []
        
        try:
            # pdfplumber doesn't have direct TOC extraction, so we'll look for patterns
            # This is a simplified implementation - would be more sophisticated in production
            
            # Look at first few pages for TOC patterns
            toc_keywords = ['contents', 'table of contents', 'index']
            
            for page_num, page in enumerate(document.pages[:10]):  # Check first 10 pages
                text = page.extract_text() or ""
                text_lower = text.lower()
                
                # Look for TOC indicators
                if any(keyword in text_lower for keyword in toc_keywords):
                    # Try to extract TOC structure from this page
                    page_toc = self._extract_toc_from_page(page, text)
                    toc_entries.extend(page_toc)
                    
                    # Also check next page in case TOC continues
                    if page_num + 1 < len(document.pages):
                        next_page = document.pages[page_num + 1]
                        next_text = next_page.extract_text() or ""
                        next_toc = self._extract_toc_from_page(next_page, next_text)
                        toc_entries.extend(next_toc)
                    
                    break
        
        except Exception as e:
            self.logger.warning("Failed to extract TOC", error=str(e))
        
        return toc_entries
    
    def _extract_toc_from_page(self, page, text: str) -> List[Dict[str, Any]]:
        """
        Extract TOC entries from a page of text
        """
        import re
        
        toc_entries = []
        lines = text.split('\n')
        
        # Common TOC patterns
        patterns = [
            r'^(Chapter\s+\d+.*?)\s+(\d+)$',  # Chapter 1 Title ... 15
            r'^(\d+\.?\s+.*?)\s+(\d+)$',      # 1. Title ... 15
            r'^([A-Z][^.]*?)\s+(\d+)$',       # TITLE ... 15
        ]
        
        for line in lines:
            line = line.strip()
            if len(line) < 5:  # Skip very short lines
                continue
                
            for pattern in patterns:
                match = re.match(pattern, line)
                if match:
                    title = match.group(1).strip()
                    try:
                        page_num = int(match.group(2))
                        toc_entries.append({
                            'title': title,
                            'page': page_num,
                            'level': 1  # Would determine level more sophisticatedly
                        })
                    except ValueError:
                        continue
                    break
        
        return toc_entries
    
    def extract_metadata(self, document: pdfplumber.PDF) -> Dict[str, Any]:
        """
        Extract document metadata using pdfplumber
        """
        metadata = {}
        
        try:
            # pdfplumber provides access to PDF metadata
            pdf_metadata = document.metadata
            
            if pdf_metadata:
                metadata.update({
                    'title': pdf_metadata.get('Title', ''),
                    'author': pdf_metadata.get('Author', ''),
                    'subject': pdf_metadata.get('Subject', ''),
                    'creator': pdf_metadata.get('Creator', ''),
                    'producer': pdf_metadata.get('Producer', ''),
                    'creation_date': pdf_metadata.get('CreationDate', ''),
                    'modification_date': pdf_metadata.get('ModDate', ''),
                })
            
            # Add document statistics
            metadata.update({
                'page_count': len(document.pages),
                'engine': 'pdfplumber'
            })
        
        except Exception as e:
            self.logger.warning("Failed to extract metadata", error=str(e))
            metadata = {'engine': 'pdfplumber', 'page_count': len(document.pages)}
        
        return metadata
    
    def get_page_dimensions(self, page: pdfplumber.page.Page) -> Dict[str, float]:
        """
        Get page dimensions from pdfplumber page
        """
        return {
            "width": float(page.width),
            "height": float(page.height)
        }
    
    def extract_fonts(self, page: pdfplumber.page.Page) -> List[Dict[str, Any]]:
        """
        Extract font information from pdfplumber page
        """
        fonts = {}
        
        try:
            chars = page.chars
            
            for char in chars:
                font_name = char.get('fontname', 'unknown')
                font_size = char.get('size', 12)
                
                font_key = f"{font_name}_{font_size}"
                
                if font_key not in fonts:
                    fonts[font_key] = {
                        'name': font_name,
                        'size': font_size,
                        'bold': self._is_bold_font(font_name),
                        'usage_count': 0
                    }
                
                fonts[font_key]['usage_count'] += 1
        
        except Exception as e:
            self.logger.warning("Failed to extract font information", error=str(e))
        
        return list(fonts.values())