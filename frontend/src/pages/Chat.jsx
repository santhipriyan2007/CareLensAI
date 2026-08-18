import { useState } from "react";
import { api } from "../services/api";

export default function Chat({ selectedReport, onNavigate }) {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    const cleanedQuestion = question.trim();

    if (!cleanedQuestion || !selectedReport || loading) {
      return;
    }

    const userMessage = {
      role: "user",
      content: cleanedQuestion,
    };

    setMessages((prev) => [...prev, userMessage]);
    setQuestion("");
    setLoading(true);

    try {
      const response = await api.chat(
        selectedReport.id,
        cleanedQuestion,
      );

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            response.answer ||
            "The AI could not generate an answer.",
          disclaimer: response.medical_disclaimer,
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "error",
          content:
            error.message ||
            "Unable to get an AI response.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };

  if (!selectedReport) {
    return (
      <div className="page">
        <div className="page-heading">
          <div>
            <span className="eyebrow">
              AI MEDICAL CHAT
            </span>

            <h1>AI Medical Chat</h1>

            <p>
              Ask questions about a medical report and receive
              AI-assisted explanations grounded in the report.
            </p>
          </div>
        </div>

        <div className="analysis-empty">
          <div className="analysis-orb">✦</div>

          <h2>No report selected</h2>

          <p>
            Select a medical report before starting a
            conversation with CareLens AI.
          </p>

          {onNavigate && (
            <button
              className="primary-button"
              onClick={() => onNavigate("reports")}
            >
              Go to Reports
            </button>
          )}
        </div>
      </div>
    );
  }

  const reportName =
    selectedReport.original_file_name ||
    selectedReport.file_name ||
    selectedReport.filename ||
    "Medical Report";

  return (
    <div className="page">
      <div className="page-heading">
        <div>
          <span className="eyebrow">
            AI MEDICAL CHAT
          </span>

          <h1>AI Medical Chat</h1>

          <p>
            Ask questions about the selected medical report
            and receive AI-assisted explanations grounded in
            the report.
          </p>

          <p style={{ marginTop: "8px" }}>
            <strong>Report:</strong> {reportName}
          </p>

          <p
            style={{
              fontSize: "12px",
              color: "#64748b",
              marginTop: "4px",
            }}
          >
            Report ID: {selectedReport.id}
          </p>
        </div>
      </div>

      <div
        style={{
          marginTop: "20px",
          border: "1px solid #e2e8f0",
          borderRadius: "12px",
          padding: "20px",
          minHeight: "400px",
          maxHeight: "500px",
          overflowY: "auto",
          background: "#ffffff",
        }}
      >
        {messages.length === 0 ? (
          <div
            style={{
              textAlign: "center",
              padding: "80px 20px",
              color: "#64748b",
            }}
          >
            <div
              style={{
                fontSize: "32px",
                marginBottom: "12px",
              }}
            >
              ✦
            </div>

            <h3>Ask about this report</h3>

            <p>
              Ask CareLens AI questions about the medical
              information contained in this report.
            </p>

            <div
              style={{
                marginTop: "20px",
                display: "flex",
                flexDirection: "column",
                gap: "8px",
                alignItems: "center",
              }}
            >
              <button
                type="button"
                onClick={() =>
                  setQuestion(
                    "Can you explain the abnormal findings in simple language?"
                  )
                }
                style={{
                  border: "1px solid #cbd5e1",
                  background: "#ffffff",
                  borderRadius: "8px",
                  padding: "9px 14px",
                  cursor: "pointer",
                  color: "#334155",
                }}
              >
                Explain the abnormal findings
              </button>

              <button
                type="button"
                onClick={() =>
                  setQuestion(
                    "What is the HbA1c level and what does it mean?"
                  )
                }
                style={{
                  border: "1px solid #cbd5e1",
                  background: "#ffffff",
                  borderRadius: "8px",
                  padding: "9px 14px",
                  cursor: "pointer",
                  color: "#334155",
                }}
              >
                Explain the HbA1c level
              </button>

              <button
                type="button"
                onClick={() =>
                  setQuestion(
                    "What are the main findings in this report?"
                  )
                }
                style={{
                  border: "1px solid #cbd5e1",
                  background: "#ffffff",
                  borderRadius: "8px",
                  padding: "9px 14px",
                  cursor: "pointer",
                  color: "#334155",
                }}
              >
                Summarize the report
              </button>
            </div>
          </div>
        ) : (
          messages.map((message, index) => (
            <div
              key={index}
              style={{
                marginBottom: "18px",
                textAlign:
                  message.role === "user"
                    ? "right"
                    : "left",
              }}
            >
              <div
                style={{
                  display: "inline-block",
                  maxWidth: "80%",
                  padding: "12px 16px",
                  borderRadius: "12px",
                  background:
                    message.role === "user"
                      ? "#2563eb"
                      : message.role === "error"
                        ? "#fee2e2"
                        : "#f1f5f9",
                  color:
                    message.role === "user"
                      ? "#ffffff"
                      : message.role === "error"
                        ? "#991b1b"
                        : "#1e293b",
                  textAlign: "left",
                  whiteSpace: "pre-wrap",
                  lineHeight: "1.6",
                }}
              >
                {message.content}
              </div>

              {message.disclaimer && (
                <p
                  style={{
                    maxWidth: "80%",
                    marginTop: "8px",
                    fontSize: "12px",
                    color: "#64748b",
                    lineHeight: "1.5",
                  }}
                >
                  {message.disclaimer}
                </p>
              )}
            </div>
          ))
        )}

        {loading && (
          <div
            style={{
              color: "#64748b",
              padding: "10px 0",
            }}
          >
            AI is analyzing the report...
          </div>
        )}
      </div>

      <div
        style={{
          display: "flex",
          gap: "10px",
          marginTop: "16px",
        }}
      >
        <textarea
          value={question}
          onChange={(event) =>
            setQuestion(event.target.value)
          }
          onKeyDown={handleKeyDown}
          placeholder="Ask a question about this medical report..."
          rows={2}
          disabled={loading}
          style={{
            flex: 1,
            resize: "none",
            padding: "12px",
            border: "1px solid #cbd5e1",
            borderRadius: "10px",
            fontSize: "14px",
            outline: "none",
          }}
        />

        <button
          onClick={sendMessage}
          disabled={!question.trim() || loading}
          style={{
            padding: "12px 20px",
            border: "none",
            borderRadius: "10px",
            background:
              !question.trim() || loading
                ? "#94a3b8"
                : "#2563eb",
            color: "#ffffff",
            cursor:
              !question.trim() || loading
                ? "not-allowed"
                : "pointer",
            fontWeight: "600",
          }}
        >
          {loading ? "Thinking..." : "Send"}
        </button>
      </div>

      <p
        style={{
          marginTop: "14px",
          fontSize: "12px",
          color: "#64748b",
          lineHeight: "1.5",
        }}
      >
        AI-generated information is provided for clinical
        decision support and general understanding. It does
        not replace evaluation or advice from a qualified
        healthcare professional.
      </p>
    </div>
  );
}