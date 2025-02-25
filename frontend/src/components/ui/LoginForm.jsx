import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useNavigate } from "react-router-dom";
import { ArrowLeft } from "lucide-react";

export function LoginForm({ className, ...props }) {
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
      <Card className="overflow-hidden">

        <CardContent className="grid p-0 md:grid-cols-2">
          {/* Left side: Login Form */}
          <form className="p-6 md:p-8">
            <div className="flex flex-col gap-6">
              <div className="flex flex-col items-center text-center">
                <h1 className="text-2xl font-bold">Welcome back</h1>
                <p className="text-gray-500">Login to your account</p>
              </div>
              <div className="grid gap-2">
                <Label htmlFor="email">Email</Label>
                <Input id="email" type="email" placeholder="m@example.com" required />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="password">Password</Label>
                <Input id="password" type="password" required />
                <a href="#" className="text-sm text-gray-600 hover:text-black font-medium self-end">
                  Forgot your password?
                </a>
              </div>
              <Button type="submit" className="w-full">Login</Button>

              {/* Sign Up Link */}
              <p className="text-center text-sm text-gray-600">
                Don't have an account?{" "}
                <a
                  href="#"
                  className="font-semibold text-black hover:underline"
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
