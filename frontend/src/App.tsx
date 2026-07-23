import HomePage from "./pages/HomePage"
import LoginPage from "./pages/LoginPage"
import RegisterPage from "./pages/RegisterPage"
import CreateEntryPage from "./pages/CreateEntryPage"
import LogoutButton from "./components/auth/Logout"
function App() {

  return (
    <>
        <HomePage />
        <RegisterPage />
        <LoginPage />
        <LogoutButton />
        <CreateEntryPage />
    </>
  )
}

export default App
