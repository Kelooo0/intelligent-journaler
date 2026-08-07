import { Link } from "react-router";
import { useLocation } from "react-router";
import { useNavigate } from "react-router";
import { useEffect } from "react";
import { useState } from "react";
import "./HomePage.css";

interface LocationState {
  message?: string;
  type?: "success" | "error" | "info";
}

type SavedMessage = {
  message: string;
  type: "success" | "error" | "info";
};

export default function HomePage() {
  const location = useLocation();
  const navigate = useNavigate();
  const locationState = location.state as LocationState | null;
  const [notification] = useState<SavedMessage | null>(() => {
    if (locationState?.message) {
      return {
        message: locationState.message,
        type: locationState.type ?? "info",
      };
    }

    const savedState = sessionStorage.getItem("state");

    if (!savedState) {
      return null;
    }

    try {
      return JSON.parse(savedState) as SavedMessage;
    } catch {
      return null;
    }
  });
  const message = notification?.message ?? "";
  const type = notification?.type ?? "info";

  useEffect(() => {
    sessionStorage.removeItem("state");

    if (locationState?.message) {
      navigate(location.pathname, {
        replace: true,
        state: null,
      });
    }
  }, [locationState?.message, location.pathname, navigate]);

  return (
    <main className="home-main">
      <section className="home-header">
        <h2>Welcome to</h2>
        <h1>Intelligent Journaler</h1>
      </section>
      <section className="home-buttons">
        <section className="home-button-box login-box">
          <Link to="/login" className="home-link login-link">
            Log in
          </Link>
        </section>
        <section className="home-button-box register-box">
          <Link to="/register" className="home-link register-link">
            Register
          </Link>
        </section>
      </section>
      <section className="home-messages">
        {message && (
          <p role={type === "error" ? "alert" : "status"}>{message}</p>
        )}
      </section>
    </main>
  );
}
