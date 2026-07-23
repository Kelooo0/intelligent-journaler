import { useState } from "react"
import type { TokenResponse} from "../../types/auth";
import { login } from "../../api/authApi";

type LoginFormProps = {
    onSuccess: (result: TokenResponse) => void;
    onError: (message: string) => void;
};

export default function LoginForm({
    onSuccess,
    onError
}: LoginFormProps) {
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
                const data = await login(form_data_string);
                localStorage.setItem("access_token", data.access_token)
                onSuccess(data);
            } catch (error) {
                onError(
                    error instanceof Error
                    ? error.message
                    : "An unexpected error occured",
                );
            } finally {
                setIsLoading(false);
            }
    }
    return (
        <form onSubmit={handleSubmit}>
            <label htmlFor="email">Email:</label>
            <input id="email" type="email" onChange={(event) => setEmail(event.target.value)} disabled={isLoading}></input>
            <label htmlFor="password">Password:</label>
            <input id="password" type="password" onChange={(event) => setPassword(event.target.value)} disabled={isLoading}></input>
            <button type="submit" disabled={isLoading}>{isLoading ? "..." : "Login"}</button>
        </form>
    )
}
