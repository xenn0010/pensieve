"""SixtyFour API client wrapper extracted from the original notebook.

This keeps network logic in a reusable, testable module instead of a .ipynb cell.
Supports both synchronous and asynchronous (polling) modes for long-running jobs.
"""

from __future__ import annotations

import os
import json
import asyncio
import time
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

import requests
import aiohttp

from config.settings import settings
from config.logging_config import get_component_logger

logger = get_component_logger("sixtyfour_api_client")


API_BASE_URL = "https://api.sixtyfour.ai"


class JobStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing" 
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class SixtyFourJob:
    """Represents a SixtyFour intelligence job"""
    job_id: str
    status: JobStatus
    submitted_at: float
    completed_at: Optional[float] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class SixtyFourAPIError(RuntimeError):
    """Raised when SixtyFour API returns an error or unexpected payload."""


# Global job storage (in production, use Redis or database)
_active_jobs: Dict[str, SixtyFourJob] = {}


def submit_enrich_job(lead_info: Dict[str, Any], struct: Dict[str, Any]) -> str:
    """Submit an enrichment job without waiting for completion.
    
    Returns
    -------
    str
        Job ID for polling results later
    """
    import uuid
    job_id = str(uuid.uuid4())
    
    # Create job record
    job = SixtyFourJob(
        job_id=job_id,
        status=JobStatus.PENDING,
        submitted_at=time.time()
    )
    _active_jobs[job_id] = job
    
    # Submit job in background
    asyncio.create_task(_process_job_async(job_id, lead_info, struct))
    
    logger.info(f"Submitted SixtyFour job {job_id} for {lead_info.get('company', 'unknown')}")
    return job_id


async def _process_job_async(job_id: str, lead_info: Dict[str, Any], struct: Dict[str, Any]):
    """Process the job asynchronously"""
    job = _active_jobs[job_id]
    job.status = JobStatus.PROCESSING
    
    try:
        # Make the actual API call with no timeout
        result = await _make_async_api_call(lead_info, struct)
        
        # Update job with result
        job.status = JobStatus.COMPLETED
        job.completed_at = time.time()
        job.result = result
        
        logger.info(f"Job {job_id} completed successfully")
        
    except Exception as exc:
        job.status = JobStatus.FAILED
        job.error = str(exc)
        job.completed_at = time.time()
        
        logger.error(f"Job {job_id} failed: {exc}")


async def _make_async_api_call(lead_info: Dict[str, Any], struct: Dict[str, Any]) -> Dict[str, Any]:
    """Make the actual API call without timeout"""
    api_key = settings.sixtyfour_api_key or os.getenv("SIXTYFOUR_API_KEY")
    if not api_key:
        raise SixtyFourAPIError("SixtyFour API key not configured")

    payload = {
        "lead_info": lead_info,
        "struct": struct,
    }

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
    }

    url = f"{API_BASE_URL}/enrich-lead"
    logger.debug("Async POST %s payload=%s", url, json.dumps(payload, indent=2)[:500])

    async with aiohttp.ClientSession() as session:
        try:
            # No timeout - let it run as long as needed
            async with session.post(url, headers=headers, json=payload) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    raise SixtyFourAPIError(f"API error {resp.status}: {text[:300]}")
                
                body = await resp.json()
                return body.get("structured_data", {})
                
        except asyncio.TimeoutError:
            raise SixtyFourAPIError("Request timed out")
        except Exception as exc:
            raise SixtyFourAPIError(f"Network error: {exc}")


def get_job_status(job_id: str) -> SixtyFourJob:
    """Get the current status of a job"""
    if job_id not in _active_jobs:
        raise SixtyFourAPIError(f"Job {job_id} not found")
    
    return _active_jobs[job_id]


def get_job_result(job_id: str) -> Optional[Dict[str, Any]]:
    """Get job result if completed, None if still processing"""
    job = get_job_status(job_id)
    
    if job.status == JobStatus.COMPLETED:
        return job.result
    elif job.status == JobStatus.FAILED:
        raise SixtyFourAPIError(f"Job failed: {job.error}")
    else:
        return None  # Still processing


async def wait_for_job(job_id: str, poll_interval: float = 10.0) -> Dict[str, Any]:
    """Wait for a job to complete with polling"""
    logger.info(f"Waiting for job {job_id} (polling every {poll_interval}s)")
    
    while True:
        job = get_job_status(job_id)
        
        if job.status == JobStatus.COMPLETED:
            logger.info(f"Job {job_id} completed after {time.time() - job.submitted_at:.1f}s")
            return job.result
        elif job.status == JobStatus.FAILED:
            raise SixtyFourAPIError(f"Job failed: {job.error}")
        
        # Still processing, wait and check again
        await asyncio.sleep(poll_interval)


def enrich_lead(lead_info: Dict[str, Any], struct: Dict[str, Any]) -> Dict[str, Any]:
    """Legacy synchronous interface - now with longer timeout
    
    For new code, use submit_enrich_job() + wait_for_job() instead
    """
    api_key = settings.sixtyfour_api_key or os.getenv("SIXTYFOUR_API_KEY")
    if not api_key:
        raise SixtyFourAPIError("SixtyFour API key not configured")

    payload = {
        "lead_info": lead_info,
        "struct": struct,
    }

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
    }

    url = f"{API_BASE_URL}/enrich-lead"
    logger.debug("POST %s payload=%s", url, json.dumps(payload, indent=2)[:500])

    try:
        # Much longer timeout for deep intelligence (10 minutes)
        resp = requests.post(url, headers=headers, json=payload, timeout=600)
    except Exception as exc:
        logger.error("Network error while calling SixtyFour: %s", exc)
        raise SixtyFourAPIError(str(exc)) from exc

    if resp.status_code != 200:
        logger.error("SixtyFour API error status=%s body=%s", resp.status_code, resp.text[:300])
        raise SixtyFourAPIError(f"Unexpected status {resp.status_code}")

    try:
        body = resp.json()
    except ValueError as exc:
        logger.error("Invalid JSON in SixtyFour response: %s", resp.text[:300])
        raise SixtyFourAPIError("Invalid JSON response") from exc

    return body.get("structured_data", {})
