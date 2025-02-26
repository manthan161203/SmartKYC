import { useState } from "react";
import axios from "axios";
import { toast } from "react-toastify";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent } from "@/components/ui/card";

export function ForgotPasswordPopup({ isOpen, onClose }) {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);

  const handleForgotPassword = async () => {
    if (!email) {
      toast.error("Please enter your email.");
      return;
    }

    setLoading(true);
    try {
      await axios.post("http://localhost:8000/auth/forgot-password", { email });
      toast.success("Password reset link sent! Check your email.");
      onClose();
    } catch (err) {
      toast.error(err.response?.data?.detail || "Failed to send reset link.");
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
      <Card className="w-[90%] max-w-sm bg-white p-6 rounded-lg shadow-md">
        <CardContent>
          <h4 className="text-lg font-semibold text-center mb-4">Forgot Password</h4>
          <Label htmlFor="email">Enter your email</Label>
          <Input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="you@example.com"
            className="w-full mb-4"
          />
          <Button onClick={handleForgotPassword} disabled={loading} className="w-full">
            {loading ? "Sending..." : "Send Reset Link"}
          </Button>
          <Button variant="outline" onClick={onClose} className="w-full mt-2">
            Cancel
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}