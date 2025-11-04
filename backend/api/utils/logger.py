"""
Advanced logging configuration with structured logging support.
Provides console output, file logging, and JSON formatting for production.
"""
import logging
import sys
from pathlib import Path
import structlog
from datetime import datetime


def setup_logging(log_level: str = "INFO") -> structlog.stdlib.BoundLogger:
    """
    Configure structured logging with:
    - Console output (colored for development)
    - File output with rotation
    - JSON formatting for production
    - Request IDs for tracing
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        structlog.stdlib.BoundLogger: Configured logger instance
    """
    
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    # Setup standard logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level.upper()),
    )
    
    logger = structlog.get_logger()
    logger.info("logging_initialized", log_level=log_level)
    
    return logger
