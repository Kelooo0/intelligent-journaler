import { Outlet } from "react-router";
import GuestNavbar from "./GuestNavbar";

export default function GuestLayout() {
    return (
        <>
            <GuestNavbar />

            <main>
                <Outlet />
            </main>
        </>
    )
}
