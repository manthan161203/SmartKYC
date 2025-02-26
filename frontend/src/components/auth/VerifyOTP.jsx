import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { toast } from "react-toastify";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { REGEXP_ONLY_DIGITS_AND_CHARS } from "input-otp";
import { InputOTP, InputOTPGroup, InputOTPSlot } from "@/components/ui/input-otp";
import { getAccessToken } from "@/utils/getAccessToken";
import { Loader2 } from "lucide-react";
import "react-toastify/dist/ReactToastify.css";

export function VerifyOTP({ userId }) {
  const [otpCode, setOtpCode] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleVerifyOTP = async () => {
    if (otpCode.length !== 6) {
      toast.error("Please enter a valid 6-digit OTP.", { position: "top-right" });
      return;
    }

    setLoading(true);

    setTimeout(async () => {
      try {
        const token = getAccessToken();
        if (!token) {
          toast.error("Unauthorized! No access token found.", { position: "top-right" });
          setLoading(false);
          return;
        }

        await axios.post(
          "http://localhost:8000/auth/verify-otp",
          { user_id: userId, otp_code: otpCode },
          { headers: { Authorization: `Bearer ${token}` } }
        );

        navigate("/"); // ✅ Redirect on success
      } catch (err) {
        const errorMessage = err.response?.data?.detail || "An unexpected error occurred.";
        toast.error(errorMessage, { position: "top-right" }); // ✅ Show error in toast
      } finally {
        setLoading(false);
      }
    }, 2500);
  };

  return (
    <div className="flex flex-col gap-4">
      <Label htmlFor="otp">Enter OTP</Label>
      <InputOTP
        maxLength={6}
        pattern={REGEXP_ONLY_DIGITS_AND_CHARS}
        value={otpCode}
        onChange={setOtpCode}
        disabled={loading} // ✅ Disable input during verification
      >
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
        {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Verify OTP"}
      </Button>
    </div>
  );
}
