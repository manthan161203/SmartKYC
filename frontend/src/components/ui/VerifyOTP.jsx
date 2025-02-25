import { useState } from "react";
import { toast } from "react-toastify";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { REGEXP_ONLY_DIGITS_AND_CHARS } from "input-otp";
import { InputOTP, InputOTPGroup, InputOTPSlot } from "@/components/ui/input-otp";

export function VerifyOTP({ userId, onSuccess }) {
  const [otpCode, setOtpCode] = useState("");
  const [loading, setLoading] = useState(false);

  const handleVerifyOTP = async () => {
    if (otpCode.length !== 6) {
      toast.error("Please enter a valid 6-digit OTP.", { position: "top-right" });
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post("http://localhost:8000/auth/verify-otp", {
        user_id: userId,
        otp_code: otpCode,
      });

      console.log("OTP Verification Response:", response.data);

      // Retrieve the temporarily stored token
      const tempToken = sessionStorage.getItem("temp_access_token");

      if (!tempToken) {
        toast.error("Session expired. Please log in again.", { position: "top-right" });
        return;
      }

      // Store access_token in cookies (WITHOUT HttpOnly)
      document.cookie = `access_token=${tempToken}; path=/; Secure`;

      // Clear temporary token
      sessionStorage.removeItem("temp_access_token");

      toast.success("OTP Verified! Redirecting...", { position: "top-right" });
      onSuccess(); // Call the success function (navigate to dashboard, etc.)
    } catch (err) {
      toast.error(err.response?.data?.detail || "Invalid OTP. Try again.", { position: "top-right" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col gap-4">
      <Label htmlFor="otp">Enter OTP</Label>
      <InputOTP maxLength={6} pattern={REGEXP_ONLY_DIGITS_AND_CHARS} value={otpCode} onChange={setOtpCode}>
        <InputOTPGroup>
          <InputOTPSlot index={0} />
          <InputOTPSlot index={1} />
          <InputOTPSlot index={2} />
          <InputOTPSlot index={3} />
          <InputOTPSlot index={4} />
          <InputOTPSlot index={5} />
        </InputOTPGroup>
      </InputOTP>

      <Button type="button" onClick={handleVerifyOTP} className="w-full" disabled={loading}>
        {loading ? "Verifying..." : "Verify OTP"}
      </Button>
    </div>
  );
}