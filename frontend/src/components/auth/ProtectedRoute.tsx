import { Navigate, Outlet } from "react-router";

export default function ProtectedRoute() {
    const token = localStorage.getItem("access_token");

    if(!token) {
        return (
            <Navigate to="/" replace state={{"message": "You must log in to access this resource.", "type": "error"}} />
        )
    }
    return <Outlet />
}
