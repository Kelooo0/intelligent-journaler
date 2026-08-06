import RegisterForm from "../components/auth/RegisterForm"
import { useState } from "react"
import type { User } from "../types/auth"
import "./Auth.css";

export default function RegisterPage() {
    const [result, setResult] = useState<User | null>(null);
    const [error, setError] = useState("");
    return (
        <main className="auth-main">
            <section className="auth-header">
                <h1>Create account</h1>
            </section>
            <section className="auth-form-container">
                <RegisterForm onSuccess={setResult} onError={setError}/>
            </section>
            <section className="auth-messages">
                {error && <p className="auth-msg"role="alert">{ error }</p>}
                {result && <p className="auth-msg" role="status">Registered succesfully. You may log in now.</p> }
            </section>
        </main>
    )
}
