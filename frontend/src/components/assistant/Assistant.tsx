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

    return(
        <section>
            <section>
                <h2>Journal Assistant</h2>
            </section>
            <section>
                <AssistantForm
                onError={setError}
                onStart={() => setResponse("")}
                onChunk={(chunk) => {
                    setResponse((previousResponse) => previousResponse + chunk);
                    }}
                onSuccess={onSuccess}
                />
            </section>
            <section>
                {error && <p role="alert">{ error }</p>}
                {response && <p>Response: {response}</p>}
            </section>
        </section>

    )
}
