import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { toast, ToastContainer } from "react-toastify";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent } from "@/components/ui/card";
import { ForgotPasswordPopup } from "@/components/auth/ForgotPasswordPopup";
import { VerifyOTP } from "@/components/ui/VerifyOTP";
import { ArrowLeft, Eye, EyeOff, Loader2 } from "lucide-react";
import "react-toastify/dist/ReactToastify.css";

export function LoginForm() {
  const navigate = useNavigate();
  const [showForgotPassword, setShowForgotPassword] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [otpStep, setOtpStep] = useState(false);
  const [otpLoading, setOtpLoading] = useState(false);
  const [userId, setUserId] = useState(null);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("username", username);
      formData.append("password", password);

      const response = await axios.post("http://localhost:8000/auth/login", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      document.cookie = `access_token=${response.data.access_token}; path=/; Secure`;
      setUserId(response.data.user_id);
      setOtpStep(true);
      toast.info("OTP sent to your email", { position: "top-right" });
    } catch (err) {
      toast.error(err.response?.data?.detail || "Invalid credentials. Please try again.", { position: "top-right" });
    } finally {
      setLoading(false);
    }
  };

  const handleOTPVerification = async (otp) => {
    setOtpLoading(true);
    try {
      await new Promise((resolve) => setTimeout(resolve, 2000)); // Simulated delay
      navigate("/");
    } catch (err) {
      toast.error("Invalid OTP, please try again.");
    } finally {
      setOtpLoading(false);
    }
  };

  const handleBack = () => {
    if (otpStep) {
      document.cookie = "access_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC; Secure";
      setOtpStep(false);
      setUserId(null);
    } else {
      navigate("/");
    }
  };

  return (
    <div className="flex flex-col gap-6">
      <ToastContainer />
      <ForgotPasswordPopup isOpen={showForgotPassword} onClose={() => setShowForgotPassword(false)} />

      {/* Back Button */}
      <Button variant="outline" onClick={handleBack} className="w-10 h-10 rounded-full flex items-center justify-center" disabled={loading || otpLoading}>
        <ArrowLeft className="w-5 h-5" />
      </Button>

      <Card className="overflow-hidden">
        <CardContent className="grid p-0 md:grid-cols-2">
          <form className="p-6 md:p-8" onSubmit={handleLogin}>
            <div className="flex flex-col gap-6">
              <div className="flex flex-col items-center text-center">
                <h1 className="text-2xl font-bold">{otpStep ? "Enter OTP" : "Welcome back"}</h1>
                <p className="text-gray-500">{otpStep ? "Check your email for the OTP" : "Login to your account"}</p>
              </div>

              {!otpStep ? (
                <>
                  {/* Username Input */}
                  <div className="grid gap-2">
                    <Label htmlFor="username">Email</Label>
                    <Input
                      id="username"
                      type="email"
                      placeholder="Enter email"
                      value={username}
                      onChange={(e) => setUsername(e.target.value)}
                      required
                      disabled={loading} // ✅ Disabled when loading
                    />
                  </div>

                  {/* Password Input */}
                  <div className="grid gap-2 relative">
                    <Label htmlFor="password">Password</Label>
                    <div className="relative">
                      <Input
                        id="password"
                        type={showPassword ? "text" : "password"}
                        value={password}
                        placeholder="Enter Password"
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        disabled={loading} // ✅ Disabled when loading
                      />
                      <button
                        type="button"
                        className="absolute right-3 top-3"
                        onClick={() => setShowPassword(!showPassword)}
                        disabled={loading} // ✅ Disable password toggle button
                      >
                        {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                      </button>
                    </div>
                    <button
                      type="button"
                      onClick={() => setShowForgotPassword(true)}
                      className="text-sm text-gray-600 hover:text-black font-medium self-end"
                      disabled={loading} // ✅ Disable Forgot Password button
                    >
                      Forgot your password?
                    </button>
                  </div>

                  {/* Login Button */}
                  <Button type="submit" className="w-full" disabled={loading}>
                    {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Login"}
                  </Button>
                </>
              ) : (
                <VerifyOTP userId={userId} onSuccess={handleOTPVerification} loading={otpLoading} />
              )}
            </div>
          </form>

          {/* Right side: Illustration */}
          <div className="hidden md:flex items-center justify-center bg-white-100 p-4">
            <img src="login-illustration.png" alt="Login Illustration" className="w-3/4 h-auto max-w-xs object-contain" />
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
