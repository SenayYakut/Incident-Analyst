"""
Autonomous Incident Analyst - FastAPI Backend
Stateful AI agent for log analysis and incident resolution.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import memory
import llm

app = FastAPI(
    title="Autonomous Incident Analyst",
    description="Stateful AI agent for incident analysis and resolution",
    version="1.0.0"
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class IncidentRequest(BaseModel):
    logs: str
    metrics: Optional[str] = ""


class ActionRequest(BaseModel):
    incident_id: int
    fix_applied: str
    new_logs: Optional[str] = ""


class ResolveRequest(BaseModel):
    incident_id: int
    resolution_notes: Optional[str] = ""


class IncidentResponse(BaseModel):
    incident_id: int
    status: str
    suspected_root_causes: List[str]
    suggested_fix: str
    confidence: str
    explanation: str
    similar_incidents: List[dict]
    attempted_fixes: List[dict]
    web_sources: List[dict] = []
    powered_by: str = ""


class ActionResponse(BaseModel):
    incident_id: int
    status: str
    evaluation: dict
    next_suggestion: Optional[dict] = None


class ResolveResponse(BaseModel):
    incident_id: int
    status: str
    message: str


# Endpoints
@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Autonomous Incident Analyst"}


@app.get("/incidents")
async def list_incidents():
    """List all incidents."""
    incidents = memory.load_incidents()
    return {"incidents": incidents, "total": len(incidents)}


@app.get("/incidents/{incident_id}")
async def get_incident(incident_id: int):
    """Get a specific incident."""
    incident = memory.get_incident(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident


@app.post("/incident", response_model=IncidentResponse)
async def submit_incident(request: IncidentRequest):
    """
    Submit logs for analysis.
    Creates a new incident and provides AI-powered analysis.
    """
    # Find similar past incidents for context
    similar_incidents = memory.find_similar_incidents(request.logs)

    # Create new incident
    incident = memory.create_incident(request.logs, request.metrics)

    # Analyze with LLM
    analysis = await llm.analyze_incident(
        logs=request.logs,
        metrics=request.metrics,
        similar_incidents=similar_incidents
    )

    # Update incident with analysis
    memory.update_incident(incident["id"], {
        "suspected_root_causes": analysis.get("suspected_root_causes", [])
    })

    return IncidentResponse(
        incident_id=incident["id"],
        status=incident["status"],
        suspected_root_causes=analysis.get("suspected_root_causes", []),
        suggested_fix=analysis.get("suggested_fix", ""),
        confidence=analysis.get("confidence", "low"),
        explanation=analysis.get("explanation", ""),
        similar_incidents=[
            {
                "id": s.get("id"),
                "logs_preview": s.get("logs", "")[:200],
                "resolution": s.get("resolution_notes", ""),
                "root_causes": s.get("suspected_root_causes", [])
            }
            for s in similar_incidents
        ],
        attempted_fixes=[],
        web_sources=analysis.get("web_sources", []),
        powered_by=analysis.get("powered_by", "")
    )


@app.post("/action", response_model=ActionResponse)
async def apply_action(request: ActionRequest):
    """
    Record an applied fix and re-evaluate the incident.
    Updates state and provides next-step suggestions.
    """
    incident = memory.get_incident(request.incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    if incident["status"] == "resolved":
        raise HTTPException(status_code=400, detail="Incident already resolved")

    # Record the attempted fix
    updated_incident = memory.add_attempted_fix(request.incident_id, request.fix_applied)

    # Evaluate state after fix
    evaluation = await llm.evaluate_after_fix(updated_incident, request.new_logs)

    # If still needs investigation, provide next suggestion
    next_suggestion = None
    if evaluation.get("recommendation") == "continue_investigating":
        similar_incidents = memory.find_similar_incidents(incident["logs"])
        next_suggestion = await llm.analyze_incident(
            logs=request.new_logs or incident["logs"],
            metrics=incident.get("metrics", ""),
            similar_incidents=similar_incidents,
            attempted_fixes=updated_incident.get("attempted_fixes", [])
        )

    return ActionResponse(
        incident_id=request.incident_id,
        status=updated_incident["status"],
        evaluation=evaluation,
        next_suggestion=next_suggestion
    )


@app.post("/resolve", response_model=ResolveResponse)
async def resolve_incident(request: ResolveRequest):
    """
    Mark an incident as resolved.
    Stores the resolution in memory for future reference.
    """
    incident = memory.get_incident(request.incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    if incident["status"] == "resolved":
        return ResolveResponse(
            incident_id=request.incident_id,
            status="resolved",
            message="Incident was already resolved"
        )

    # Resolve the incident
    memory.resolve_incident(request.incident_id, request.resolution_notes)

    return ResolveResponse(
        incident_id=request.incident_id,
        status="resolved",
        message="Incident resolved and stored in memory for future reference"
    )


@app.delete("/incidents/{incident_id}")
async def delete_incident(incident_id: int):
    """Delete an incident (for testing/cleanup)."""
    incidents = memory.load_incidents()
    incidents = [i for i in incidents if i["id"] != incident_id]
    memory.save_incidents(incidents)
    return {"message": f"Incident {incident_id} deleted"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
