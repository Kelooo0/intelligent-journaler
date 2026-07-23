import { apiRequest } from "./client";
import type { RegisterPayload, User, TokenResponse } from "../types/auth";

export function register(
    payload: RegisterPayload,
): Promise<User> {
    return apiRequest<User>("/auth/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
    })
}

export function login(
    form_data_string: string,
): Promise<TokenResponse> {
    return apiRequest<TokenResponse>("/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: form_data_string
    })
}
