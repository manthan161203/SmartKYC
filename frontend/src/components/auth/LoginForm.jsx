import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { toast, ToastContainer } from "react-toastify";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent } from "@/components/ui/card";
import { ForgotPasswordPopup } from "@/components/auth/ForgotPasswordPopup";
import { ArrowLeft, Eye, EyeOff, Loader2 } from "lucide-react";
import "react-toastify/dist/ReactToastify.css";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export function LoginForm() {
  const navigate = useNavigate();
  const [showForgotPassword, setShowForgotPassword] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("username", username);
      formData.append("password", password);

      const response = await axios.post(`${API_BASE_URL}/auth/login`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      document.cookie = `access_token=${response.data.access_token}; path=/; Secure`;

      toast.success("Login successful!", { position: "top-right" });
      navigate("/"); // Redirect after login success
    } catch (err) {
      toast.error(err.response?.data?.detail || "Invalid credentials. Please try again.", { position: "top-right" });
    } finally {
      setLoading(false);
    }
  };

  const handleBack = () => {
    navigate("/");
  };

  return (
    <div className="flex flex-col gap-6">
      <ToastContainer />
      <ForgotPasswordPopup isOpen={showForgotPassword} onClose={() => setShowForgotPassword(false)} />

      {/* Back Button */}
      <Button variant="outline" onClick={handleBack} className="w-10 h-10 rounded-full flex items-center justify-center" disabled={loading}>
        <ArrowLeft className="w-5 h-5" />
      </Button>

      <Card className="overflow-hidden">
        <CardContent className="grid p-0 md:grid-cols-2">
          <form className="p-6 md:p-8" onSubmit={handleLogin}>
            <div className="flex flex-col gap-6">
              <div className="flex flex-col items-center text-center">
                <h1 className="text-2xl font-bold">Welcome back</h1>
                <p className="text-gray-500">Login to your account</p>
              </div>

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
              <p className="text-center text-xs text-gray-600">
                Dont have an account?{" "}
                <span
                  onClick={() => navigate("/register")}
                  className="font-semibold text-black hover:underline cursor-pointer"
                >
                  Register
                </span>
              </p>
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
