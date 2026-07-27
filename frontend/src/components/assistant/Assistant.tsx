import AssistantForm from "./AssistantForm"
import { useState } from "react"

export default function Assistant() {
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
                />
            </section>
            <section>
                {error && <p role="alert">{ error }</p>}
                {response && <p>Response: {response}</p>}
            </section>
        </section>

    )
}
