import { useEffect, useState } from 'react'
import { api } from '../services/api'


function normalizeAnalysisResponse(data) {
  if (!data) {
    return null
  }

  /*
   * Backend response:
   *
   * {
   *   message: "...",
   *   analysis: {
   *     id: "...",
   *     report_id: "...",
   *     analysis: {
   *       clinical_summary: "...",
   *       risk_level: "...",
   *       ...
   *     },
   *     created_at: "..."
   *   }
   * }
   *
   * We want the innermost AI analysis object.
   */

  if (
    data.analysis?.analysis &&
    typeof data.analysis.analysis === 'object'
  ) {
    return data.analysis.analysis
  }

  /*
   * Supports the case where the API already returns
   * the actual AI analysis object directly.
   */
  if (
    data.analysis &&
    typeof data.analysis === 'object'
  ) {
    return data.analysis
  }

  /*
   * Fallback for APIs that may return:
   *
   * {
   *   data: {
   *     analysis: {
   *       ...
   *     }
   *   }
   * }
   */
  if (
    data.data?.analysis?.analysis &&
    typeof data.data.analysis.analysis === 'object'
  ) {
    return data.data.analysis.analysis
  }

  if (
    data.data?.analysis &&
    typeof data.data.analysis === 'object'
  ) {
    return data.data.analysis
  }

  return data
}


function Analysis({
  report,
  analysis: initialAnalysis,
  onNavigate,
}) {
  const [analysis, setAnalysis] = useState(
    normalizeAnalysisResponse(initialAnalysis)
  )

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')


  /*
   * Keep local analysis state synchronized when the
   * parent component changes the selected analysis.
   */
  useEffect(() => {
    setAnalysis(
      normalizeAnalysisResponse(initialAnalysis)
    )
  }, [initialAnalysis])


  const runAnalysis = async () => {
    if (!report?.id) {
      setError('No report selected.')
      return
    }

    setLoading(true)
    setError('')

    try {
      const data = await api.analyzeReport(report.id)

      const normalizedAnalysis =
        normalizeAnalysisResponse(data)

      setAnalysis(normalizedAnalysis)
    } catch (err) {
      setError(
        err?.message ||
        'Failed to analyze the medical report.'
      )
    } finally {
      setLoading(false)
    }
  }


  if (!report) {
    return (
      <div className="empty-state">
        <h2>No report selected</h2>

        <p>
          Select a report to begin analysis.
        </p>

        <button
          className="primary-button"
          onClick={() => onNavigate('reports')}
        >
          Go to Reports
        </button>
      </div>
    )
  }


  return (
    <section>
      <div className="page-heading">
        <div>
          <span className="eyebrow">
            AI MEDICAL ANALYSIS
          </span>

          <h1>
            {report.file_name ||
              report.filename ||
              'Medical Report'}
          </h1>

          <p>
            Report ID: {report.id}
          </p>
        </div>

        <button
          className="primary-button"
          onClick={runAnalysis}
          disabled={loading}
        >
          {loading
            ? 'Analyzing...'
            : '✦ Run AI Analysis'}
        </button>
      </div>


      {error && (
        <div className="error-box">
          {error}
        </div>
      )}


      {!analysis ? (
        <div className="analysis-empty">
          <div className="analysis-orb">
            ✦
          </div>

          <h2>
            Ready for AI analysis
          </h2>

          <p>
            CareLens will process the report through
            OCR and Gemini-powered clinical analysis.
          </p>

          <button
            className="primary-button"
            onClick={runAnalysis}
            disabled={loading}
          >
            {loading
              ? 'Processing report...'
              : 'Start Analysis'}
          </button>
        </div>
      ) : (
        <>
          {/* Summary Cards */}

          <div className="analysis-summary-grid">
            <div className="analysis-card">
              <span>
                Risk Level
              </span>

              <strong className="risk-value">
                {analysis.risk_level ||
                  'N/A'}
              </strong>
            </div>


            <div className="analysis-card">
              <span>
                Urgency
              </span>

              <strong>
                {analysis.urgency ||
                  'N/A'}
              </strong>
            </div>


            <div className="analysis-card">
              <span>
                Confidence
              </span>

              <strong>
                {analysis.confidence_score != null
                  ? `${analysis.confidence_score}%`
                  : 'N/A'}
              </strong>
            </div>
          </div>


          {/* Main Analysis Grid */}

          <div className="analysis-grid">

            {/* Clinical Summary */}

            <div className="panel">
              <div className="panel-header">
                <div>
                  <h3>
                    Clinical Summary
                  </h3>

                  <p>
                    AI-generated clinical interpretation.
                  </p>
                </div>
              </div>

              <p className="analysis-text">
                {analysis.clinical_summary ||
                  'No clinical summary available.'}
              </p>
            </div>


            {/* Key Findings */}

            <div className="panel">
              <div className="panel-header">
                <div>
                  <h3>
                    Key Findings
                  </h3>

                  <p>
                    Important observations from the report.
                  </p>
                </div>
              </div>

              <List
                items={analysis.key_findings}
              />
            </div>


            {/* Abnormal Findings */}

            <div className="panel">
              <div className="panel-header">
                <div>
                  <h3>
                    Abnormal Findings
                  </h3>

                  <p>
                    Potentially significant abnormalities.
                  </p>
                </div>
              </div>

              <AbnormalFindingsList
                items={analysis.abnormal_findings}
              />
            </div>


            {/* Possible Conditions */}

            <div className="panel">
              <div className="panel-header">
                <div>
                  <h3>
                    Possible Conditions
                  </h3>

                  <p>
                    AI-generated differential considerations.
                  </p>
                </div>
              </div>

              <List
                items={analysis.possible_conditions}
              />
            </div>


            {/* Red Flags */}

            <div className="panel">
              <div className="panel-header">
                <div>
                  <h3>
                    Red Flags
                  </h3>

                  <p>
                    Findings requiring clinical attention.
                  </p>
                </div>
              </div>

              <List
                items={analysis.red_flags}
                warning
              />
            </div>


            {/* Recommended Tests */}

            <div className="panel">
              <div className="panel-header">
                <div>
                  <h3>
                    Recommended Tests
                  </h3>

                  <p>
                    Potential follow-up investigations.
                  </p>
                </div>
              </div>

              <List
                items={analysis.recommended_tests}
              />
            </div>


            {/* Doctor Recommendations */}

            <div className="panel full-panel">
              <div className="panel-header">
                <div>
                  <h3>
                    Doctor Recommendations
                  </h3>

                  <p>
                    Clinical decision-support suggestions.
                  </p>
                </div>
              </div>

              <List
                items={analysis.doctor_recommendations}
              />
            </div>


            {/* Patient Explanation */}

            <div className="panel full-panel patient-panel">
              <div className="panel-header">
                <div>
                  <h3>
                    Patient Explanation
                  </h3>

                  <p>
                    Plain-language explanation of the findings.
                  </p>
                </div>
              </div>

              <p className="analysis-text">
                {analysis.patient_explanation ||
                  'No patient explanation available.'}
              </p>
            </div>

          </div>


          {/* Medical Disclaimer */}

          <div className="medical-disclaimer">
            <strong>
              Medical Disclaimer
            </strong>

            <p>
              {analysis.medical_disclaimer ||
                'CareLens AI provides clinical decision support and does not replace professional medical judgment.'}
            </p>
          </div>
        </>
      )}
    </section>
  )
}


