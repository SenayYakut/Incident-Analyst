"""
Incident memory storage and retrieval.
Simulates RAG behavior with simple string similarity matching.
"""
import json
import os
from datetime import datetime
from typing import List, Optional
from difflib import SequenceMatcher

MEMORY_FILE = "incidents.json"


def load_incidents() -> List[dict]:
    """Load all incidents from memory file."""
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def save_incidents(incidents: List[dict]) -> None:
    """Save incidents to memory file."""
    with open(MEMORY_FILE, "w") as f:
        json.dump(incidents, f, indent=2, default=str)


def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate string similarity between two texts."""
    return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()


def find_similar_incidents(logs: str, top_k: int = 3) -> List[dict]:
    """Find similar past incidents based on log content."""
    incidents = load_incidents()
    resolved_incidents = [i for i in incidents if i.get("status") == "resolved"]

    if not resolved_incidents:
        return []

    # Calculate similarity scores
    scored = []
    for incident in resolved_incidents:
        similarity = calculate_similarity(logs, incident.get("logs", ""))
        if similarity > 0.1:  # Minimum threshold
            scored.append((similarity, incident))

    # Sort by similarity and return top_k
    scored.sort(key=lambda x: x[0], reverse=True)
    return [incident for _, incident in scored[:top_k]]


def create_incident(logs: str, metrics: str = "") -> dict:
    """Create a new incident."""
    incidents = load_incidents()

    incident = {
        "id": len(incidents) + 1,
        "logs": logs,
        "metrics": metrics,
        "suspected_root_causes": [],
        "attempted_fixes": [],
        "status": "open",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "resolution_notes": ""
    }

    incidents.append(incident)
    save_incidents(incidents)
    return incident


def get_incident(incident_id: int) -> Optional[dict]:
    """Get incident by ID."""
    incidents = load_incidents()
    for incident in incidents:
        if incident["id"] == incident_id:
            return incident
    return None


def update_incident(incident_id: int, updates: dict) -> Optional[dict]:
    """Update an incident."""
    incidents = load_incidents()
    for i, incident in enumerate(incidents):
        if incident["id"] == incident_id:
            incidents[i].update(updates)
            incidents[i]["updated_at"] = datetime.now().isoformat()
            save_incidents(incidents)
            return incidents[i]
    return None


def add_attempted_fix(incident_id: int, fix: str) -> Optional[dict]:
    """Add an attempted fix to an incident."""
    incident = get_incident(incident_id)
    if not incident:
        return None

    attempted_fixes = incident.get("attempted_fixes", [])
    attempted_fixes.append({
        "fix": fix,
        "applied_at": datetime.now().isoformat()
    })

    return update_incident(incident_id, {"attempted_fixes": attempted_fixes})


def resolve_incident(incident_id: int, resolution_notes: str = "") -> Optional[dict]:
    """Mark an incident as resolved."""
    return update_incident(incident_id, {
        "status": "resolved",
        "resolution_notes": resolution_notes
    })
