import asyncio
import signal
import sys
from typing import Optional

from fastapi import FastAPI
from contextlib import asynccontextmanager

from intelligence_engine.decision_orchestrator import DecisionOrchestrator
from data_pipeline.event_processor import RealTimeEventProcessor
from mcp_servers.brex_mcp.financial_monitor import BrexFinancialMonitor
from mcp_servers.pylon_mcp.customer_intelligence import PylonCustomerIntelligence
from mcp_servers.sixtyfour_mcp.market_intelligence import SixtyFourMarketIntelligence
from mcp_servers.mixrank_mcp.technology_intelligence import MixRankTechnologyIntelligence
from config.settings import settings
from config.logging_config import setup_logging, get_component_logger, log_error_with_context
from config.supabase_client import supabase_client


class PensieveCIO:
    def __init__(self):
        self.logger = get_component_logger("pensieve_cio")
        self.decision_orchestrator = DecisionOrchestrator()
        self.event_processor = RealTimeEventProcessor(self.decision_orchestrator)
        self.brex_monitor = BrexFinancialMonitor()
        self.pylon_intelligence = PylonCustomerIntelligence()
        self.sixtyfour_intelligence = SixtyFourMarketIntelligence()
        self.mixrank_intelligence = MixRankTechnologyIntelligence()
        self.running = False
        
    async def initialize(self):
        """Initialize all components"""
        self.logger.info("Initializing Pensieve CIO autonomous intelligence system")
        
        try:
            # Initialize Supabase client first
            await supabase_client.initialize()
            self.logger.info("Supabase client initialized successfully")
            
            # Initialize event processor
            await self.event_processor.initialize()
            self.logger.info("Event processor initialized successfully")
            
            # Initialize all MCP servers
            if settings.brex_api_key:
                await self.brex_monitor.initialize()
                self.logger.info("Brex financial monitor initialized successfully")
            else:
                self.logger.warning("Brex API key not provided, skipping Brex monitor initialization")
            
            if settings.pylon_api_key:
                await self.pylon_intelligence.initialize()
                self.logger.info("Pylon customer intelligence initialized successfully")
            else:
                self.logger.warning("Pylon API key not provided, skipping Pylon intelligence initialization")
            
            if settings.sixtyfour_api_key:
                await self.sixtyfour_intelligence.initialize()
                self.logger.info("SixtyFour market intelligence initialized successfully")
            else:
                self.logger.warning("SixtyFour API key not provided, skipping SixtyFour intelligence initialization")
            
            if settings.mixrank_api_key:
                await self.mixrank_intelligence.initialize()
                self.logger.info("MixRank technology intelligence initialized successfully")
            else:
                self.logger.warning("MixRank API key not provided, skipping MixRank intelligence initialization")
            
            self.logger.info("Pensieve CIO initialization completed successfully")
            
        except Exception as e:
            log_error_with_context(e, {"component": "pensieve_cio", "operation": "initialization"}, "pensieve_cio")
            raise
        
    async def start(self):
        """Start the autonomous intelligence system"""
        self.running = True
        self.logger.info("Starting autonomous intelligence operations")
        
        try:
            # Start all monitoring and processing tasks
            tasks = [
                asyncio.create_task(self.decision_orchestrator.start_event_processing()),
                asyncio.create_task(self.event_processor.start_processing()),
            ]
            
            # Add MCP server monitoring tasks if API keys are available
            if settings.brex_api_key:
                tasks.append(asyncio.create_task(self.brex_monitor.start_monitoring()))
            
            if settings.pylon_api_key:
                tasks.append(asyncio.create_task(self.pylon_intelligence.start_monitoring()))
            
            if settings.sixtyfour_api_key:
                tasks.append(asyncio.create_task(self.sixtyfour_intelligence.start_monitoring()))
            
            if settings.mixrank_api_key:
                tasks.append(asyncio.create_task(self.mixrank_intelligence.start_monitoring()))
            
            self.logger.info(f"Started {len(tasks)} monitoring tasks")
            
            # Add graceful shutdown handler
            def signal_handler(signum, frame):
                self.logger.info("Received shutdown signal, initiating graceful shutdown")
                self.running = False
                for task in tasks:
                    task.cancel()
            
            signal.signal(signal.SIGINT, signal_handler)
            signal.signal(signal.SIGTERM, signal_handler)
            
            await asyncio.gather(*tasks, return_exceptions=True)
            
        except Exception as e:
            log_error_with_context(e, {"component": "pensieve_cio", "operation": "start"}, "pensieve_cio")
            raise
        finally:
            self.logger.info("Pensieve CIO shutdown complete")
    
    async def stop(self):
        """Stop the system gracefully"""
        self.running = False
        self.logger.info("Stopping Pensieve CIO")


