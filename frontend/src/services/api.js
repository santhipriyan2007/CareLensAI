const API_BASE_URL =
  import.meta.env.VITE_API_URL ||
  "http://127.0.0.1:8000";

async function request(endpoint, options = {}) {
  const token = localStorage.getItem("carelens_token");

  const headers = {
    ...(options.headers || {}),
  };

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(
    `${API_BASE_URL}${endpoint}`,
    {
      ...options,
      headers,
    },
  );

  const contentType =
    response.headers.get("content-type") || "";

  let data;

  if (contentType.includes("application/json")) {
    data = await response.json();
  } else {
    data = await response.text();
  }

  if (!response.ok) {
    const message =
      typeof data === "object"
        ? data.detail ||
          data.message ||
          "Request failed"
        : data || "Request failed";

    throw new Error(message);
  }

  return data;
}

export const api = {

  login: (data) =>
    request("/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    }),

  register: (data) =>
    request("/auth/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    }),

  getReports: () =>
    request("/reports"),

  getPatients: () =>
    request("/patients"),

  getReport: (reportId) =>
    request(`/reports/${reportId}`),

  uploadReport: (file, patientUserId) => {
    const formData = new FormData();

    formData.append("patient_user_id", patientUserId);
    formData.append("file", file);

    return request("/reports/upload", {
      method: "POST",
      body: formData,
    });
  },

  analyzeReport: (reportId) =>
    request(`/analysis/report/${reportId}`, {
      method: "POST",
    }),

  getAnalysis: (reportId) =>
    request(`/analysis/report/${reportId}`),

  getHistory: (page = 1, pageSize = 10) =>
    request(
      `/analysis/history?page=${page}&page_size=${pageSize}`,
    ),

  compareReports: (
    previousReportId,
    currentReportId,
  ) =>
    request(
      `/compare?previous_report_id=${previousReportId}&current_report_id=${currentReportId}`,
    ),

  chat: (reportId, question) =>
    request("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        report_id: reportId,
        question,
      }),
    }),

  getAnalyticsOverview: () =>
    request("/analytics/overview"),

  getRiskDistribution: () =>
    request("/analytics/risk-distribution"),

  getAnalyticsTrends: () =>
    request("/analytics/trends"),
};