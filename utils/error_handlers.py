import asyncio
import functools
import inspect
from typing import Any, Callable, Dict, Optional, Type, Union
from datetime import datetime
import traceback

from config.logging_config import log_error_with_context, get_component_logger


class PensieveError(Exception):
    """Base exception for Pensieve CIO errors"""
    
    def __init__(self, message: str, component: str = None, context: Dict[str, Any] = None):
        self.message = message
        self.component = component or "unknown"
        self.context = context or {}
        self.timestamp = datetime.now()
        super().__init__(self.message)


class APIError(PensieveError):
    """Error for API-related failures"""
    
    def __init__(self, message: str, api_name: str, status_code: int = None, 
                 response_data: Any = None, **kwargs):
        self.api_name = api_name
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(message, component=f"{api_name}_api", context=kwargs)


class DecisionError(PensieveError):
    """Error for AI decision-making failures"""
    
    def __init__(self, message: str, decision_type: str = None, 
                 confidence: float = None, **kwargs):
        self.decision_type = decision_type
        self.confidence = confidence
        super().__init__(message, component="decision_engine", context=kwargs)


class DataProcessingError(PensieveError):
    """Error for data processing failures"""
    
    def __init__(self, message: str, data_source: str = None, 
                 processing_stage: str = None, **kwargs):
        self.data_source = data_source
        self.processing_stage = processing_stage
        super().__init__(message, component="data_processing", context=kwargs)


class ConfigurationError(PensieveError):
    """Error for configuration-related failures"""
    
    def __init__(self, message: str, config_key: str = None, **kwargs):
        self.config_key = config_key
        super().__init__(message, component="configuration", context=kwargs)


def handle_errors(
    retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,),
    default_return: Any = None,
    log_errors: bool = True,
    reraise: bool = True
):
    """
    Decorator for comprehensive error handling with retry logic
    
    Args:
        retries: Number of retry attempts
        delay: Initial delay between retries (seconds)
        backoff: Backoff multiplier for delay
        exceptions: Tuple of exceptions to catch and retry
        default_return: Value to return if all retries fail and reraise=False
        log_errors: Whether to log errors
        reraise: Whether to reraise the exception after all retries fail
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            last_exception = None
            current_delay = delay
            
            # Get component name from function or class
            component_name = _get_component_name(func, args)
            
            for attempt in range(retries + 1):
                try:
                    if inspect.iscoroutinefunction(func):
                        return await func(*args, **kwargs)
                    else:
                        return func(*args, **kwargs)
                        
                except exceptions as e:
                    last_exception = e
                    
                    if log_errors:
                        error_context = {
                            'function': func.__name__,
                            'attempt': attempt + 1,
                            'max_attempts': retries + 1,
                            'args_count': len(args),
                            'kwargs_keys': list(kwargs.keys())
                        }
                        
                        # Add specific error context based on exception type
                        if isinstance(e, PensieveError):
                            error_context.update(e.context)
                            error_context['pensieve_error_type'] = type(e).__name__
                        
                        log_error_with_context(
                            e, 
                            error_context, 
                            component_name
                        )
                    
                    # If this was the last attempt, decide whether to reraise or return default
                    if attempt == retries:
                        if reraise:
                            raise
                        else:
                            return default_return
                    
                    # Wait before retrying
                    if attempt < retries:
                        await asyncio.sleep(current_delay)
                        current_delay *= backoff
            
            # This should never be reached, but just in case
            if reraise and last_exception:
                raise last_exception
            return default_return
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            last_exception = None
            current_delay = delay
            
            # Get component name from function or class
            component_name = _get_component_name(func, args)
            
            for attempt in range(retries + 1):
                try:
                    return func(*args, **kwargs)
                        
                except exceptions as e:
                    last_exception = e
                    
                    if log_errors:
                        error_context = {
                            'function': func.__name__,
                            'attempt': attempt + 1,
                            'max_attempts': retries + 1,
                            'args_count': len(args),
                            'kwargs_keys': list(kwargs.keys())
                        }
                        
                        # Add specific error context based on exception type
                        if isinstance(e, PensieveError):
                            error_context.update(e.context)
                            error_context['pensieve_error_type'] = type(e).__name__
                        
                        log_error_with_context(
                            e, 
                            error_context, 
                            component_name
                        )
                    
                    # If this was the last attempt, decide whether to reraise or return default
                    if attempt == retries:
                        if reraise:
                            raise
                        else:
                            return default_return
                    
                    # Wait before retrying (for sync functions, use time.sleep)
                    if attempt < retries:
                        import time
                        time.sleep(current_delay)
                        current_delay *= backoff
            
            # This should never be reached, but just in case
            if reraise and last_exception:
                raise last_exception
            return default_return
        
        # Return the appropriate wrapper based on whether the function is async
        if inspect.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


def _get_component_name(func: Callable, args: tuple) -> str:
    """Extract component name from function or class instance"""
    # Try to get from class instance (first arg for methods)
    if args and hasattr(args[0], '__class__'):
        class_name = args[0].__class__.__name__.lower()
        return class_name
    
    # Try to get from module name
    if hasattr(func, '__module__'):
        module_parts = func.__module__.split('.')
        if len(module_parts) > 1:
            return module_parts[-1]
    
    # Fallback to function name
    return func.__name__


def api_error_handler(api_name: str):
    """Decorator specifically for API calls"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                # Convert generic exceptions to APIError
                if not isinstance(e, APIError):
                    # Try to extract HTTP status and response data
                    status_code = getattr(e, 'status_code', None)
                    response_data = getattr(e, 'response', None)
                    
                    raise APIError(
                        message=f"API call to {api_name} failed: {str(e)}",
                        api_name=api_name,
                        status_code=status_code,
                        response_data=response_data,
                        original_error=str(e),
                        original_error_type=type(e).__name__
                    )
                raise
        return wrapper
    return decorator


