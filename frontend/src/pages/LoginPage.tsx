import LoginForm from "../components/auth/LoginForm";
import { useState } from "react";
import "./Auth.css";

export default function LoginPage() {
    const [error, setError] = useState("");
    return (
        <main className="auth-main">
            <section className="auth-header">
                <h1>Log in</h1>
            </section>
            <section className="auth-form-container">
                <LoginForm onError={setError} />
            </section>
            <section className="auth-messages">
                {error && <p role="alert">{ error }</p>}
            </section>
        </main>
    )
}
