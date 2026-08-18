import { useEffect, useState } from 'react'
import {
  Bar,
  BarChart,
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { api } from '../services/api'

function Dashboard({ onNavigate }) {
  const [reports, setReports] = useState([])
  const [history, setHistory] = useState([])
  const [analytics, setAnalytics] = useState(null)
  const [riskDistribution, setRiskDistribution] = useState([])
  const [trends, setTrends] = useState([])
  const [loading, setLoading] = useState(true)
  const [analyticsError, setAnalyticsError] = useState('')

  useEffect(() => {
    async function loadDashboard() {
      try {
        const [
          reportsData,
          historyData,
          overviewData,
          riskData,
          trendsData,
        ] = await Promise.all([
          api.getReports(),
          api.getHistory(),
          api.getAnalyticsOverview(),
          api.getRiskDistribution(),
          api.getAnalyticsTrends(),
        ])

        setReports(
          Array.isArray(reportsData)
            ? reportsData
            : reportsData.reports || [],
        )

        setHistory(
          Array.isArray(historyData)
            ? historyData
            : historyData.items || historyData.history || [],
        )

        setAnalytics(overviewData)

        setRiskDistribution(
          riskData.distribution || [],
        )

        setTrends(
          trendsData.trends || [],
        )
      } catch (error) {
        console.error('Dashboard loading error:', error)
        setAnalyticsError(error.message)
      } finally {
        setLoading(false)
      }
    }

    loadDashboard()
  }, [])

  return (
    <section>
      <div className="page-heading">
        <div>
          <span className="eyebrow">OVERVIEW</span>
          <h1>Clinical Dashboard</h1>
          <p>
            Monitor medical reports and AI-assisted clinical insights.
          </p>
        </div>

        <button
          className="primary-button"
          onClick={() => onNavigate('reports')}
        >
          + Upload Report
        </button>
      </div>

      {analyticsError && (
        <div className="error-box">
          Analytics data could not be loaded: {analyticsError}
        </div>
      )}

      <div className="stats-grid">
        <div className="stat-card">
          <span className="stat-icon blue">▣</span>
          <div>
            <span>Total Reports</span>
            <strong>
              {loading
                ? '—'
                : analytics?.total_reports ?? reports.length}
            </strong>
          </div>
        </div>

        <div className="stat-card">
          <span className="stat-icon green">✓</span>
          <div>
            <span>AI Analyses</span>
            <strong>
              {loading
                ? '—'
                : analytics?.total_analyses ?? history.length}
            </strong>
          </div>
        </div>

        <div className="stat-card">
          <span className="stat-icon purple">✦</span>
          <div>
            <span>Total Patients</span>
            <strong>
              {loading
                ? '—'
                : analytics?.total_patients ?? '—'}
            </strong>
          </div>
        </div>

        <div className="stat-card">
          <span className="stat-icon orange">◷</span>
          <div>
            <span>Abnormal Reports</span>
            <strong>
              {loading
                ? '—'
                : analytics?.abnormal_reports ?? '—'}
            </strong>
          </div>
        </div>
      </div>

      <div className="dashboard-grid">
        <div className="panel">
          <div className="panel-header">
            <div>
              <h3>Recent Reports</h3>
              <p>Your latest uploaded medical reports.</p>
            </div>

            <button
              className="text-button"
              onClick={() => onNavigate('reports')}
            >
              View all →
            </button>
          </div>

          {reports.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">▣</div>
              <h3>No reports yet</h3>
              <p>
                Upload your first medical report to begin.
              </p>
              <button
                className="primary-button"
                onClick={() => onNavigate('reports')}
              >
                Upload Report
              </button>
            </div>
          ) : (
            <div className="report-list">
              {reports.slice(0, 5).map((report) => (
                <div
                  className="report-row"
                  key={report.id}
                >
                  <div className="file-icon">PDF</div>

                  <div className="report-info">
                    <strong>
                      {report.file_name ||
                        report.filename ||
                        'Medical Report'}
                    </strong>

                    <span>
                      {report.created_at
                        ? new Date(
                            report.created_at,
                          ).toLocaleDateString()
                        : 'Recently uploaded'}
                    </span>
                  </div>

                  <button
                    className="small-button"
                    onClick={() =>
                      onNavigate('analysis', { report })
                    }
                  >
                    Analyze
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="panel insight-panel">
          <span className="insight-label">
            CARELENS INTELLIGENCE
          </span>

          <h2>AI-assisted clinical reasoning</h2>

          <p>
            CareLens combines OCR, Gemini AI and
            retrieval-augmented generation to turn
            medical reports into structured clinical
            insights.
          </p>

          <div className="feature-list">
            <div>
              <span>✓</span>
              Structured AI analysis
            </div>

            <div>
              <span>✓</span>
              Abnormal finding detection
            </div>

            <div>
              <span>✓</span>
              Report comparison
            </div>

            <div>
              <span>✓</span>
              RAG-powered medical knowledge
            </div>
          </div>
        </div>
      </div>

      <div className="analytics-grid">
        <div className="panel analytics-panel">
          <div className="panel-header">
            <div>
              <h3>Risk Distribution</h3>
              <p>
                Distribution of analyzed reports by risk level.
              </p>
            </div>
          </div>

          {riskDistribution.length === 0 ? (
            <div className="empty-state">
              <p>No risk distribution data available.</p>
            </div>
          ) : (
            <div className="chart-container">
              <ResponsiveContainer
                width="100%"
                height={300}
              >
                <BarChart
                  data={riskDistribution}
                  margin={{
                    top: 10,
                    right: 20,
                    left: 0,
                    bottom: 10,
                  }}
                >
                  <CartesianGrid strokeDasharray="3 3" />

                  <XAxis
                    dataKey="risk_level"
                  />

                  <YAxis
                    allowDecimals={false}
                  />

                  <Tooltip />

                  <Bar
                    dataKey="count"
                    name="Reports"
                  />
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}
        </div>

        <div className="panel analytics-panel">
          <div className="panel-header">
            <div>
              <h3>Report Trends</h3>
              <p>
                Report uploads grouped by month.
              </p>
            </div>
          </div>

          {trends.length === 0 ? (
            <div className="empty-state">
              <p>No trend data available.</p>
            </div>
          ) : (
            <div className="chart-container">
              <ResponsiveContainer
                width="100%"
                height={300}
              >
                <LineChart
                  data={trends}
                  margin={{
                    top: 10,
                    right: 20,
                    left: 0,
                    bottom: 10,
                  }}
                >
                  <CartesianGrid strokeDasharray="3 3" />

                  <XAxis
                    dataKey="period"
                  />

                  <YAxis
                    allowDecimals={false}
                  />

                  <Tooltip />

                  <Line
                    type="monotone"
                    dataKey="count"
                    name="Reports"
                    strokeWidth={2}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}
        </div>
      </div>
    </section>
  )
}

export default Dashboard