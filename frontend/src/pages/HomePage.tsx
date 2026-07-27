import { Link } from "react-router"
import { useLocation } from "react-router"

interface LocationState {
    message?: string;
    type?: "success" | "error";
}
export default function HomePage() {
    const location  = useLocation();
    const state = location.state as LocationState | null;
    return (
        <main>
            <section>
                <h1>Intelligent Journaler</h1>
            </section>
            <section>
                {state?.message && (<p role={state.type === "error" ? "error" : "status"}>{state.message}</p>)}
            </section>
            <section>
                <Link to="/login">Login</Link>
                <Link to="/register">Register</Link>
            </section>
        </main>
    )
}
