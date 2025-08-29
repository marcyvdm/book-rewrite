"""
PDF Engine Factory for managing multiple extraction engines
"""

from typing import Dict, Type, List
from ..models import ExtractionConfig
from .base_engine import BasePDFEngine
from .pdfplumber_engine import PDFPlumberEngine
from .pypdf_engine import PyPDFEngine
from ..utils import logger


class PDFEngineFactory:
    """
    Factory class for creating and managing PDF extraction engines
    """
    
    # Registry of available engines
    _engines: Dict[str, Type[BasePDFEngine]] = {
        'pdfplumber': PDFPlumberEngine,
        'pypdf': PyPDFEngine,
    }
    
    def __init__(self, config: ExtractionConfig):
        self.config = config
        self.logger = logger.bind(component="PDFEngineFactory")
        
        # Cache for initialized engines
        self._engine_cache: Dict[str, BasePDFEngine] = {}
        
        # Validate engine availability
        self._validate_engines()
    
    def _validate_engines(self) -> None:
        """
        Validate that required engines are available
        """
        primary_engine = self.config.primary_engine
        fallback_engines = self.config.fallback_engines
        
        # Check primary engine
        if primary_engine not in self._engines:
            available_engines = list(self._engines.keys())
            raise ValueError(
                f"Primary engine '{primary_engine}' not available. "
                f"Available engines: {available_engines}"
            )
        
        # Check fallback engines
        for engine_name in fallback_engines:
            if engine_name not in self._engines:
                self.logger.warning(
                    "Fallback engine not available, removing from list",
                    engine=engine_name
                )
                fallback_engines.remove(engine_name)
        
        # Ensure we have at least one working engine
        all_engines = [primary_engine] + fallback_engines
        working_engines = []
        
        for engine_name in all_engines:
            if self._test_engine_availability(engine_name):
                working_engines.append(engine_name)
        
        if not working_engines:
            raise RuntimeError("No PDF extraction engines are available")
        
        self.logger.info(
            "PDF engines validated",
            primary=primary_engine,
            fallbacks=fallback_engines,
            working_engines=working_engines
        )
    
    def _test_engine_availability(self, engine_name: str) -> bool:
        """
        Test if an engine is available and can be initialized
        """
        try:
            engine_class = self._engines[engine_name]
            # Try to create instance
            engine = engine_class(self.config)
            return True
        except ImportError as e:
            self.logger.warning(
                "Engine dependencies not available",
                engine=engine_name,
                error=str(e)
            )
            return False
        except Exception as e:
            self.logger.error(
                "Engine initialization failed", 
                engine=engine_name,
                error=str(e)
            )
            return False
    
    def get_engine(self, engine_name: str) -> BasePDFEngine:
        """
        Get an engine instance by name
        
        Args:
            engine_name: Name of the engine to get
            
        Returns:
            Engine instance
            
        Raises:
            ValueError: If engine name is not recognized
            RuntimeError: If engine cannot be initialized
        """
        if engine_name not in self._engines:
            available_engines = list(self._engines.keys())
            raise ValueError(
                f"Engine '{engine_name}' not recognized. "
                f"Available engines: {available_engines}"
            )
        
        # Return cached instance if available
        if engine_name in self._engine_cache:
            return self._engine_cache[engine_name]
        
        # Create new instance
        try:
            engine_class = self._engines[engine_name]
            engine = engine_class(self.config)
            
            # Cache the instance
            self._engine_cache[engine_name] = engine
            
            self.logger.debug("Engine initialized", engine=engine_name)
            return engine
            
        except Exception as e:
            self.logger.error(
                "Failed to initialize engine",
                engine=engine_name,
                error=str(e)
            )
            raise RuntimeError(f"Cannot initialize engine '{engine_name}': {e}")
    
    def get_primary_engine(self) -> BasePDFEngine:
        """
        Get the primary engine instance
        
        Returns:
            Primary engine instance
        """
        return self.get_engine(self.config.primary_engine)
    
    def get_fallback_engines(self) -> List[BasePDFEngine]:
        """
        Get all fallback engine instances
        
        Returns:
            List of fallback engine instances
        """
        engines = []
        for engine_name in self.config.fallback_engines:
            try:
                engine = self.get_engine(engine_name)
                engines.append(engine)
            except Exception as e:
                self.logger.warning(
                    "Fallback engine not available",
                    engine=engine_name,
                    error=str(e)
                )
        
        return engines
    
    def get_available_engines(self) -> List[str]:
        """
        Get list of available engine names
        
        Returns:
            List of available engine names
        """
        available = []
        for engine_name in self._engines.keys():
            if self._test_engine_availability(engine_name):
                available.append(engine_name)
        
        return available
    
    def register_engine(self, name: str, engine_class: Type[BasePDFEngine]) -> None:
        """
        Register a new engine class
        
        Args:
            name: Engine name
            engine_class: Engine class that inherits from BasePDFEngine
        """
        if not issubclass(engine_class, BasePDFEngine):
            raise TypeError("Engine class must inherit from BasePDFEngine")
        
        self._engines[name] = engine_class
        self.logger.info("Engine registered", name=name)
    
    def clear_cache(self) -> None:
        """
        Clear the engine instance cache
        """
        self._engine_cache.clear()
        self.logger.debug("Engine cache cleared")