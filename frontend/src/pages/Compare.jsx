import { useEffect, useState } from 'react'
import { api } from '../services/api'

function Compare() {
  const [reports, setReports] = useState([])
  const [previousId, setPreviousId] = useState('')
  const [currentId, setCurrentId] = useState('')
  const [comparison, setComparison] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    async function loadReports() {
      try {
        const data = await api.getReports()

        setReports(
          Array.isArray(data)
            ? data
            : data.reports || [],
        )
      } catch (err) {
        setError(err.message)
      }
    }

    loadReports()
  }, [])

  const compare = async () => {
    if (!previousId || !currentId) {
      setError('Select both reports.')
      return
    }

    if (previousId === currentId) {
      setError('Please select two different reports.')
      return
    }

    setLoading(true)
    setError('')

    try {
      const data = await api.compareReports(
        previousId,
        currentId,
      )

      setComparison(
        data.data ||
        data.comparison ||
        data,
      )
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <section>
      <div className="page-heading">
        <div>
          <span className="eyebrow">
            LONGITUDINAL ANALYSIS
          </span>
          <h1>Compare Reports</h1>
          <p>
            Compare two medical analyses to identify clinical trends.
          </p>
        </div>
      </div>

      <div className="panel compare-selector">
        <div className="compare-field">
          <label>
            Previous Report
            <select
              value={previousId}
              onChange={(e) =>
                setPreviousId(e.target.value)
              }
            >
              <option value="">
                Select previous report
              </option>

              {reports.map((report) => (
                <option
                  value={report.id}
                  key={report.id}
                >
                  {report.file_name ||
                    report.filename ||
                    report.id}
                </option>
              ))}
            </select>
          </label>
        </div>

        <div className="compare-arrow">→</div>

        <div className="compare-field">
          <label>
            Current Report
            <select
              value={currentId}
              onChange={(e) =>
                setCurrentId(e.target.value)
              }
            >
              <option value="">
                Select current report
              </option>

              {reports.map((report) => (
                <option
                  value={report.id}
                  key={report.id}
                >
                  {report.file_name ||
                    report.filename ||
                    report.id}
                </option>
              ))}
            </select>
          </label>
        </div>

        <button
          className="primary-button"
          onClick={compare}
          disabled={loading}
        >
          {loading
            ? 'Comparing...'
            : 'Compare'}
        </button>
      </div>

      {error && (
        <div className="error-box">
          {error}
        </div>
      )}

      {comparison && (
        <div className="comparison-result">
          <div className="comparison-banner">
            <span>Overall Trend</span>
            <strong>
              {comparison.overall_trend || 'N/A'}
            </strong>
          </div>

          <div className="comparison-grid">
            <CompareCard
              title="Risk Change"
              value={comparison.risk_change}
            />

            <CompareCard
              title="Urgency Change"
              value={comparison.urgency_change}
            />

            <CompareCard
              title="Confidence Change"
              value={comparison.confidence_change}
              type="confidence"
            />
          </div>

          <div className="panel">
            <div className="panel-header">
              <div>
                <h3>Abnormality Comparison</h3>
                <p>
                  Changes detected between the two reports.
                </p>
              </div>
            </div>

            {comparison.abnormality_comparison ? (
              <pre className="comparison-json">
                {JSON.stringify(
                  comparison.abnormality_comparison,
                  null,
                  2,
                )}
              </pre>
            ) : (
              <p className="muted">
                No abnormality comparison available.
              </p>
            )}
          </div>
        </div>
      )}
    </section>
  )
}

function CompareCard({
  title,
  value,
  type,
}) {
  let displayValue = 'N/A'

  if (type === 'confidence') {
    if (
      value &&
      typeof value === 'object'
    ) {
      const previous = value.previous
      const current = value.current
      const difference = value.difference

      if (
        previous != null &&
        current != null &&
        difference != null
      ) {
        const sign =
          difference > 0
            ? '+'
            : ''

        displayValue =
          `${previous}% → ${current}% (${sign}${difference}%)`
      }
    }
  } else if (
    value &&
    typeof value === 'object'
  ) {
    const previous = value.previous
    const current = value.current
    const change = value.change

    if (
      previous != null &&
      current != null &&
      change
    ) {
      displayValue =
        `${previous} → ${current} (${change})`
    }
  } else if (
    value != null
  ) {
    displayValue = String(value)
  }

  return (
    <div className="analysis-card">
      <span>{title}</span>
      <strong>{displayValue}</strong>
    </div>
  )
}

export default Compare