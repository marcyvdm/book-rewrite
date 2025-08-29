"""
PyPDF-based PDF extraction engine (fallback)
"""

import base64
from pathlib import Path
from typing import List, Dict, Any, ContextManager
from contextlib import contextmanager

try:
    import PyPDF2
except ImportError:
    raise ImportError("PyPDF2 is required. Install with: pip install PyPDF2")

from .base_engine import BasePDFEngine
from ..utils import logger


class PyPDFEngine(BasePDFEngine):
    """
    PDF extraction engine using PyPDF2 library (fallback engine)
    """
    
    def __init__(self, config):
        super().__init__(config)
        self.logger = logger.bind(component="PyPDFEngine")
    
    @contextmanager
    def open_pdf(self, pdf_path: Path) -> ContextManager[PyPDF2.PdfReader]:
        """
        Open PDF file using PyPDF2
        """
        self.logger.debug("Opening PDF with PyPDF2", path=str(pdf_path))
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                yield pdf_reader
        except Exception as e:
            self.logger.error("Failed to open PDF with PyPDF2", error=str(e))
            raise
    
    def extract_text_blocks(self, page: PyPDF2.PageObject) -> List[Dict[str, Any]]:
        """
        Extract text blocks from PyPDF2 page (limited positioning info)
        """
        text_blocks = []
        
        try:
            # PyPDF2 provides basic text extraction without detailed positioning
            text = page.extract_text()
            
            if text and text.strip():
                # Split into paragraphs based on double newlines
                paragraphs = text.split('\n\n')
                
                for i, paragraph in enumerate(paragraphs):
                    paragraph = paragraph.strip()
                    if paragraph:
                        # PyPDF2 doesn't provide positioning info, so we estimate
                        estimated_y = i * 50  # Rough estimation
                        
                        text_blocks.append({
                            'text': paragraph,
                            'bbox': {
                                'x0': 50,  # Estimated margins
                                'y0': estimated_y,
                                'x1': 550,  # Estimated page width
                                'y1': estimated_y + 40  # Estimated paragraph height
                            },
                            'font_info': {
                                'size': 12,  # Default size
                                'name': 'unknown',
                                'bold': False
                            },
                            'confidence': 0.6  # Lower confidence due to limited info
                        })
        
        except Exception as e:
            self.logger.warning("Failed to extract text with PyPDF2", error=str(e))
        
        return text_blocks
    
    def extract_images(self, page: PyPDF2.PageObject) -> List[Dict[str, Any]]:
        """
        Extract images from PyPDF2 page (basic support)
        """
        images = []
        
        try:
            # PyPDF2 has limited image extraction capabilities
            if '/XObject' in page['/Resources']:
                xobjects = page['/Resources']['/XObject'].get_object()
                
                for i, (obj_name, obj_ref) in enumerate(xobjects.items()):
                    try:
                        obj = obj_ref.get_object()
                        
                        if obj['/Subtype'] == '/Image':
                            # Basic image metadata
                            width = obj.get('/Width', 0)
                            height = obj.get('/Height', 0)
                            
                            image_data = {
                                'id': f"pypdf_img_{i}",
                                'bbox': {
                                    'x0': 0,
                                    'y0': 0,
                                    'x1': width,
                                    'y1': height
                                },
                                'width': width,
                                'height': height,
                                'raw_data': None,  # PyPDF2 image extraction is complex
                                'file_size': 0,
                                'confidence': 0.4  # Lower confidence for PyPDF2 images
                            }
                            
                            images.append(image_data)
                    
                    except Exception as img_error:
                        self.logger.debug(f"Failed to process image {i} with PyPDF2", error=str(img_error))
                        continue
        
        except Exception as e:
            self.logger.debug("No images found with PyPDF2", error=str(e))
        
        return images
    
    def extract_table_of_contents(self, document: PyPDF2.PdfReader) -> List[Dict[str, Any]]:
        """
        Extract table of contents using PyPDF2
        """
        toc_entries = []
        
        try:
            # PyPDF2 can access PDF outline/bookmarks
            outlines = document.outline
            
            if outlines:
                toc_entries = self._process_outline_items(outlines)
        
        except Exception as e:
            self.logger.debug("No TOC found with PyPDF2", error=str(e))
        
        return toc_entries
    
    def _process_outline_items(self, items: List, level: int = 1) -> List[Dict[str, Any]]:
        """
        Recursively process PDF outline items
        """
        toc_entries = []
        
        for item in items:
            if isinstance(item, dict):
                # This is a destination
                continue
            elif hasattr(item, 'title'):
                # This is an outline item
                entry = {
                    'title': item.title,
                    'level': level
                }
                
                # Try to get page number
                try:
                    if hasattr(item, 'page') and item.page:
                        # Page number extraction from PyPDF2 destination
                        entry['page'] = item.page.idnum if hasattr(item.page, 'idnum') else 1
                    else:
                        entry['page'] = None
                except:
                    entry['page'] = None
                
                toc_entries.append(entry)
            
            elif isinstance(item, list):
                # Nested outline items
                nested_entries = self._process_outline_items(item, level + 1)
                toc_entries.extend(nested_entries)
        
        return toc_entries
    
    def extract_metadata(self, document: PyPDF2.PdfReader) -> Dict[str, Any]:
        """
        Extract document metadata using PyPDF2
        """
        metadata = {'engine': 'pypdf'}
        
        try:
            # PyPDF2 metadata extraction
            pdf_metadata = document.metadata
            
            if pdf_metadata:
                metadata.update({
                    'title': pdf_metadata.get('/Title', ''),
                    'author': pdf_metadata.get('/Author', ''),
                    'subject': pdf_metadata.get('/Subject', ''),
                    'creator': pdf_metadata.get('/Creator', ''),
                    'producer': pdf_metadata.get('/Producer', ''),
                    'creation_date': str(pdf_metadata.get('/CreationDate', '')),
                    'modification_date': str(pdf_metadata.get('/ModDate', '')),
                })
            
            # Add page count
            metadata['page_count'] = len(document.pages)
        
        except Exception as e:
            self.logger.warning("Failed to extract metadata with PyPDF2", error=str(e))
            metadata['page_count'] = 0
        
        return metadata
    
    def get_page_dimensions(self, page: PyPDF2.PageObject) -> Dict[str, float]:
        """
        Get page dimensions from PyPDF2 page
        """
        try:
            mediabox = page.mediabox
            return {
                "width": float(mediabox.width),
                "height": float(mediabox.height)
            }
        except:
            return {"width": 612.0, "height": 792.0}  # Default letter size
    
    def extract_fonts(self, page: PyPDF2.PageObject) -> List[Dict[str, Any]]:
        """
        Extract font information from PyPDF2 page (limited support)
        """
        fonts = []
        
        try:
            # PyPDF2 has limited font extraction capabilities
            if '/Font' in page.get('/Resources', {}):
                font_resources = page['/Resources']['/Font']
                
                for font_name, font_ref in font_resources.items():
                    try:
                        font_obj = font_ref.get_object()
                        
                        font_info = {
                            'name': font_name,
                            'base_font': font_obj.get('/BaseFont', 'unknown'),
                            'subtype': font_obj.get('/Subtype', 'unknown'),
                            'size': 12,  # PyPDF2 doesn't provide size info easily
                            'bold': 'Bold' in str(font_obj.get('/BaseFont', '')),
                            'usage_count': 1  # Can't determine actual usage with PyPDF2
                        }
                        
                        fonts.append(font_info)
                    
                    except Exception as font_error:
                        self.logger.debug(f"Failed to process font {font_name}", error=str(font_error))
                        continue
        
        except Exception as e:
            self.logger.debug("Failed to extract fonts with PyPDF2", error=str(e))
        
        return fonts