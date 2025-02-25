import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useNavigate } from "react-router-dom";
import { ArrowLeft, Eye, EyeOff } from "lucide-react"; // Import Eye and EyeOff icons
import { useState } from "react";
import axios from "axios";
import { toast, ToastContainer } from "react-toastify"; // Import Toastify
import "react-toastify/dist/ReactToastify.css"; // Import the CSS for Toastify

export function LoginForm({ className, ...props }) {
  const navigate = useNavigate();

  // State to manage form fields and errors
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [showPassword, setShowPassword] = useState(false); // State to toggle password visibility

  // Handle form submission
  const handleLogin = async (e) => {
    e.preventDefault();

    // Prepare form data to send
    const formData = new FormData();
    formData.append("username", username);  // username could be email or phone number
    formData.append("password", password);

    try {
      // Send the form data to the backend
      const response = await axios.post("http://localhost:8000/auth/login", formData, {
        headers: {
          "Content-Type": "multipart/form-data",  // Send as form data
        },
      });

      console.log(response.data);

      // Save token in cookies if login is successful
      document.cookie = `access_token=${response.data.access_token}; path=/`;

      // Show success message
      toast.success("Login successful! Redirecting...", { position: "top-right" });

      // Redirect to the main page after a short delay
      setTimeout(() => {
        navigate("/");
      }, 2000);
    } catch (err) {
      // Handle errors, such as invalid credentials
      const errorMessage = err.response?.data?.detail || "Invalid credentials. Please try again.";

      // Show error message
      toast.error(errorMessage, { position: "top-right" });
    }
  };

  return (
    <div className={cn("flex flex-col gap-6", className)} {...props}>
      <ToastContainer /> {/* Include ToastContainer for showing toasts */}

      {/* Back Button */}
      <Button
        variant="outline"
        onClick={() => navigate("/")}
        className="w-10 h-10 rounded-full flex items-center justify-center"
      >
        <ArrowLeft className="w-5 h-5" />
      </Button>
      <Card className="overflow-hidden">
        <CardContent className="grid p-0 md:grid-cols-2">
          {/* Left side: Login Form */}
          <form className="p-6 md:p-8" onSubmit={handleLogin}>
            <div className="flex flex-col gap-6">
              <div className="flex flex-col items-center text-center">
                <h1 className="text-2xl font-bold">Welcome back</h1>
                <p className="text-gray-500">Login to your account</p>
              </div>
              <div className="grid gap-2">
                <Label htmlFor="username">Email or Phone Number</Label>
                <Input
                  id="username"
                  type="text"
                  placeholder="Enter email or phone number"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                />
              </div>
              <div className="grid gap-2 relative">
                <Label htmlFor="password">Password</Label>
                <div className="relative">
                  <Input
                    id="password"
                    type={showPassword ? "text" : "password"} // Toggle between text and password input type
                    value={password}
                    placeholder="Enter Password"
                    onChange={(e) => setPassword(e.target.value)}
                    required
                  />
                  {/* Eye Button for toggling password visibility */}
                  <button
                    type="button"
                    className="absolute right-3 top-3"
                    onClick={() => setShowPassword(!showPassword)} // Toggle the state on button click
                  >
                    {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
                <a href="#" className="text-sm text-gray-600 hover:text-black font-medium self-end">
                  Forgot your password?
                </a>
              </div>

              {/* Show error message if login fails */}
              {error && <p className="text-red-500 text-center">{error}</p>}

              <Button type="submit" className="w-full">Login</Button>

              {/* Sign Up Link */}
              <p className="text-center text-xs text-gray-600">
                Don't have an account?{" "}
                <a
                  href="#"
                  className="font-semibold text-black hover:underline cursor-pointer"
                  onClick={() => navigate("/register")}
                >
                  Sign up
                </a>
              </p>
            </div>
          </form>

          {/* Right side: Image */}
          <div className="hidden md:flex items-center justify-center bg-gray-100">
            <img
              src="/login-illustration.png"
              alt="Login Illustration"
              className="w-full h-full object-cover"
            />
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