def decision_error_handler(decision_type: str):
    """Decorator specifically for AI decision-making functions"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if not isinstance(e, DecisionError):
                    # Try to extract confidence from kwargs or result
                    confidence = kwargs.get('confidence', None)
                    
                    raise DecisionError(
                        message=f"Decision making failed for {decision_type}: {str(e)}",
                        decision_type=decision_type,
                        confidence=confidence,
                        original_error=str(e),
                        original_error_type=type(e).__name__
                    )
                raise
        return wrapper
    return decorator


class CircuitBreaker:
    """Circuit breaker pattern implementation for external service calls"""
    
    def __init__(
        self,
        failure_threshold: int = 5,
        timeout: float = 60.0,
        success_threshold: int = 3
    ):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.success_threshold = success_threshold
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
        self.logger = get_component_logger("circuit_breaker")
    
    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            if self.state == 'OPEN':
                if self._should_attempt_reset():
                    self.state = 'HALF_OPEN'
                    self.logger.info(f"Circuit breaker half-open for {func.__name__}")
                else:
                    raise APIError(
                        message=f"Circuit breaker OPEN for {func.__name__}",
                        api_name=func.__name__,
                        context={'circuit_breaker_state': self.state}
                    )
            
            try:
                result = await func(*args, **kwargs)
                self._on_success()
                return result
                
            except Exception as e:
                self._on_failure()
                raise
        
        return wrapper
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset"""
        if self.last_failure_time is None:
            return True
        
        time_since_failure = datetime.now().timestamp() - self.last_failure_time
        return time_since_failure >= self.timeout
    
    def _on_success(self):
        """Handle successful call"""
        self.failure_count = 0
        
        if self.state == 'HALF_OPEN':
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.state = 'CLOSED'
                self.success_count = 0
                self.logger.info("Circuit breaker reset to CLOSED")
    
    def _on_failure(self):
        """Handle failed call"""
        self.failure_count += 1
        self.last_failure_time = datetime.now().timestamp()
        
        if self.failure_count >= self.failure_threshold:
            self.state = 'OPEN'
            self.success_count = 0
            self.logger.warning(f"Circuit breaker OPEN after {self.failure_count} failures")


