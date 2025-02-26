import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { ProtectedAuthRoute } from "@/components/Protector/ProtectedAuthRoute";
import { ProtectedOTPRoute } from "@/components/Protector/ProtectedOTPRoute";
import Landing from "@/pages/Landing";
import LoginPage from "@/pages/LoginPage";
import RegisterPage from "@/pages/RegisterPage";
import ResetPasswordPage from "./pages/ResetPasswordPage";
import VerifyOTPPopup from "@/components/auth/VerifyOTPPopup"; // ✅ Correct

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

        {/* OTP verification route */}
        <Route element={<ProtectedOTPRoute />}>
          <Route path="/verify-otp" element={<VerifyOTPPopup />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
