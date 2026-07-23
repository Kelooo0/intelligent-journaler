import LoginForm from "./LoginForm"
import { useState } from "react";
import type { TokenResponse } from "../../types/auth";
import LoginResult from "./LoginResult";

export default function LoginPanel() {
    const [result, setResult] = useState<TokenResponse | null>(null);
    const [error, setError] = useState("");
    return (
        <section id="login-panel">
            <LoginForm onSuccess={setResult} onError={setError} />
            {error && <p role="alert">{ error }</p>}
            {result && <LoginResult />}
        </section>
    )
}
