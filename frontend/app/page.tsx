'use client'

import { useState } from 'react'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface Analysis {
  incident_id: number
  status: string
  suspected_root_causes: string[]
  suggested_fix: string
  confidence: string
  explanation: string
  similar_incidents: Array<{
    id: number
    logs_preview: string
    resolution: string
    root_causes: string[]
  }>
  attempted_fixes: Array<{
    fix: string
    applied_at: string
  }>
}

interface ActionResult {
  incident_id: number
  status: string
  evaluation: {
    likely_resolved: boolean
    remaining_concerns: string[]
    next_steps: string
    recommendation: string
  }
  next_suggestion?: {
    suspected_root_causes: string[]
    suggested_fix: string
    confidence: string
    explanation: string
  }
}

export default function Home() {
  const [logs, setLogs] = useState('')
  const [metrics, setMetrics] = useState('')
  const [analysis, setAnalysis] = useState<Analysis | null>(null)
  const [actionResult, setActionResult] = useState<ActionResult | null>(null)
  const [fixInput, setFixInput] = useState('')
  const [newLogs, setNewLogs] = useState('')
  const [loading, setLoading] = useState(false)
  const [resolved, setResolved] = useState(false)
  const [error, setError] = useState('')

  const submitIncident = async () => {
    if (!logs.trim()) {
      setError('Please enter log data')
      return
    }

    setLoading(true)
    setError('')
    setAnalysis(null)
    setActionResult(null)
    setResolved(false)

    try {
      const response = await fetch(`${API_URL}/incident`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ logs, metrics }),
      })

      if (!response.ok) throw new Error('Failed to analyze incident')

      const data = await response.json()
      setAnalysis(data)
    } catch (err) {
      setError('Failed to connect to backend. Make sure the server is running.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const applyFix = async () => {
    if (!analysis || !fixInput.trim()) {
      setError('Please describe the fix you applied')
      return
    }

    setLoading(true)
    setError('')

    try {
      const response = await fetch(`${API_URL}/action`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          incident_id: analysis.incident_id,
          fix_applied: fixInput,
          new_logs: newLogs,
        }),
      })

      if (!response.ok) throw new Error('Failed to record action')

      const data = await response.json()
      setActionResult(data)
      setFixInput('')
      setNewLogs('')

      // Update analysis with new attempted fix
      setAnalysis(prev => prev ? {
        ...prev,
        attempted_fixes: [...prev.attempted_fixes, { fix: fixInput, applied_at: new Date().toISOString() }]
      } : null)
    } catch (err) {
      setError('Failed to record action')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const resolveIncident = async () => {
    if (!analysis) return

    setLoading(true)
    setError('')

    try {
      const response = await fetch(`${API_URL}/resolve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          incident_id: analysis.incident_id,
          resolution_notes: fixInput || 'Resolved via suggested fixes',
        }),
      })

      if (!response.ok) throw new Error('Failed to resolve incident')

      setResolved(true)
    } catch (err) {
      setError('Failed to resolve incident')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const resetForm = () => {
    setLogs('')
    setMetrics('')
    setAnalysis(null)
    setActionResult(null)
    setFixInput('')
    setNewLogs('')
    setResolved(false)
    setError('')
  }

  return (
    <div className="container">
      <header className="header">
        <h1>Autonomous Incident Analyst</h1>
        <p>AI-powered log analysis with stateful memory and continuous learning</p>
      </header>

      <div className="main-grid">
        {/* Left Panel - Input */}
        <div className="panel">
          <h2 className="panel-title">
            <span className="icon">📋</span>
            Submit Incident
          </h2>

          <div>
            <label className="analysis-label">System Logs</label>
            <textarea
              value={logs}
              onChange={(e) => setLogs(e.target.value)}
              placeholder="Paste your error logs here...&#10;&#10;Example:&#10;[ERROR] 2024-02-06 10:23:45 - Container killed: OOMKilled&#10;[ERROR] Memory usage exceeded limit: 512Mi&#10;[WARN] Pod restarting..."
              disabled={loading || !!analysis}
            />
          </div>

          <div>
            <label className="analysis-label">Additional Metrics (optional)</label>
            <textarea
              value={metrics}
              onChange={(e) => setMetrics(e.target.value)}
              placeholder="CPU: 85%&#10;Memory: 512Mi/512Mi&#10;Requests: 1500/min"
              style={{ minHeight: '100px' }}
              disabled={loading || !!analysis}
            />
          </div>

          {error && (
            <div style={{ color: 'var(--error)', marginBottom: '16px' }}>
              {error}
            </div>
          )}

          {!analysis ? (
            <button
              className="btn btn-primary"
              onClick={submitIncident}
              disabled={loading || !logs.trim()}
              style={{ width: '100%' }}
            >
              {loading ? 'Analyzing...' : 'Analyze Incident'}
            </button>
          ) : (
            <button
              className="btn btn-outline"
              onClick={resetForm}
              style={{ width: '100%' }}
            >
              Start New Analysis
            </button>
          )}
        </div>

        {/* Right Panel - Analysis */}
        <div className="panel">
          <h2 className="panel-title">
            <span className="icon">🤖</span>
            Agent Analysis
          </h2>

          {loading && !analysis && (
            <div className="loading">
              <div className="loading-spinner" />
              <span>Agent is analyzing the incident...</span>
            </div>
          )}

          {!analysis && !loading && (
            <div className="empty-state">
              <div className="empty-state-icon">🔍</div>
              <p>Submit logs to get AI-powered analysis</p>
            </div>
          )}

          {analysis && (
            <>
              {/* Status */}
              <div style={{ marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '12px' }}>
                <span className={`status-badge ${resolved ? 'status-resolved' : 'status-open'}`}>
                  {resolved ? '✓ Resolved' : '● Open'}
                </span>
                <span style={{ color: 'var(--text-secondary)' }}>
                  Incident #{analysis.incident_id}
                </span>
              </div>

              {resolved ? (
                <div className="analysis-card">
                  <div style={{ textAlign: 'center', padding: '20px' }}>
                    <div style={{ fontSize: '3rem', marginBottom: '16px' }}>✅</div>
                    <h3 style={{ marginBottom: '8px' }}>Incident Resolved</h3>
                    <p style={{ color: 'var(--text-secondary)' }}>
                      This incident has been stored in memory and will help improve future analysis.
                    </p>
                  </div>
                </div>
              ) : (
                <>
                  {/* Root Causes */}
                  <div className="analysis-card">
                    <div className="analysis-section">
                      <div className="analysis-label">Suspected Root Causes</div>
                      <ul className="root-causes">
                        {analysis.suspected_root_causes.map((cause, i) => (
                          <li key={i}>{cause}</li>
                        ))}
                      </ul>
                    </div>

                    <div className="analysis-section">
                      <div className="analysis-label">Suggested Fix</div>
                      <div className="suggested-fix">
                        {actionResult?.next_suggestion?.suggested_fix || analysis.suggested_fix}
                      </div>
                    </div>

                    <div className="analysis-section">
                      <div className="analysis-label">Confidence</div>
                      <span className={`confidence-badge confidence-${analysis.confidence}`}>
                        {analysis.confidence.toUpperCase()}
                      </span>
                    </div>

                    <div className="analysis-section">
                      <div className="analysis-label">Explanation</div>
                      <div className="analysis-value">{analysis.explanation}</div>
                    </div>
                  </div>

                  {/* Action Result */}
                  {actionResult && (
                    <div className="analysis-card" style={{ borderColor: 'var(--accent)' }}>
                      <div className="analysis-label">Agent Evaluation After Fix</div>
                      <div className="analysis-value" style={{ marginBottom: '12px' }}>
                        {actionResult.evaluation.next_steps}
                      </div>
                      {actionResult.evaluation.remaining_concerns.length > 0 && (
                        <div style={{ color: 'var(--warning)', fontSize: '0.9rem' }}>
                          ⚠️ Remaining concerns: {actionResult.evaluation.remaining_concerns.join(', ')}
                        </div>
                      )}
                    </div>
                  )}

                  {/* Similar Incidents */}
                  {analysis.similar_incidents.length > 0 && (
                    <div className="analysis-card">
                      <div className="analysis-label">Similar Past Incidents</div>
                      {analysis.similar_incidents.map((incident) => (
                        <div key={incident.id} className="similar-incident">
                          <div className="similar-incident-header">
                            <span className="similar-incident-id">Incident #{incident.id}</span>
                            <span className="status-badge status-resolved">Resolved</span>
                          </div>
                          <div className="similar-incident-preview">
                            {incident.logs_preview}
                          </div>
                          {incident.resolution && (
                            <div style={{ marginTop: '8px', fontSize: '0.9rem' }}>
                              <strong>Resolution:</strong> {incident.resolution}
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Attempted Fixes */}
                  {analysis.attempted_fixes.length > 0 && (
                    <div className="analysis-card">
                      <div className="analysis-label">Attempted Fixes</div>
                      {analysis.attempted_fixes.map((fix, i) => (
                        <div key={i} style={{ padding: '8px 0', borderBottom: '1px solid var(--border)' }}>
                          <div>{fix.fix}</div>
                          <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                            {new Date(fix.applied_at).toLocaleString()}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Fix Input */}
                  <div className="fix-input-section">
                    <div className="analysis-label">Apply a Fix</div>
                    <input
                      type="text"
                      value={fixInput}
                      onChange={(e) => setFixInput(e.target.value)}
                      placeholder="Describe the fix you applied..."
                    />
                    <input
                      type="text"
                      value={newLogs}
                      onChange={(e) => setNewLogs(e.target.value)}
                      placeholder="New logs after fix (optional)..."
                    />

                    <div className="action-buttons">
                      <button
                        className="btn btn-primary"
                        onClick={applyFix}
                        disabled={loading || !fixInput.trim()}
                      >
                        {loading ? 'Processing...' : 'Apply Fix & Re-evaluate'}
                      </button>
                      <button
                        className="btn btn-success"
                        onClick={resolveIncident}
                        disabled={loading}
                      >
                        Mark Resolved
                      </button>
                    </div>
                  </div>
                </>
              )}
            </>
          )}
        </div>
      </div>

      <div className="powered-by">
        Powered by <a href="https://you.com" target="_blank" rel="noopener noreferrer">You.com</a> •
        Deployed on <a href="https://render.com" target="_blank" rel="noopener noreferrer">Render</a> •
        Built for Continual Learning Hackathon 2025
      </div>
    </div>
  )
}
