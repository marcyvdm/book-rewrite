"""
Base PDF engine interface
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict, Any, ContextManager
from contextlib import contextmanager


class BasePDFEngine(ABC):
    """
    Abstract base class for PDF extraction engines
    """
    
    def __init__(self, config):
        self.config = config
        self.name = self.__class__.__name__
    
    @abstractmethod
    @contextmanager
    def open_pdf(self, pdf_path: Path) -> ContextManager[Any]:
        """
        Open PDF file and return document object
        
        Args:
            pdf_path: Path to PDF file
            
        Yields:
            PDF document object
        """
        pass
    
    @abstractmethod
    def extract_text_blocks(self, page) -> List[Dict[str, Any]]:
        """
        Extract text blocks from a page with positioning information
        
        Args:
            page: Page object from PDF document
            
        Returns:
            List of text blocks with content and positioning data
        """
        pass
    
    @abstractmethod
    def extract_images(self, page) -> List[Dict[str, Any]]:
        """
        Extract images from a page with metadata
        
        Args:
            page: Page object from PDF document
            
        Returns:
            List of image data with positioning and metadata
        """
        pass
    
    @abstractmethod
    def extract_table_of_contents(self, document) -> List[Dict[str, Any]]:
        """
        Extract table of contents from PDF document
        
        Args:
            document: PDF document object
            
        Returns:
            List of TOC entries with titles and page numbers
        """
        pass
    
    @abstractmethod
    def extract_metadata(self, document) -> Dict[str, Any]:
        """
        Extract document metadata
        
        Args:
            document: PDF document object
            
        Returns:
            Dictionary of metadata fields
        """
        pass
    
    def get_page_dimensions(self, page) -> Dict[str, float]:
        """
        Get page dimensions
        
        Args:
            page: Page object
            
        Returns:
            Dictionary with width and height
        """
        return {"width": 0.0, "height": 0.0}
    
    def extract_fonts(self, page) -> List[Dict[str, Any]]:
        """
        Extract font information from page
        
        Args:
            page: Page object
            
        Returns:
            List of font information
        """
        return []