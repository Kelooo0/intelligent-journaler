import LoginForm from "../components/auth/LoginForm";
import { useState } from "react";

export default function LoginPage() {
    const [error, setError] = useState("");
    return (
        <main>
            <section>
                <LoginForm onError={setError} />
            </section>
            <section>
                {error && <p role="alert">{ error }</p>}
            </section>
        </main>
    )
}
