export function logout() {
    localStorage.removeItem("access_token");
}

export default function LogoutButton() {
    return (
        <button onClick={logout}>Logout</button>
    )
}
