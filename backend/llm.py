"""
LLM integration using You.com Search API for intelligent incident analysis.
"""
import os
import re
from typing import List

# API Configuration
YOU_API_KEY = os.getenv("YOU_API_KEY", "ydc-sk-5ea85544c02a05f9-GJov23rQ0SbPwYTZ4G19krtAkJRMmFVG-8047ba4b")
YOU_SEARCH_URL = "https://ydc-index.io/v1/search"


def extract_error_keywords(logs: str) -> List[str]:
    """Extract key error terms from logs for searching."""
    keywords = []
    logs_lower = logs.lower()

    patterns = [
        (r'oomkilled|out of memory', 'OOMKilled kubernetes memory limit'),
        (r'econnrefused|connection refused', 'ECONNREFUSED connection refused fix'),
        (r'timeout', 'request timeout troubleshooting'),
        (r'permission denied|403|401', 'permission denied kubernetes RBAC'),
        (r'crash|segfault', 'application crash debug'),
        (r'disk|storage|no space', 'disk space full kubernetes'),
        (r'crashloopbackoff', 'CrashLoopBackOff kubernetes debug'),
        (r'imagepullbackoff', 'ImagePullBackOff kubernetes fix'),
    ]

    for pattern, search_term in patterns:
        if re.search(pattern, logs_lower):
            keywords.append(search_term)

    return keywords[:2]


async def search_you_com(query: str) -> dict:
    """Search You.com for relevant information."""
    import httpx

    if not YOU_API_KEY:
        return {"results": {}}

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                YOU_SEARCH_URL,
                headers={"X-API-Key": YOU_API_KEY},
                params={"query": query}
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        print(f"You.com Search error: {e}")
        return {"results": {}}


def extract_insights_from_search(search_results: dict) -> dict:
    """Extract actionable insights from You.com search results."""
    insights = {"snippets": [], "sources": []}

    results = search_results.get("results", {})
    hits = results.get("web", []) if isinstance(results, dict) else []

    for hit in hits[:5]:
        title = hit.get("title", "")
        description = hit.get("description", "")
        snippets = hit.get("snippets", [])
        url = hit.get("url", "")

        if snippets:
            insights["snippets"].extend(snippets[:2])
        elif description:
            insights["snippets"].append(description)

        if url:
            insights["sources"].append({"title": title, "url": url})

    return insights


async def analyze_incident(
    logs: str,
    metrics: str = "",
    similar_incidents: List[dict] = None,
    attempted_fixes: List[dict] = None
) -> dict:
    """Analyze an incident using You.com Search API for context."""
    similar_incidents = similar_incidents or []
    attempted_fixes = attempted_fixes or []

    # Step 1: Search You.com for context
    search_insights = {"snippets": [], "sources": []}
    keywords = extract_error_keywords(logs)

    if YOU_API_KEY and keywords:
        for keyword in keywords[:1]:  # Just one search to keep it fast
            results = await search_you_com(keyword)
            new_insights = extract_insights_from_search(results)
            search_insights["snippets"].extend(new_insights["snippets"])
            search_insights["sources"].extend(new_insights["sources"])

    # Step 2: Pattern-based analysis
    analysis = generate_pattern_analysis(logs, similar_incidents, attempted_fixes)

    # Step 3: Enhance with search results
    if search_insights["snippets"]:
        context = " ".join(search_insights["snippets"][:2])[:300]
        analysis["explanation"] = f"Web-enhanced analysis. {analysis['explanation']} Context: {context}"
        analysis["web_sources"] = search_insights["sources"][:3]

    analysis["powered_by"] = "You.com Search API" if YOU_API_KEY else "Pattern matching"
    return analysis


def generate_pattern_analysis(
    logs: str,
    similar_incidents: List[dict] = None,
    attempted_fixes: List[dict] = None
) -> dict:
    """Generate analysis using pattern matching."""
    similar_incidents = similar_incidents or []
    attempted_fixes = attempted_fixes or []
    logs_lower = logs.lower()

    if "oomkilled" in logs_lower or "out of memory" in logs_lower:
        causes = ["Memory limit exceeded", "Memory leak in application"]
        fix = "Increase memory limits or investigate memory leaks"
        confidence = "high"
    elif "connection refused" in logs_lower or "econnrefused" in logs_lower:
        causes = ["Target service is down", "Network policy blocking"]
        fix = "Check if target service is running"
        confidence = "high"
    elif "timeout" in logs_lower:
        causes = ["Slow downstream service", "Network latency"]
        fix = "Increase timeout or investigate slow services"
        confidence = "medium"
    elif "crashloopbackoff" in logs_lower:
        causes = ["Application failing to start", "Configuration error"]
        fix = "Check pod logs with kubectl logs"
        confidence = "high"
    elif "imagepullbackoff" in logs_lower:
        causes = ["Invalid image name", "Missing credentials"]
        fix = "Verify image name and imagePullSecrets"
        confidence = "high"
    else:
        causes = ["Unknown error", "Requires investigation"]
        fix = "Review full logs"
        confidence = "low"

    # Add context from similar incidents
    if similar_incidents:
        for inc in similar_incidents[:1]:
            if inc.get("resolution_notes"):
                fix = f"{fix}. Past fix: {inc['resolution_notes']}"

    explanation = f"Pattern analysis. Found {len(similar_incidents)} similar incidents."

    return {
        "suspected_root_causes": causes,
        "suggested_fix": fix,
        "confidence": confidence,
        "explanation": explanation,
        "web_sources": []
    }


async def evaluate_after_fix(incident: dict, new_logs: str = "") -> dict:
    """Evaluate incident after fix."""
    attempted_fixes = incident.get("attempted_fixes", [])

    if new_logs and "error" not in new_logs.lower():
        return {
            "likely_resolved": True,
            "remaining_concerns": [],
            "next_steps": "Monitor for recurrence",
            "recommendation": "resolve"
        }

    return {
        "likely_resolved": len(attempted_fixes) > 0,
        "remaining_concerns": [] if attempted_fixes else ["No fix applied yet"],
        "next_steps": "Apply suggested fix" if not attempted_fixes else "Monitor",
        "recommendation": "resolve" if attempted_fixes else "continue_investigating"
    }
