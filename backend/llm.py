"""
LLM integration using You.com API for reasoning.
"""
import os
import httpx
from typing import List, Optional

YOU_API_KEY = os.getenv("YOU_API_KEY", "")
YOU_API_URL = "https://api.you.com/v1/chat"


async def analyze_incident(
    logs: str,
    metrics: str = "",
    similar_incidents: List[dict] = None,
    attempted_fixes: List[dict] = None
) -> dict:
    """
    Analyze an incident using You.com LLM.
    Returns suspected root causes and suggested fixes.
    """
    similar_incidents = similar_incidents or []
    attempted_fixes = attempted_fixes or []

    # Build context from similar incidents
    similar_context = ""
    if similar_incidents:
        similar_context = "\n\n## Similar Past Incidents:\n"
        for i, incident in enumerate(similar_incidents, 1):
            similar_context += f"""
### Past Incident {i}:
- Logs: {incident.get('logs', 'N/A')[:500]}
- Root Causes Found: {', '.join(incident.get('suspected_root_causes', ['Unknown']))}
- Resolution: {incident.get('resolution_notes', 'N/A')}
- Fixes Applied: {', '.join([f.get('fix', '') for f in incident.get('attempted_fixes', [])])}
"""

    # Build context from attempted fixes
    fixes_context = ""
    if attempted_fixes:
        fixes_context = "\n\n## Already Attempted Fixes (did not fully resolve):\n"
        for fix in attempted_fixes:
            fixes_context += f"- {fix.get('fix', 'Unknown')}\n"

    prompt = f"""You are an autonomous incident analyst AI. Analyze the following system incident and provide actionable insights.

## Current Incident:
### Logs:
{logs}

### Metrics:
{metrics if metrics else 'No additional metrics provided'}
{similar_context}
{fixes_context}

Based on your analysis, provide:
1. **Suspected Root Causes**: List the most likely root causes (be specific)
2. **Suggested Fix**: Provide ONE specific, actionable fix to try next
3. **Confidence Level**: How confident are you in this diagnosis (low/medium/high)
4. **Explanation**: Brief explanation of your reasoning

Format your response as JSON:
{{
    "suspected_root_causes": ["cause1", "cause2"],
    "suggested_fix": "specific action to take",
    "confidence": "medium",
    "explanation": "your reasoning here"
}}
"""

    if not YOU_API_KEY:
        # Fallback response for demo/testing without API key
        return generate_fallback_analysis(logs, similar_incidents, attempted_fixes)

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                YOU_API_URL,
                headers={
                    "X-API-Key": YOU_API_KEY,
                    "Content-Type": "application/json"
                },
                json={
                    "query": prompt,
                    "chat_mode": "default"
                }
            )
            response.raise_for_status()
            data = response.json()

            # Parse the response
            answer = data.get("answer", "")
            return parse_llm_response(answer)

    except Exception as e:
        print(f"LLM API error: {e}")
        return generate_fallback_analysis(logs, similar_incidents, attempted_fixes)


