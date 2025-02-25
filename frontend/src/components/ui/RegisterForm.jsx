import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useNavigate } from "react-router-dom";
import { ArrowLeft } from "lucide-react";

export function RegisterForm({ className, ...props }) {
  const navigate = useNavigate();

  return (
    <div className={cn("flex flex-col gap-6", className)} {...props}>
      {/* Back Button */}
      <Button 
        variant="outline" 
        onClick={() => navigate("/")} 
        className="w-10 h-10 rounded-full flex items-center justify-center"
      >
        <ArrowLeft className="w-5 h-5" />  
      </Button>

      <Card className="w-full max-w-4xl shadow-lg relative">
        
        <CardContent className="grid grid-cols-1 md:grid-cols-2 p-0">
          {/* Left side: Registration Form */}
          <div className="p-8 flex flex-col justify-center">
            <h1 className="text-2xl font-bold text-center mb-2">Create an Account</h1>
            <p className="text-gray-500 text-center mb-6">Sign up to start using Smart KYC</p>

            <form className="space-y-4">
              {/* Full Name */}
              <div>
                <Label htmlFor="full_name">Full Name</Label>
                <Input id="full_name" type="text" placeholder="John Doe" required />
              </div>

              {/* Email */}
              <div>
                <Label htmlFor="email">Email</Label>
                <Input id="email" type="email" placeholder="john.doe@example.com" required />
              </div>

              {/* Phone Number */}
              <div>
                <Label htmlFor="phone_number">Phone Number</Label>
                <Input id="phone_number" type="text" placeholder="+1234567890" required />
              </div>

              {/* DOB & Gender in One Row */}
              <div className="grid grid-cols-2 gap-4">
                {/* Date of Birth */}
                <div>
                  <Label htmlFor="dob">Date of Birth</Label>
                  <Input id="dob" type="date" required />
                </div>

                {/* Gender */}
                <div>
                  <Label htmlFor="gender">Gender</Label>
                  <select id="gender" className="border p-2 rounded-md w-full" required>
                    <option value="">Select Gender</option>
                    <option value="1">Male</option>
                    <option value="2">Female</option>
                    <option value="3">Other</option>
                  </select>
                </div>
              </div>

              {/* Password */}
              <div>
                <Label htmlFor="password">Password</Label>
                <Input id="password" type="password" required />
              </div>

              {/* Submit Button */}
              <Button type="submit" className="w-full">Register</Button>

              {/* Already have an account? */}
              <p className="text-center text-sm text-gray-600">
                Already have an account?{" "}
                <span 
                  onClick={() => navigate("/login")} 
                  className="font-semibold text-black hover:underline cursor-pointer"
                >
                  Login
                </span>
              </p>
            </form>
          </div>

          {/* Right side: Image */}
          <div className="hidden md:flex items-center justify-center bg-white-100 p-4">
            <img 
              src="login-illustration.png" 
              alt="Register Illustration" 
              className="w-3/4 h-auto max-w-xs object-contain"
            />
          </div>

        </CardContent>
      </Card>
    </div>
  );
}