/*
 * Generic list renderer.
 *
 * Handles:
 * - string[]
 * - simple objects
 */
function List({
  items,
  warning = false,
}) {
  if (
    !Array.isArray(items) ||
    items.length === 0
  ) {
    return (
      <p className="muted">
        No items identified.
      </p>
    )
  }


  return (
    <ul
      className={
        warning
          ? 'analysis-list warning'
          : 'analysis-list'
      }
    >
      {items.map((item, index) => (
        <li key={index}>
          <span>•</span>

          {typeof item === 'string'
            ? item
            : item.finding ||
              item.name ||
              item.description ||
              JSON.stringify(item)}
        </li>
      ))}
    </ul>
  )
}


/*
 * Specialized renderer for abnormal findings.
 *
 * Backend returns objects such as:
 *
 * {
 *   parameter: "HbA1c",
 *   value: "6.6%",
 *   reference_range: "<5.7",
 *   status: "High",
 *   clinical_significance: "..."
 * }
 */
function AbnormalFindingsList({
  items,
}) {
  if (
    !Array.isArray(items) ||
    items.length === 0
  ) {
    return (
      <p className="muted">
        No items identified.
      </p>
    )
  }


  return (
    <ul className="analysis-list">
      {items.map((item, index) => (
        <li key={index}>
          <span>•</span>

          <div>
            <strong>
              {item.parameter || 'Finding'}
            </strong>

            {item.value && (
              <div>
                Value: {item.value}
              </div>
            )}

            {item.reference_range && (
              <div>
                Reference: {item.reference_range}
              </div>
            )}

            {item.status && (
              <div>
                Status: {item.status}
              </div>
            )}

            {item.clinical_significance && (
              <div>
                {item.clinical_significance}
              </div>
            )}
          </div>
        </li>
      ))}
    </ul>
  )
}


export default Analysis