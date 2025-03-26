import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { ToastContainer } from "react-toastify"; // Import ToastContainer
import "react-toastify/dist/ReactToastify.css"; // Import styles

import { ProtectedAuthRoute } from "@/components/Protector/ProtectedAuthRoute";
import ProtectedOTPRoute from "@/components/Protector/ProtectedOTPRoute";
import ProtectedRoute from "@/components/Protector/ProtectedRoute";
import Landing from "@/pages/LandingPage";
import LoginPage from "@/pages/LoginPage";
import RegisterPage from "@/pages/RegisterPage";
import ResetPasswordPage from "./pages/ResetPasswordPage";
import VerifyOTPPopup from "@/components/auth/VerifyOTPPopup";
import Profile from "./components/ui/Profile";
import ChangePasswordPage from "./pages/ChangePasswordPage";
import DocumentUploadPage from "@/pages/DocumentUploadPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/reset-password" element={<ResetPasswordPage />} />

        {/* Protected Auth Routes (Redirect if already logged in) */}
        <Route element={<ProtectedAuthRoute />}>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
        </Route>
        <Route element={<ProtectedRoute />}>
          <Route path="/change-password" element={<ChangePasswordPage />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/upload-documents" element={<DocumentUploadPage />} />
        </Route>
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