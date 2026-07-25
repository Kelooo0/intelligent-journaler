import HomePage from "./pages/HomePage"
import LoginPage from "./pages/LoginPage"
import RegisterPage from "./pages/RegisterPage"
import CreateEntryPage from "./pages/CreateEntryPage"
import { Route, Routes } from "react-router"
import AppLayout from "./components/layout/AppLayout"
import EntriesPage from "./pages/EntriesPage"
import LoggedOutLayout from "./components/layout/LoggedOutLayout"

function App() {

  return (
    <Routes>
        <Route path="/" element={<HomePage />} />
        <Route element={<LoggedOutLayout />}>
            <Route path="/auth/register" element={<RegisterPage />} />
            <Route path="/auth/login" element={<LoginPage />} />
        </Route>
        <Route element={<AppLayout />}>
            <Route path="/entries" element={<EntriesPage />} />
            <Route path="/entries/new" element={<CreateEntryPage />} />
        </Route>
    </Routes>
  )
}

export default App
