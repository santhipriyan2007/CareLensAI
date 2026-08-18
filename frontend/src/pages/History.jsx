import { useEffect, useState } from 'react'
import { api } from '../services/api'

function History({ onNavigate }) {
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    async function loadHistory() {
      try {
        const data = await api.getHistory()

        setHistory(
          Array.isArray(data)
            ? data
            : data.items || data.history || [],
        )
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    loadHistory()
  }, [])

  async function handleViewAnalysis(item) {
    try {
      setError('')

      const reportId =
        item.report_id ||
        item.id

      if (!reportId) {
        throw new Error(
          'Unable to open analysis: report ID is missing.',
        )
      }

      const data = await api.getAnalysis(reportId)

      onNavigate('analysis', {
        report: {
          id: reportId,
          file_name:
            item.report_name ||
            item.file_name ||
            item.filename,
        },
        analysis: data,
      })
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <section>
      <div className="page-heading">
        <div>
          <span className="eyebrow">CLINICAL RECORD</span>
          <h1>Analysis History</h1>
          <p>
            Review previous AI-assisted medical analyses.
          </p>
        </div>
      </div>

      {error && (
        <div className="error-box">
          {error}
        </div>
      )}

      <div className="panel">
        {loading ? (
          <div className="loading-state">
            Loading analysis history...
          </div>
        ) : history.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">◷</div>
            <h3>No analysis history</h3>
            <p>
              Completed analyses will appear here.
            </p>
          </div>
        ) : (
          <div className="history-table-wrapper">
            <table className="history-table">
              <thead>
                <tr>
                  <th>Report</th>
                  <th>Risk</th>
                  <th>Urgency</th>
                  <th>Confidence</th>
                  <th>Date</th>
                  <th></th>
                </tr>
              </thead>

              <tbody>
                {history.map((item, index) => {
                  const analysis =
                    item.analysis || item

                  return (
                    <tr key={item.id || index}>
                      <td>
                        <strong>
                          {item.report_name ||
                            item.file_name ||
                            item.filename ||
                            item.report_id ||
                            'Medical Report'}
                        </strong>
                      </td>

                      <td>
                        <span className="table-badge">
                          {analysis.risk_level || 'N/A'}
                        </span>
                      </td>

                      <td>
                        {analysis.urgency || 'N/A'}
                      </td>

                      <td>
                        {analysis.confidence_score != null
                          ? `${analysis.confidence_score}%`
                          : 'N/A'}
                      </td>

                      <td>
                        {item.analysis_date
                          ? new Date(
                              item.analysis_date,
                            ).toLocaleDateString()
                          : '—'}
                      </td>

                      <td>
                        <button
                          className="small-button"
                          onClick={() =>
                            handleViewAnalysis(item)
                          }
                        >
                          View
                        </button>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </section>
  )
}

export default History