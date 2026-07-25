import RegisterForm from "./RegisterForm"
import { useState } from "react";
import type { User } from "../../types/auth";

export default function RegisterPanel() {
    const [result, setResult] = useState<User | null>(null);
    const [error, setError] = useState("");
    return (

        <section id="register-panel">
            <RegisterForm onSuccess={setResult} onError={setError}/>
            <section>
                {error && <p role="alert">{ error }</p>}
                {result && <p role="status">Registered succesfully. You may log in now.</p> }
            </section>
        </section>
    )
}
