import { useState } from "react"
import type { User, RegisterPayload } from "../../types/auth";
import { Register } from "../../api/authApi";

type RegisterFormProps = {
    onSuccess: (result: User) => void;
    onError: (message: string) => void;
};

export default function RegisterForm({
    onSuccess,
    onError,
}: RegisterFormProps) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    async function handleSubmit(event: React.SubmitEvent<HTMLFormElement>) {
            event.preventDefault();
            try {
                setIsLoading(true);
                onError("");
                const payload: RegisterPayload = {
                    "email": email,
                    "password": password,
                }
                const data = await Register(payload);
                onSuccess(data);
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
            <button type="submit" disabled={isLoading}>{isLoading ? "..." : "Register"}</button>
        </form>
    )
}
