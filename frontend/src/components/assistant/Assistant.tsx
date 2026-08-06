import AssistantForm from "./AssistantForm"
import { useState } from "react"

type AssistantProps = {
    onSuccess: () => Promise<void>;
    onAction: () => void;
}

export default function Assistant({
    onSuccess,
    onAction
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
                onStart={() => {setResponse(""); setError("");onAction();}}
                onChunk={(chunk) => {
                    setResponse((previousResponse) => previousResponse + chunk);
                    }}
                onSuccess={onSuccess}
                onLoading={setIsLoading}
                loading={isLoading}
                />
            </section>
            <section className="assistant-msgs">
                {
                    isLoading ? (<section className="as-message-container"><p className="message" role="status">Loading...</p></section>) :
                    error ? (<section className="as-message-container"><p className="message" role="alert">{ error }</p></section>) :
                    response ? (<section className="as-response-container"><p className="response">{response}</p></section>) :
                    (<section className="as-message-container"><p className="message" role="status">No response.</p></section>)
                }
            </section>
        </section>

    )
}
