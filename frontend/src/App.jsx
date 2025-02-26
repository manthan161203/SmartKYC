import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { ProtectedAuthRoute } from "@/components/Protector/ProtectedAuthRoute";
import { ProtectedOTPRoute } from "@/components/Protector/ProtectedOTPRoute";
import Landing from "@/pages/Landing";
import LoginPage from "@/pages/LoginPage";
import RegisterPage from "@/pages/RegisterPage";
import ResetPasswordPage from "./pages/ResetPasswordPage";
import { VerifyOTP } from "@/components/auth/VerifyOTP";

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
          <Route path="/verify-otp" element={<VerifyOTP />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
