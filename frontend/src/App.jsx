import { useState } from "react";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Reports from "./pages/Reports";
import History from "./pages/History";
import Compare from "./pages/Compare";
import Analysis from "./pages/Analysis";
import Chat from "./pages/Chat";

import "./App.css";

function App() {
  const [page, setPage] = useState(
    localStorage.getItem("carelens_token")
      ? "dashboard"
      : "login",
  );

  const [selectedReport, setSelectedReport] =
    useState(null);

  const [selectedAnalysis, setSelectedAnalysis] =
    useState(null);

  /*
   * Central navigation function.
   *
   * Important:
   * selectedReport is intentionally preserved when
   * navigating to Chat.
   */
  const navigate = (nextPage, data = null) => {
    if (nextPage === "analysis") {
      setSelectedReport(
        data?.report || null,
      );

      setSelectedAnalysis(
        data?.analysis || null,
      );
    }

    if (nextPage === "chat") {
      /*
       * Chat can receive:
       *
       * 1. { report: report }
       * 2. report
       *
       * This makes navigation more flexible.
       */
      const report =
        data?.report ||
        data ||
        selectedReport ||
        null;

      if (report) {
        setSelectedReport(report);
      }
    }

    if (nextPage === "reports") {
      /*
       * Do not clear selectedReport here.
       *
       * Keeping it allows the user to return to
       * Chat without losing the current report.
       */
    }

    setPage(nextPage);
  };

  /*
   * Logout
   */
  const logout = () => {
    localStorage.removeItem("carelens_token");
    localStorage.removeItem("carelens_user");

    setSelectedReport(null);
    setSelectedAnalysis(null);

    setPage("login");
  };

  /*
   * Authentication pages
   */
  if (page === "login") {
    return (
      <Login
        onLogin={() => setPage("dashboard")}
        onRegister={() => setPage("register")}
      />
    );
  }

  if (page === "register") {
    return (
      <Register
        onRegistered={() => setPage("login")}
        onLogin={() => setPage("login")}
      />
    );
  }

  /*
   * Main application pages
   */
  const renderPage = () => {
    switch (page) {
      case "dashboard":
        return (
          <Dashboard
            onNavigate={navigate}
          />
        );

      case "reports":
        return (
          <Reports
            onNavigate={navigate}
          />
        );

      case "history":
        return (
          <History
            onNavigate={navigate}
          />
        );

      case "compare":
        return (
          <Compare
            onNavigate={navigate}
          />
        );

      case "analysis":
        return (
          <Analysis
            report={selectedReport}
            analysis={selectedAnalysis}
            onNavigate={navigate}
          />
        );

      case "chat":
        return (
          <Chat
            selectedReport={selectedReport}
            onNavigate={navigate}
          />
        );

      default:
        return (
          <Dashboard
            onNavigate={navigate}
          />
        );
    }
  };

  /*
   * Read logged-in user information.
   */
  let storedUser = {};

  try {
    storedUser = JSON.parse(
      localStorage.getItem("carelens_user") ||
        "{}",
    );
  } catch {
    storedUser = {};
  }

  const userRole =
    storedUser.role || "doctor";

  const displayName =
    storedUser.full_name ||
    storedUser.name ||
    (userRole === "patient"
      ? "Patient"
      : "Doctor");

  const roleLabel =
    userRole === "patient"
      ? "Patient"
      : userRole === "admin"
        ? "Administrator"
        : "Medical Professional";

  const avatarLabel =
    userRole === "patient"
      ? "PT"
      : userRole === "admin"
        ? "AD"
        : "DR";

  return (
    <div className="app-shell">
      {/* =========================
          SIDEBAR
      ========================= */}

      <aside className="sidebar">
        <div className="sidebar-brand">
          <div className="brand-mark">
            C
          </div>

          <div>
            <strong>CareLens</strong>
            <span>
              AI Clinical Intelligence
            </span>
          </div>
        </div>

        <nav className="sidebar-nav">
          {/* Dashboard */}

          <button
            className={
              page === "dashboard"
                ? "nav-item active"
                : "nav-item"
            }
            onClick={() =>
              navigate("dashboard")
            }
          >
            <span>⌂</span>
            Dashboard
          </button>

          {/* Reports */}

          <button
            className={
              page === "reports"
                ? "nav-item active"
                : "nav-item"
            }
            onClick={() =>
              navigate("reports")
            }
          >
            <span>▣</span>
            Reports
          </button>

          {/* Analysis History */}

          <button
            className={
              page === "history"
                ? "nav-item active"
                : "nav-item"
            }
            onClick={() =>
              navigate("history")
            }
          >
            <span>◷</span>
            Analysis History
          </button>

          {/* Compare Reports */}

          <button
            className={
              page === "compare"
                ? "nav-item active"
                : "nav-item"
            }
            onClick={() =>
              navigate("compare")
            }
          >
            <span>⇄</span>
            Compare Reports
          </button>

          {/* AI Medical Chat */}

          <button
            className={
              page === "chat"
                ? "nav-item active"
                : "nav-item"
            }
            onClick={() =>
              navigate("chat")
            }
          >
            <span>✦</span>
            AI Medical Chat
          </button>
        </nav>

        <div className="sidebar-bottom">
          <div className="ai-status">
            <span className="status-dot"></span>
            AI Engine Online
          </div>

          <button
            className="logout-button"
            onClick={logout}
          >
            Sign out
          </button>
        </div>
      </aside>

      {/* =========================
          MAIN CONTENT
      ========================= */}

      <main className="main-content">
        <header className="topbar">
          <div>
            <span className="topbar-label">
              Clinical Decision Support
            </span>

            <h2>CareLens AI</h2>
          </div>

          <div className="doctor-profile">
            <div className="avatar">
              {avatarLabel}
            </div>

            <div>
              <strong>
                {displayName}
              </strong>

              <span>
                {roleLabel}
              </span>
            </div>
          </div>
        </header>

        <div className="page-container">
          {renderPage()}
        </div>
      </main>
    </div>
  );
}

export default App;