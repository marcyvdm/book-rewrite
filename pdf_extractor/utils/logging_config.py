"""
Structured logging configuration for PDF extraction
"""

import logging
import sys
from pathlib import Path
from typing import Optional
import structlog
from rich.console import Console
from rich.logging import RichHandler


def setup_logging(
    level: str = "INFO",
    log_file: Optional[Path] = None,
    console_output: bool = True,
    simple_format: bool = False,
) -> structlog.BoundLogger:
    """
    Set up structured logging with rich console output
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional file path for log output
        console_output: Whether to output to console
        simple_format: Use simple text formatting instead of rich
    
    Returns:
        Configured structured logger
    """
    
    # Configure stdlib logging
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(message)s",
        handlers=[]
    )
    
    handlers = []
    
    # Console handler with rich formatting
    if console_output:
        if simple_format:
            # Simple console handler for Windows compatibility
            console_handler = logging.StreamHandler(sys.stderr)
            console_handler.setFormatter(
                logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            )
            handlers.append(console_handler)
        else:
            console = Console(stderr=True, force_terminal=False, legacy_windows=True)
            rich_handler = RichHandler(
                console=console,
                show_time=True,
                show_path=False,
                markup=True,
                rich_tracebacks=False  # Disable rich tracebacks to avoid Unicode issues
            )
            handlers.append(rich_handler)
    
    # File handler if specified
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
        )
        handlers.append(file_handler)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    for handler in handlers:
        root_logger.addHandler(handler)
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="ISO"),
            (structlog.dev.ConsoleRenderer() if console_output and not simple_format 
             else structlog.processors.KeyValueRenderer()) if console_output 
            else structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, level.upper())
        ),
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    return structlog.get_logger("pdf_extractor")


# Create default logger instance
logger = setup_logging()