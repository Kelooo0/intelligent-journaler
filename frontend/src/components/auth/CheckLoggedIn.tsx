import { Navigate, Outlet } from "react-router";

export default function CheckLoggedIn() {
  const token = localStorage.getItem("access_token");

  if (token) {
    return <Navigate to="/entries/list" replace />;
  }
  return <Outlet />;
}
