import HomePage from "./pages/HomePage"
import LoginPage from "./pages/LoginPage"
import RegisterPage from "./pages/RegisterPage"
import { Route, Routes } from "react-router"
import AppLayout from "./components/layout/AppLayout"
import EntriesPage from "./pages/EntriesPage"
import GuestLayout from "./components/layout/GuestLayout"
import EntryDetailsPage from "./pages/EntryDetailsPage"
import EntryCreatePage from "./pages/EntryCreatePage"
import EntryUpdatePage from "./pages/EntryUpdatePage"
import ProtectedRoute from "./components/auth/ProtectedRoute"
import CheckLoggedIn from "./components/auth/CheckLoggedIn"

function App() {

  return (
    <Routes>
        <Route element={<CheckLoggedIn />}>
            <Route path="/" element={<HomePage />} />
        </Route>
        <Route element={<GuestLayout />}>
            <Route element={<CheckLoggedIn />}>
                <Route path="/register" element={<RegisterPage />} />
                <Route path="/login" element={<LoginPage />} />
            </Route>
        </Route>
        <Route element={<AppLayout />}>
            <Route element={<ProtectedRoute />}>
                <Route path="/entries/list" element={<EntriesPage />} />
                <Route path="/entries/new" element={<EntryCreatePage />} />
                <Route path="/entries/:id/details" element={<EntryDetailsPage />} />
                <Route path="/entries/:id/edit" element={<EntryUpdatePage />} />
            </Route>
        </Route>
    </Routes>
  )
}

export default App