class ErrorRecoveryManager:
    """Manager for error recovery strategies"""
    
    def __init__(self):
        self.recovery_strategies = {}
        self.logger = get_component_logger("error_recovery")
    
    def register_strategy(
        self,
        error_type: Type[Exception],
        strategy: Callable[[Exception], Any]
    ):
        """Register a recovery strategy for a specific error type"""
        self.recovery_strategies[error_type] = strategy
    
    async def attempt_recovery(self, error: Exception, context: Dict[str, Any] = None):
        """Attempt to recover from an error using registered strategies"""
        error_type = type(error)
        
        # Look for exact match first
        if error_type in self.recovery_strategies:
            strategy = self.recovery_strategies[error_type]
            self.logger.info(f"Attempting recovery for {error_type.__name__}")
            return await self._execute_strategy(strategy, error, context)
        
        # Look for parent class matches
        for registered_type, strategy in self.recovery_strategies.items():
            if isinstance(error, registered_type):
                self.logger.info(f"Attempting recovery for {error_type.__name__} using {registered_type.__name__} strategy")
                return await self._execute_strategy(strategy, error, context)
        
        self.logger.warning(f"No recovery strategy found for {error_type.__name__}")
        return None
    
    async def _execute_strategy(
        self,
        strategy: Callable,
        error: Exception,
        context: Dict[str, Any]
    ):
        """Execute a recovery strategy"""
        try:
            if inspect.iscoroutinefunction(strategy):
                return await strategy(error, context)
            else:
                return strategy(error, context)
        except Exception as e:
            self.logger.error(f"Recovery strategy failed: {e}")
            return None


# Global error recovery manager instance
error_recovery_manager = ErrorRecoveryManager()


def register_recovery_strategy(error_type: Type[Exception]):
    """Decorator to register error recovery strategies"""
    def decorator(func: Callable) -> Callable:
        error_recovery_manager.register_strategy(error_type, func)
        return func
    return decorator


# Built-in recovery strategies
@register_recovery_strategy(APIError)
async def api_error_recovery(error: APIError, context: Dict[str, Any] = None):
    """Recovery strategy for API errors"""
    logger = get_component_logger("recovery.api")
    
    # For API errors, we might want to:
    # 1. Switch to backup API endpoint
    # 2. Use cached data
    # 3. Degrade functionality gracefully
    
    logger.info(f"Attempting API error recovery for {error.api_name}")
    
    if error.status_code == 429:  # Rate limiting
        # Wait and suggest retry with exponential backoff
        return {
            'recovery_action': 'retry_with_backoff',
            'suggested_delay': 60,
            'max_retries': 3
        }
    elif error.status_code in [500, 502, 503, 504]:  # Server errors
        # Suggest fallback to cached data or degraded mode
        return {
            'recovery_action': 'use_cached_data',
            'degraded_mode': True
        }
    elif error.status_code == 401:  # Authentication error
        # Suggest credential refresh
        return {
            'recovery_action': 'refresh_credentials',
            'component': error.api_name
        }
    
    return None


@register_recovery_strategy(DecisionError)
async def decision_error_recovery(error: DecisionError, context: Dict[str, Any] = None):
    """Recovery strategy for AI decision errors"""
    logger = get_component_logger("recovery.decision")
    
    logger.info(f"Attempting decision error recovery for {error.decision_type}")
    
    # For decision errors, we might:
    # 1. Fall back to simpler decision logic
    # 2. Use default conservative decisions
    # 3. Alert human operators
    
    return {
        'recovery_action': 'use_fallback_decision',
        'decision_type': error.decision_type,
        'confidence': 0.3,  # Low confidence fallback
        'alert_required': True
    }


def safe_execute(func: Callable, *args, **kwargs):
    """
    Safely execute a function with comprehensive error handling
    Returns tuple: (success: bool, result: Any, error: Exception)
    """
    try:
        if inspect.iscoroutinefunction(func):
            # For async functions, return a coroutine that handles the execution
            async def async_safe_execute():
                try:
                    result = await func(*args, **kwargs)
                    return True, result, None
                except Exception as e:
                    return False, None, e
            return async_safe_execute()
        else:
            result = func(*args, **kwargs)
            return True, result, None
    except Exception as e:
        return False, None, e