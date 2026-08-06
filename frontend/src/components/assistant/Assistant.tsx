import AssistantForm from "./AssistantForm"
import { useState } from "react"

type AssistantProps = {
    onSuccess: () => Promise<void>;
}

export default function Assistant({
    onSuccess
}: AssistantProps) {
    const [error, setError] = useState("");
    const [response, setResponse] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    return(
        <section className="assistant-container">
            <section className="assistant-header-container">
                <h2 className="assistant-header">Journal Assistant</h2>
            </section>
            <section className="assistant-form-container">
                <AssistantForm
                onError={setError}
                onStart={() => {setResponse(""); setError("");}}
                onChunk={(chunk) => {
                    setResponse((previousResponse) => previousResponse + chunk);
                    }}
                onSuccess={onSuccess}
                onLoading={setIsLoading}
                loading={isLoading}
                />
            </section>
            <section className="assistant-msgs">
                {error && <p className="message" role="alert">{ error }</p>}
                {response && <p className="response">{response}</p>}
                {!error && !response && !isLoading && (<p className="message" role="status">No response.</p>)}
                {isLoading && <p className="message" role="status">Loading...</p>}
            </section>
        </section>

    )
}
