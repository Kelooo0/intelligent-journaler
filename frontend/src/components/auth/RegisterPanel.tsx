import RegisterForm from "./RegisterForm"
import { useState } from "react";
import type { User } from "../../types/auth";
import RegisterResult from "./RegisterResult";

export default function RegisterPanel() {
    const [result, setResult] = useState<User | null>(null);
    const [error, setError] = useState("");
    return (

        <section id="register-panel">
            <RegisterForm onSuccess={setResult} onError={setError}/>
            {error && <p role="alert">{ error }</p>}
            {result && <RegisterResult result={ result } />}
        </section>
    )
}
