import { useState } from "react"
import { Login } from "../../api/authApi";
import { useNavigate } from "react-router";

type LoginFormProps = {
    onError: (message: string) => void;
};

export default function LoginForm({
    onError
}: LoginFormProps) {
    const navigate = useNavigate();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [isLoading, setIsLoading] = useState(false);


    async function handleSubmit(event: React.SubmitEvent<HTMLFormElement>) {
            event.preventDefault();
            try {
                setIsLoading(true);
                onError("");
                const form_data = new URLSearchParams()
                form_data.append("username", email);
                form_data.append("password", password);
                const form_data_string = form_data.toString()
                const data = await Login(form_data_string);
                localStorage.setItem("access_token", data.access_token)
                navigate("/entries/list", {"state": {"message": "Logged in succesfully.", "type": "success"}})

            } catch (error) {
                onError(
                    error instanceof Error
                    ? error.message
                    : "An unexpected error occured.",
                );
            } finally {
                setIsLoading(false);
            }
    }
    return (
        <form onSubmit={handleSubmit}>
            <label htmlFor="email">Email:</label>
            <input id="email" type="email" value={email} onChange={(event) => setEmail(event.target.value)} disabled={isLoading}></input>
            <label htmlFor="password">Password:</label>
            <input id="password" type="password" value={password} onChange={(event) => setPassword(event.target.value)} disabled={isLoading}></input>
            <button type="submit" disabled={isLoading}>{isLoading ? "..." : "Login"}</button>
        </form>
    )
}