# FastAPI app for health checks and monitoring
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup logging
    setup_logging("INFO" if not settings.debug else "DEBUG")
    logger = get_component_logger("fastapi")
    
    # Startup
    logger.info("Starting FastAPI application with Pensieve CIO")
    pensieve = PensieveCIO()
    
    try:
        await pensieve.initialize()
        
        # Store in app state
        app.state.pensieve = pensieve
        
        # Start background task
        background_task = asyncio.create_task(pensieve.start())
        app.state.background_task = background_task
        
        logger.info("FastAPI application startup completed")
        
        yield
        
    except Exception as e:
        log_error_with_context(e, {"component": "fastapi", "operation": "startup"}, "fastapi")
        raise
    finally:
        # Shutdown
        logger.info("Shutting down FastAPI application")
        await pensieve.stop()
        if hasattr(app.state, 'background_task'):
            app.state.background_task.cancel()
            try:
                await app.state.background_task
            except asyncio.CancelledError:
                pass
        logger.info("FastAPI application shutdown completed")

app = FastAPI(
    title="Pensieve CIO",
    description="Autonomous AI Chief Intelligence Officer",
    version="0.1.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {
        "service": "Pensieve CIO",
        "status": "running",
        "description": "Autonomous AI Chief Intelligence Officer for startups"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": asyncio.get_event_loop().time(),
        "components": {
            "decision_orchestrator": "active",
            "event_processor": "active", 
            "brex_monitor": "active"
        }
    }

@app.get("/metrics")
async def get_metrics():
    pensieve = app.state.pensieve
    
    # Get analytics from Supabase
    try:
        decision_analytics = await supabase_client.get_decision_analytics(hours_back=24)
        system_status = await supabase_client.get_system_status()
    except Exception as e:
        logger.error(f"Error getting Supabase metrics: {e}")
        decision_analytics = {}
        system_status = []
    
    return {
        "decision_analytics": decision_analytics,
        "system_components": system_status,
        "event_cache_size": len(pensieve.event_processor.event_cache) if pensieve.event_processor.event_cache else 0,
        "monitoring_status": "active" if hasattr(pensieve, 'brex_monitor') and pensieve.brex_monitor.monitoring_active else "inactive",
        "database_connected": supabase_client.initialized
    }

@app.get("/decisions")
async def get_recent_decisions(limit: int = 50):
    """Get recent AI decisions"""
    try:
        decisions = await supabase_client.get_decision_history(limit=limit)
        return {
            "decisions": decisions,
            "count": len(decisions)
        }
    except Exception as e:
        logger.error(f"Error getting decisions: {e}")
        return {"error": "Failed to retrieve decisions"}

@app.get("/events")
async def get_recent_events(limit: int = 50, priority: str = None):
    """Get recent business events"""
    try:
        events = await supabase_client.get_business_events(limit=limit, priority=priority)
        return {
            "events": events,
            "count": len(events)
        }
    except Exception as e:
        logger.error(f"Error getting events: {e}")
        return {"error": "Failed to retrieve events"}

@app.get("/system-status")
async def get_system_status():
    """Get detailed system status"""
    try:
        system_status = await supabase_client.get_system_status()
        return {
            "components": system_status,
            "overall_health": "healthy" if all(c.get('status') == 'healthy' for c in system_status) else "degraded"
        }
    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        return {"error": "Failed to retrieve system status"}


async def main():
    """Run Pensieve CIO in standalone mode"""
    # Setup logging first
    setup_logging("INFO" if not settings.debug else "DEBUG")
    logger = get_component_logger("main")
    
    # Check required environment variables
    if not settings.gemini_api_key:
        logger.error("GEMINI_API_KEY environment variable is required")
        sys.exit(1)
    
    logger.info("Starting Pensieve CIO - Autonomous AI Chief Intelligence Officer")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"AI Model: {settings.gemini_model}")
    
    pensieve = PensieveCIO()
    
    try:
        await pensieve.initialize()
        await pensieve.start()
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down")
        await pensieve.stop()
    except Exception as e:
        log_error_with_context(e, {"component": "main", "operation": "startup"}, "main")
        await pensieve.stop()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())