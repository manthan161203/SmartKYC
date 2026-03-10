import { useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom"; // Get token from URL
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent } from "@/components/ui/card";
import { ArrowLeft, Eye, EyeOff, Loader2 } from "lucide-react"; // Import Loader2 for spinner
import { toast, ToastContainer } from "react-toastify";
import axios from "axios";
import PasswordStrengthBar from "react-password-strength-bar";
import { z } from "zod";
import "react-toastify/dist/ReactToastify.css";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

// Define password validation schema
const passwordSchema = z
  .string()
  .min(8, "Password must be at least 8 characters")
  .regex(/[A-Z]/, "Must include at least one uppercase letter")
  .regex(/[a-z]/, "Must include at least one lowercase letter")
  .regex(/[0-9]/, "Must include at least one number")
  .regex(/[\W_]/, "Must include at least one special character");

export function ResetPassword() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const token = searchParams.get("token"); // Get token from URL

  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [passwordStrength, setPasswordStrength] = useState(0); // Strength level (0-4)

  const handleResetPassword = async (e) => {
    e.preventDefault();

    try {
      // Validate password
      passwordSchema.parse(password);
    } catch (err) {
      toast.error(err.errors[0].message);
      return;
    }

    if (password !== confirmPassword) {
      toast.error("Passwords do not match.");
      return;
    }

    if (passwordStrength < 3) {
      toast.error("Please choose a stronger password.");
      return;
    }

    setLoading(true);

    setTimeout(async () => {
      try {
        await axios.post(`${API_BASE_URL}/auth/reset-password`, {
          token,
          new_password: password,
          confirm_new_password: confirmPassword,
        }, {
          headers: { "Content-Type": "application/json" },
        });

        toast.success("Password reset successful! Redirecting to login...");
        setTimeout(() => navigate("/login"), 2000);
      } catch (err) {
        toast.error(err.response?.data?.detail || "Failed to reset password.");
      } finally {
        setLoading(false);
      }
    }, 2500);
  };

  return (
    <div className="flex flex-col gap-6">
      <ToastContainer />

      <Button variant="outline" onClick={() => navigate("/login")} className="w-10 h-10 rounded-full flex items-center justify-center">
        <ArrowLeft className="w-5 h-5" />
      </Button>

      <Card className="overflow-hidden">
        <CardContent className="grid p-0 md:grid-cols-2">
          <form className="p-6 md:p-8" onSubmit={handleResetPassword}>
            <div className="flex flex-col gap-6">
              <div className="flex flex-col items-center text-center">
                <h1 className="text-2xl font-bold">Reset Password</h1>
                <p className="text-gray-500">Enter your new password</p>
              </div>

              {/* Password Input */}
              <div className="grid gap-2">
                <Label htmlFor="password">New Password</Label>
                <div className="relative">
                  <Input
                    id="password"
                    type={showPassword ? "text" : "password"}
                    value={password}
                    placeholder="Enter new password"
                    onChange={(e) => setPassword(e.target.value)}
                    disabled={loading}
                    required
                  />
                  <button
                    type="button"
                    className="absolute right-3 top-3"
                    onClick={() => setShowPassword(!showPassword)}
                    disabled={loading}
                  >
                    {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
                {/* Password Strength Indicator */}
                <PasswordStrengthBar password={password} onChangeScore={setPasswordStrength} />
              </div>

              {/* Confirm Password Input */}
              <div className="grid gap-2">
                <Label htmlFor="confirm-password">Confirm Password</Label>
                <div className="relative">
                  <Input
                    id="confirm-password"
                    type={showPassword ? "text" : "password"}
                    value={confirmPassword}
                    placeholder="Confirm new password"
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    disabled={loading}
                    required
                  />
                  <button
                    type="button"
                    className="absolute right-3 top-3"
                    onClick={() => setShowPassword(!showPassword)}
                    disabled={loading}
                  >
                    {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
              </div>

              {/* Reset Password Button */}
              <Button type="submit" className="w-full" disabled={loading}>
                {loading ? <Loader2 className="animate-spin w-5 h-5" /> : "Reset Password"}
              </Button>
            </div>
          </form>

          {/* Right side: Illustration */}
          <div className="hidden md:flex items-center justify-center bg-white-100 p-4">
            <img src="login-illustration.png" alt="Reset Password" className="w-3/4 h-auto max-w-xs object-contain" />
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

export default ResetPassword;
