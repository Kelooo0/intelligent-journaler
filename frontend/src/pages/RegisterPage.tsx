import RegisterForm from "../components/auth/RegisterForm"
import { useState } from "react"
import type { User } from "../types/auth"

export default function RegisterPage() {
    const [result, setResult] = useState<User | null>(null);
    const [error, setError] = useState("");
    return (
        <main>
            <section>
                <RegisterForm onSuccess={setResult} onError={setError}/>
            </section>
            <section>
                {error && <p role="alert">{ error }</p>}
                {result && <p role="status">Registered succesfully. You may log in now.</p> }
            </section>
        </main>
    )
}
