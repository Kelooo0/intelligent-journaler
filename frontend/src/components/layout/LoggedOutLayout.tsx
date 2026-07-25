import { Outlet } from "react-router";
import LoggedOutNavbar from "./LoggedOutNavbar";

export default function LoggedOutLayout() {
    return (
        <>
            <LoggedOutNavbar />

            <main>
                <Outlet />
            </main>
        </>
    )
}