def parse_llm_response(response: str) -> dict:
    """Parse LLM response to extract structured data."""
    import json
    import re

    # Try to extract JSON from response
    json_match = re.search(r'\{[^{}]*\}', response, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass

    # Fallback: create structured response from text
    return {
        "suspected_root_causes": ["Unable to parse - manual review needed"],
        "suggested_fix": response[:500] if response else "Review logs manually",
        "confidence": "low",
        "explanation": "Response could not be parsed into structured format"
    }


def generate_fallback_analysis(
    logs: str,
    similar_incidents: List[dict] = None,
    attempted_fixes: List[dict] = None
) -> dict:
    """Generate analysis without LLM API (for demo/testing)."""
    similar_incidents = similar_incidents or []
    attempted_fixes = attempted_fixes or []
    logs_lower = logs.lower()

    # Pattern-based analysis for common issues
    if "oomkilled" in logs_lower or "out of memory" in logs_lower:
        causes = ["Memory limit exceeded", "Memory leak in application", "Insufficient container resources"]
        fix = "Increase memory limits in deployment configuration or investigate memory leaks using profiling tools"
        confidence = "high"
    elif "connection refused" in logs_lower or "econnrefused" in logs_lower:
        causes = ["Target service is down", "Network policy blocking connection", "Incorrect service endpoint"]
        fix = "Check if target service is running and verify network policies allow the connection"
        confidence = "high"
    elif "timeout" in logs_lower:
        causes = ["Slow downstream service", "Network latency issues", "Resource contention"]
        fix = "Increase timeout values or investigate performance of downstream services"
        confidence = "medium"
    elif "permission denied" in logs_lower or "403" in logs_lower:
        causes = ["Missing IAM permissions", "Incorrect service account", "RBAC misconfiguration"]
        fix = "Review and update IAM/RBAC permissions for the affected service"
        confidence = "high"
    elif "crash" in logs_lower or "segfault" in logs_lower:
        causes = ["Application bug", "Null pointer exception", "Stack overflow"]
        fix = "Review recent code changes and check application logs for stack traces"
        confidence = "medium"
    elif "disk" in logs_lower or "storage" in logs_lower or "no space" in logs_lower:
        causes = ["Disk space exhausted", "Log files growing unbounded", "Large temporary files"]
        fix = "Clean up old logs and temporary files, consider increasing storage allocation"
        confidence = "high"
    else:
        causes = ["Unknown error pattern", "Requires manual investigation"]
        fix = "Review full logs and correlate with recent deployments or changes"
        confidence = "low"

    # Enhance with similar incident data
    if similar_incidents:
        past_causes = []
        for incident in similar_incidents:
            past_causes.extend(incident.get("suspected_root_causes", []))
        if past_causes:
            causes = list(set(causes + past_causes[:2]))

    # Adjust if fixes were already tried
    if attempted_fixes:
        fix = f"Previous fixes attempted. Next step: {fix}. Consider escalating if issue persists."

    return {
        "suspected_root_causes": causes,
        "suggested_fix": fix,
        "confidence": confidence,
        "explanation": f"Analysis based on pattern matching in logs. {'Found ' + str(len(similar_incidents)) + ' similar past incidents.' if similar_incidents else 'No similar incidents found.'}"
    }


async def evaluate_after_fix(
    incident: dict,
    new_logs: str = ""
) -> dict:
    """Evaluate incident state after a fix was applied."""
    logs = new_logs or incident.get("logs", "")
    attempted_fixes = incident.get("attempted_fixes", [])

    prompt = f"""An incident fix was just applied. Evaluate the current state.

## Original Logs:
{incident.get('logs', '')}

## Attempted Fixes:
{[f.get('fix') for f in attempted_fixes]}

## Current Logs (after fix):
{new_logs if new_logs else 'No new logs provided'}

Evaluate:
1. Did the fix likely resolve the issue?
2. Are there any remaining concerns?
3. What should be done next?

Respond in JSON:
{{
    "likely_resolved": true/false,
    "remaining_concerns": ["concern1"],
    "next_steps": "recommended action",
    "recommendation": "resolve" or "continue_investigating"
}}
"""

    if not YOU_API_KEY:
        # Fallback
        return {
            "likely_resolved": len(attempted_fixes) > 0,
            "remaining_concerns": [],
            "next_steps": "Monitor for recurrence" if len(attempted_fixes) > 0 else "Apply suggested fix",
            "recommendation": "resolve" if len(attempted_fixes) > 0 else "continue_investigating"
        }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                YOU_API_URL,
                headers={
                    "X-API-Key": YOU_API_KEY,
                    "Content-Type": "application/json"
                },
                json={
                    "query": prompt,
                    "chat_mode": "default"
                }
            )
            response.raise_for_status()
            data = response.json()
            return parse_llm_response(data.get("answer", ""))
    except Exception as e:
        print(f"LLM API error: {e}")
        return {
            "likely_resolved": False,
            "remaining_concerns": ["Could not evaluate - API error"],
            "next_steps": "Manual evaluation required",
            "recommendation": "continue_investigating"
        }
