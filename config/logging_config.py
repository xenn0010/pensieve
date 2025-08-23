import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Dict, Any
import structlog
from datetime import datetime

from config.settings import settings


def setup_logging(log_level: str = "INFO", log_file: str = None) -> None:
    """Setup comprehensive logging configuration"""
    
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="ISO"),
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.ConsoleRenderer() if settings.debug else structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        logger_factory=structlog.WriteLoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    # Configure standard logging
    log_format = (
        "%(asctime)s | %(name)-25s | %(levelname)-8s | "
        "%(filename)s:%(lineno)d | %(message)s"
    )
    
    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level.upper()))
    console_formatter = logging.Formatter(log_format)
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # File handler for general logs
    if log_file is None:
        log_file = log_dir / f"pensieve_cio_{datetime.now().strftime('%Y%m%d')}.log"
    
    file_handler = logging.handlers.TimedRotatingFileHandler(
        log_file,
        when='midnight',
        interval=1,
        backupCount=30,  # Keep 30 days of logs
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(log_format)
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)
    
    # Error-only handler
    error_handler = logging.handlers.TimedRotatingFileHandler(
        log_dir / f"pensieve_cio_errors_{datetime.now().strftime('%Y%m%d')}.log",
        when='midnight',
        interval=1,
        backupCount=90,  # Keep error logs longer
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_formatter = logging.Formatter(
        "%(asctime)s | %(name)-25s | %(levelname)-8s | "
        "%(filename)s:%(lineno)d | %(funcName)s | %(message)s | "
        "%(exc_info)s"
    )
    error_handler.setFormatter(error_formatter)
    root_logger.addHandler(error_handler)
    
    # Set up component-specific loggers
    _setup_component_loggers(log_dir)
    
    # Reduce noise from third-party libraries
    _configure_third_party_loggers()
    
    # Log initial message
    logger = structlog.get_logger("pensieve.startup")
    logger.info("Logging system initialized", log_level=log_level, debug_mode=settings.debug)


def _setup_component_loggers(log_dir: Path) -> None:
    """Setup specialized loggers for different components"""
    
    components = {
        'decision_engine': 'decision_orchestrator',
        'event_processor': 'event_processor', 
        'brex_monitor': 'brex_financial_monitor',
        'pylon_intelligence': 'pylon_customer_intelligence',
        'sixtyfour_intelligence': 'sixtyfour_market_intelligence',
        'mixrank_intelligence': 'mixrank_technology_intelligence'
    }
    
    for component, logger_name in components.items():
        logger = logging.getLogger(logger_name)
        
        # Component-specific file handler
        handler = logging.handlers.TimedRotatingFileHandler(
            log_dir / f"{component}_{datetime.now().strftime('%Y%m%d')}.log",
            when='midnight',
            interval=1,
            backupCount=15,
            encoding='utf-8'
        )
        handler.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Don't propagate to root logger (avoid duplicate logs)
        logger.propagate = False


def _configure_third_party_loggers() -> None:
    """Configure third-party library loggers to reduce noise"""
    
    # Reduce verbosity of common libraries
    third_party_configs = {
        'httpx': logging.WARNING,
        'httpcore': logging.WARNING,
        'asyncio': logging.WARNING,
        'redis': logging.WARNING,
        'urllib3': logging.WARNING,
        'google.generativeai': logging.WARNING,
        'sqlalchemy': logging.WARNING,
        'celery': logging.INFO,
        'mcp': logging.INFO
    }
    
    for logger_name, level in third_party_configs.items():
        logging.getLogger(logger_name).setLevel(level)


def get_component_logger(component_name: str) -> structlog.BoundLogger:
    """Get a structured logger for a specific component"""
    return structlog.get_logger(f"pensieve.{component_name}")


class LoggingMixin:
    """Mixin class to add logging capabilities to any class"""
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.logger = get_component_logger(cls.__name__.lower())
    
    @property
    def logger(self) -> structlog.BoundLogger:
        """Get logger for this component"""
        return structlog.get_logger(f"pensieve.{self.__class__.__name__.lower()}")


def log_function_call(func_name: str, **kwargs) -> None:
    """Log function call with parameters"""
    logger = get_component_logger("function_calls")
    logger.info(f"Calling {func_name}", **kwargs)


def log_api_call(api_name: str, endpoint: str, method: str = "GET", **kwargs) -> None:
    """Log API calls"""
    logger = get_component_logger("api_calls")
    logger.info(
        f"API call to {api_name}",
        endpoint=endpoint,
        method=method,
        **kwargs
    )


def log_decision(decision_type: str, confidence: float, reasoning: str, **kwargs) -> None:
    """Log AI decisions"""
    logger = get_component_logger("ai_decisions")
    logger.info(
        f"AI Decision: {decision_type}",
        confidence=confidence,
        reasoning=reasoning,
        **kwargs
    )


def log_error_with_context(
    error: Exception, 
    context: Dict[str, Any] = None,
    component: str = "unknown"
) -> None:
    """Log errors with full context"""
    logger = get_component_logger(f"errors.{component}")
    
    error_context = {
        'error_type': type(error).__name__,
        'error_message': str(error),
        'component': component
    }
    
    if context:
        error_context.update(context)
    
    logger.error(
        f"Error in {component}",
        **error_context,
        exc_info=True
    )


def log_performance_metric(
    metric_name: str, 
    value: float, 
    unit: str = None,
    component: str = "system",
    **kwargs
) -> None:
    """Log performance metrics"""
    logger = get_component_logger(f"performance.{component}")
    logger.info(
        f"Performance Metric: {metric_name}",
        metric_name=metric_name,
        value=value,
        unit=unit,
        component=component,
        **kwargs
    )


def log_business_event(
    event_type: str,
    event_data: Dict[str, Any],
    priority: str = "medium",
    component: str = "business"
) -> None:
    """Log business events"""
    logger = get_component_logger(f"business.{component}")
    logger.info(
        f"Business Event: {event_type}",
        event_type=event_type,
        priority=priority,
        component=component,
        **event_data
    )


class ContextualLogger:
    """Logger that maintains context across related operations"""
    
    def __init__(self, component: str, operation_id: str = None):
        self.component = component
        self.operation_id = operation_id or datetime.now().isoformat()
        self.base_logger = get_component_logger(component)
        self.context = {
            'operation_id': self.operation_id,
            'component': self.component
        }
    
    def add_context(self, **kwargs):
        """Add context to all subsequent log messages"""
        self.context.update(kwargs)
    
    def info(self, message: str, **kwargs):
        """Log info message with context"""
        self.base_logger.info(message, **self.context, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message with context"""
        self.base_logger.warning(message, **self.context, **kwargs)
    
    def error(self, message: str, exc_info=None, **kwargs):
        """Log error message with context"""
        self.base_logger.error(message, exc_info=exc_info, **self.context, **kwargs)
    
    def debug(self, message: str, **kwargs):
        """Log debug message with context"""
        self.base_logger.debug(message, **self.context, **kwargs)


def create_operation_logger(component: str, operation_name: str) -> ContextualLogger:
    """Create a logger for a specific operation"""
    operation_id = f"{component}_{operation_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    return ContextualLogger(component, operation_id)


# Custom log filters
class SensitiveDataFilter(logging.Filter):
    """Filter to remove sensitive data from logs"""
    
    SENSITIVE_PATTERNS = [
        'api_key', 'password', 'token', 'secret', 'auth',
        'bearer', 'credential', 'key'
    ]
    
    def filter(self, record):
        """Filter sensitive data from log record"""
        if hasattr(record, 'args') and record.args:
            # Check if any args contain sensitive data
            filtered_args = []
            for arg in record.args:
                if isinstance(arg, (str, dict)):
                    arg_str = str(arg).lower()
                    if any(pattern in arg_str for pattern in self.SENSITIVE_PATTERNS):
                        filtered_args.append("[REDACTED]")
                    else:
                        filtered_args.append(arg)
                else:
                    filtered_args.append(arg)
            record.args = tuple(filtered_args)
        
        # Filter message content
        if hasattr(record, 'getMessage'):
            message = record.getMessage().lower()
            for pattern in self.SENSITIVE_PATTERNS:
                if pattern in message:
                    # Don't log if it contains sensitive patterns
                    return False
        
        return True


# Performance monitoring
class PerformanceLogger:
    """Logger for performance monitoring"""
    
    def __init__(self, component: str):
        self.component = component
        self.logger = get_component_logger(f"performance.{component}")
    
    def log_execution_time(self, operation: str, duration_ms: float, **kwargs):
        """Log operation execution time"""
        self.logger.info(
            f"Execution Time: {operation}",
            operation=operation,
            duration_ms=duration_ms,
            component=self.component,
            **kwargs
        )
    
    def log_memory_usage(self, operation: str, memory_mb: float, **kwargs):
        """Log memory usage"""
        self.logger.info(
            f"Memory Usage: {operation}",
            operation=operation,
            memory_mb=memory_mb,
            component=self.component,
            **kwargs
        )
    
    def log_api_latency(self, api_name: str, endpoint: str, latency_ms: float, **kwargs):
        """Log API call latency"""
        self.logger.info(
            f"API Latency: {api_name}",
            api_name=api_name,
            endpoint=endpoint,
            latency_ms=latency_ms,
            component=self.component,
            **kwargs
        )