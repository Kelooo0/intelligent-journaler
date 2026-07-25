import LoginForm from "./LoginForm"
import { useState } from "react";

export default function LoginPanel() {
    const [error, setError] = useState("");
    return (
        <section id="login-panel">
            <LoginForm onError={setError} />
            <section>
                {error && <p role="alert">{ error }</p>}
            </section>

        </section>
    )
}
