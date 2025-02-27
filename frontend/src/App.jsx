import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { ToastContainer } from "react-toastify"; // Import ToastContainer
import "react-toastify/dist/ReactToastify.css"; // Import styles

import { ProtectedAuthRoute } from "@/components/Protector/ProtectedAuthRoute";
import ProtectedOTPRoute from "@/components/Protector/ProtectedOTPRoute";
import Landing from "@/pages/Landing";
import LoginPage from "@/pages/LoginPage";
import RegisterPage from "@/pages/RegisterPage";
import ResetPasswordPage from "./pages/ResetPasswordPage";
import VerifyOTPPopup from "@/components/auth/VerifyOTPPopup";
import Profile from "./components/ui/Profile";
import ChangePassword from "./components/auth/ChangePassword";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing />} />

        {/* Protected Auth Routes (Redirect if already logged in) */}
        <Route element={<ProtectedAuthRoute />}>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
        </Route>

        <Route path="/reset-password" element={<ResetPasswordPage />} />
        <Route path="/change-password" element={<ChangePassword />} />
        <Route path="/profile" element={<Profile />} />

        {/* OTP verification route */}
        <Route element={<ProtectedOTPRoute />}>
          <Route path="/verify-otp" element={<VerifyOTPPopup />} />
        </Route>
      </Routes>

      {/* Add ToastContainer here to make toasts work globally */}
      <ToastContainer position="top-right" autoClose={3000} />
    </Router>
  );
}

export default App;