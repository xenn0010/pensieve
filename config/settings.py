from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Core Application
    app_name: str = "Pensieve CIO"
    debug: bool = False
    
    # API Keys
    gemini_api_key: str
    brex_api_key: Optional[str] = None
# pylon_api_key removed - API not available
    sixtyfour_api_key: Optional[str] = None
    mixrank_api_key: Optional[str] = None
    
    # Database - Supabase
    supabase_url: str
    supabase_key: str
    supabase_service_key: Optional[str] = None
    redis_url: str = "redis://localhost:6379"
    
    # Event Processing
    max_concurrent_events: int = 50
    event_processing_interval: int = 30  # seconds
    
    # AI Configuration
    gemini_model: str = "gemini-pro"
    max_tokens: int = 4096
    temperature: float = 0.3
    
    # Risk Thresholds
    critical_cash_runway_days: int = 30
    high_churn_risk_threshold: float = 0.7
    competitor_threat_threshold: float = 0.8
    
    # Mock Data Configuration
    use_mock_data: bool = True
    demo_financial_profile: str = "healthy_saas"  # healthy_saas, cash_crunch_startup, post_funding_scale, seasonal_ecommerce
    
    class Config:
        env_file = ".env"


settings = Settings()