"""SixtyFour API client wrapper extracted from the original notebook.

This keeps network logic in a reusable, testable module instead of a .ipynb cell.
"""

from __future__ import annotations

import os
import json
from typing import Dict, Any

import requests

from config.settings import settings
from config.logging_config import get_component_logger

logger = get_component_logger("sixtyfour_api_client")


API_BASE_URL = "https://api.sixtyfour.ai"


class SixtyFourAPIError(RuntimeError):
    """Raised when SixtyFour API returns an error or unexpected payload."""


def enrich_lead(lead_info: Dict[str, Any], struct: Dict[str, Any]) -> Dict[str, Any]:
    """Enrich a lead using SixtyFour's `/enrich-lead` endpoint.

    Parameters
    ----------
    lead_info : dict
        Example: `{ "company": "Acme Corp", "research_depth": "maximum", "intelligence_type": "customers" }`
    struct : dict
        Deep-intelligence structure describing what attributes to return.

    Returns
    -------
    dict
        Parsed `structured_data` object from SixtyFour.

    Raises
    ------
    SixtyFourAPIError
        If the request fails or the response payload is invalid.
    """

    api_key = settings.sixtyfour_api_key or os.getenv("SIXTYFOUR_API_KEY")
    if not api_key:
        raise SixtyFourAPIError("SixtyFour API key not configured (env SIXTYFOUR_API_KEY or settings.sixtyfour_api_key)")

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
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
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
