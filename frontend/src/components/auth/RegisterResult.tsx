import type { User } from "../../types/auth";

type RegisterResultProps = {
    result: User;
};

export default function RegisterResult({
    result,
}: RegisterResultProps) {
    return (
        <section>
            <p>Created user with an email:{result.email}</p>
        </section>
    )
}
