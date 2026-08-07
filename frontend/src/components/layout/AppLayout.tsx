import { Outlet } from "react-router";
import Navbar from "./Navbar";

export default function AppLayout() {
  return (
    <>
      <Navbar />

      <main>
        <Outlet />
      </main>
    </>
  );
}
