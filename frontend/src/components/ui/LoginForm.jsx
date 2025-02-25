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
import { Loading } from "@/components/ui/Loading"; // Import the loading component
import "react-toastify/dist/ReactToastify.css";

export function LoginForm({ className, ...props }) {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false); // Controls the loader display
  const [postLoginLoading, setPostLoginLoading] = useState(false); // Controls 5-second loader

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true); // Show loader while login API request is being processed

    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);

    try {
      const response = await axios.post("http://localhost:8000/auth/login", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      document.cookie = `access_token=${response.data.access_token}; path=/`;
      // toast.success("Login successful! Redirecting...", { position: "top-right" });

      // Show wonderful skeleton loader for 5 seconds before redirecting
      setLoading(false);
      setPostLoginLoading(true);
      setTimeout(() => {
        navigate("/");
      }, 3000);
    } catch (err) {
      const errorMessage = err.response?.data?.detail || "Invalid credentials. Please try again.";
      toast.error(errorMessage, { position: "top-right" });
      setLoading(false); // Hide loader if login fails
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
          {/* Show skeleton loader after login before redirecting */}
          {postLoginLoading ? (
            <div className="flex items-center justify-center w-full h-96">
              <Loading text="Redirecting to Dashboard..." size={12} />
            </div>
          ) : (
            <form className="p-6 md:p-8" onSubmit={handleLogin}>
              <div className="flex flex-col gap-6">
                <div className="flex flex-col items-center text-center">
                  <h1 className="text-2xl font-bold">Welcome back</h1>
                  <p className="text-gray-500">Login to your account</p>
                </div>

                {/* Username Input */}
                <div className="grid gap-2">
                  <Label htmlFor="username">Email or Phone Number</Label>
                  <Input id="username" type="text" placeholder="Enter email or phone number" value={username} onChange={(e) => setUsername(e.target.value)} required />
                </div>

                {/* Password Input with Eye Icon */}
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

                {/* Sign Up Link */}
                <p className="text-center text-xs text-gray-600">
                  Don't have an account?{" "}
                  <a href="#" className="font-semibold text-black hover:underline cursor-pointer" onClick={() => navigate("/register")}>Sign up</a>
                </p>
              </div>
            </form>
          )}

          {/* Right side: Image */}
          <div className="hidden md:flex items-center justify-center bg-gray-100">
            <img src="/login-illustration.png" alt="Login Illustration" className="w-full h-full object-cover" />
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
