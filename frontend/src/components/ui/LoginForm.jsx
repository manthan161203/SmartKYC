import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useNavigate } from "react-router-dom";
import { ArrowLeft, Eye, EyeOff } from "lucide-react";
import { useState } from "react";
import axios from "axios";
import { toast, ToastContainer } from "react-toastify";
import { VerifyOTP } from "@/components/ui/VerifyOTP"; // Import new component
import "react-toastify/dist/ReactToastify.css";

export function LoginForm({ className, ...props }) {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [otpStep, setOtpStep] = useState(false);
  const [userId, setUserId] = useState(null); // Store user ID for OTP verification

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

      console.log("Login Response:", response.data);

      // Store access_token TEMPORARILY in sessionStorage
      sessionStorage.setItem("temp_access_token", response.data.access_token);

      // Store user ID for OTP verification
      setUserId(response.data.user_id);

      // Switch to OTP step
      setOtpStep(true);
      toast.info("OTP sent to your email", { position: "top-right" });

    } catch (err) {
      toast.error(err.response?.data?.detail || "Invalid credentials. Please try again.", { position: "top-right" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={cn("flex flex-col gap-6", className)} {...props}>
      <ToastContainer />
      <Button variant="outline" onClick={() => navigate("/")} className="w-10 h-10 rounded-full flex items-center justify-center">
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
                    <Label htmlFor="username">Email or Phone Number</Label>
                    <Input id="username" type="text" placeholder="Enter email or phone number" value={username} onChange={(e) => setUsername(e.target.value)} required />
                  </div>

                  {/* Password Input */}
                  <div className="grid gap-2 relative">
                    <Label htmlFor="password">Password</Label>
                    <div className="relative">
                      <Input id="password" type={showPassword ? "text" : "password"} value={password} placeholder="Enter Password" onChange={(e) => setPassword(e.target.value)} required />
                      <button type="button" className="absolute right-3 top-3" onClick={() => setShowPassword(!showPassword)}>
                        {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                      </button>
                    </div>
                    <a href="#" className="text-sm text-gray-600 hover:text-black font-medium self-end">Forgot your password?</a>
                  </div>

                  {/* Login Button */}
                  <Button type="submit" className="w-full" disabled={loading}>
                    {loading ? "Logging in..." : "Login"}
                  </Button>
                </>
              ) : (
                <VerifyOTP userId={userId} onSuccess={() => navigate("/")} />
              )}
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}