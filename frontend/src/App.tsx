import HomePage from "./pages/HomePage"
import LoginPage from "./pages/LoginPage"
import RegisterPage from "./pages/RegisterPage"
import { Route, Routes } from "react-router"
import AppLayout from "./components/layout/AppLayout"
import EntriesPage from "./pages/EntriesPage"
import LoggedOutLayout from "./components/layout/LoggedOutLayout"
import EntryDetailsPage from "./pages/EntryDetailsPage"
import EntryCreatePage from "./pages/EntryCreatePage"
import EntryUpdatePage from "./pages/EntryUpdatePage"

function App() {

  return (
    <Routes>
        <Route path="/home" element={<HomePage />} />
        <Route element={<LoggedOutLayout />}>
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/login" element={<LoginPage />} />
        </Route>
        <Route element={<AppLayout />}>
            <Route path="/entries/list" element={<EntriesPage />} />
            <Route path="/entries/new" element={<EntryCreatePage />} />
            <Route path="/entries/:id/details" element={<EntryDetailsPage />} />
            <Route path="/entries/:id/edit" element={<EntryUpdatePage />} />
        </Route>
    </Routes>
  )
}

export default App
