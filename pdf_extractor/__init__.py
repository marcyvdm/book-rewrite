"""
Intelligent PDF Extraction Library

A multi-algorithm PDF extraction system with AI enhancement capabilities.
"""

from .core import IntelligentPDFExtractor
from .models import ExtractionConfig, ExtractionResult

__version__ = "1.0.0"
__author__ = "Book Rewrite Project"

__all__ = [
    "IntelligentPDFExtractor",
    "ExtractionConfig", 
    "ExtractionResult",
]