import { useEffect, useRef, useState } from "react";
import { api } from "../services/api";

function Reports({ onNavigate }) {
  const [reports, setReports] = useState([]);
  const [patients, setPatients] = useState([]);
  const [selectedPatient, setSelectedPatient] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);

  const [loading, setLoading] = useState(false);
  const [loadingReports, setLoadingReports] = useState(true);
  const [loadingPatients, setLoadingPatients] = useState(true);

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const fileInput = useRef(null);

  const loadReports = async () => {
    try {
      const data = await api.getReports();

      setReports(
        Array.isArray(data)
          ? data
          : data.reports || [],
      );
    } catch (err) {
      setError(err.message);
    } finally {
      setLoadingReports(false);
    }
  };

  const loadPatients = async () => {
    try {
      const data = await api.getPatients();

      setPatients(
        Array.isArray(data)
          ? data
          : data.patients || [],
      );
    } catch (err) {
      setError(err.message);
    } finally {
      setLoadingPatients(false);
    }
  };

  useEffect(() => {
    loadReports();
    loadPatients();
  }, []);

  const upload = async () => {
    if (!selectedPatient) {
      setError("Please select a patient first.");
      return;
    }

    if (!selectedFile) {
      setError("Please select a medical report first.");
      return;
    }

    setLoading(true);
    setError("");
    setMessage("");

    try {
      const report = await api.uploadReport(
        selectedFile,
        selectedPatient,
      );

      setMessage("Report uploaded successfully.");
      setSelectedFile(null);
      setSelectedPatient("");

      if (fileInput.current) {
        fileInput.current.value = "";
      }

      await loadReports();

      const uploadedReport =
        report.report ||
        report.data ||
        report;

      if (uploadedReport?.id) {
        onNavigate("analysis", {
          report: uploadedReport,
        });
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const openAnalysis = (report) => {
    onNavigate("analysis", {
      report,
    });
  };

  const openChat = (report) => {
    onNavigate("chat", {
      report,
    });
  };

  return (
    <section className="page-section">
      <div className="page-header">
        <div>
          <span className="section-label">
            DOCUMENT MANAGEMENT
          </span>

          <h1>Medical Reports</h1>

          <p>
            Upload and analyze PDF or image-based medical
            reports.
          </p>
        </div>
      </div>

      <div className="upload-panel">
        <div className="form-group">
          <label htmlFor="patient-select">
            Patient
          </label>

          <select
            id="patient-select"
            value={selectedPatient}
            onChange={(e) =>
              setSelectedPatient(e.target.value)
            }
            disabled={loadingPatients || loading}
          >
            <option value="">
              {loadingPatients
                ? "Loading patients..."
                : "Select a patient"}
            </option>

            {patients.map((patient) => (
              <option
                key={patient.id}
                value={patient.id}
              >
                {patient.full_name}
              </option>
            ))}
          </select>
        </div>

        <div
          className="upload-zone"
          onClick={() => fileInput.current?.click()}
        >
          <div className="upload-icon">↑</div>

          <h2>
            {selectedFile
              ? selectedFile.name
              : "Upload medical report"}
          </h2>

          <p>
            PDF, PNG or JPG • Maximum 10 MB
          </p>

          <input
            ref={fileInput}
            type="file"
            accept=".pdf,.png,.jpg,.jpeg"
            hidden
            onChange={(e) =>
              setSelectedFile(
                e.target.files?.[0] || null,
              )
            }
          />

          <button
            type="button"
            className="secondary-button"
            onClick={(e) => {
              e.stopPropagation();
              fileInput.current?.click();
            }}
            disabled={loading}
          >
            Choose file
          </button>
        </div>

        {selectedFile && (
          <button
            className="primary-button upload-button"
            onClick={upload}
            disabled={loading}
          >
            {loading
              ? "Uploading..."
              : "Upload & Continue"}
          </button>
        )}

        {message && (
          <div className="success-box">
            {message}
          </div>
        )}

        {error && (
          <div className="error-box">
            {error}
          </div>
        )}
      </div>

      <div className="panel">
        <div className="panel-header">
          <div>
            <h3>Uploaded Reports</h3>

            <p>
              Reports available in your workspace.
            </p>
          </div>
        </div>

        {loadingReports ? (
          <div className="loading-state">
            Loading reports...
          </div>
        ) : reports.length === 0 ? (
          <div className="empty-state compact">
            <h3>No reports uploaded</h3>

            <p>
              Your uploaded reports will appear here.
            </p>
          </div>
        ) : (
          <div className="report-list">
            {reports.map((report) => (
              <div
                className="report-row"
                key={report.id}
              >
                <div className="file-icon">
                  PDF
                </div>

                <div className="report-info">
                  <strong>
                    {report.file_name ||
                      report.filename ||
                      report.original_file_name ||
                      "Medical Report"}
                  </strong>

                  <span>
                    ID: {report.id}
                  </span>
                </div>

                <div
                  style={{
                    display: "flex",
                    gap: "8px",
                    alignItems: "center",
                  }}
                >
                  <button
                    className="small-button"
                    onClick={() =>
                      openAnalysis(report)
                    }
                  >
                    Analyze →
                  </button>

                  <button
                    className="small-button"
                    onClick={() =>
                      openChat(report)
                    }
                  >
                    Chat →
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  );
}

export default Reports;