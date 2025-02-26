import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { REGEXP_ONLY_DIGITS_AND_CHARS } from "input-otp";
import { InputOTP, InputOTPGroup, InputOTPSlot } from "@/components/ui/input-otp";
import { getAccessToken } from "@/utils/getAccessToken";
import { Loader2 } from "lucide-react";

export default function VerifyOTPPopup({ isOpen, onClose, userId }) {
  const [otpCode, setOtpCode] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleVerifyOTP = async () => {
    if (otpCode.length !== 6) {
      toast.error("Please enter a valid 6-digit OTP.");
      return;
    }

    setLoading(true);

    try {
      const token = getAccessToken();
      if (!token) {
        toast.error("Unauthorized! No access token found.");
        setLoading(false);
        return;
      }

      await axios.post(
        "http://localhost:8000/auth/verify-otp",
        { user_id: userId, otp_code: otpCode },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      toast.success("OTP verified successfully!");
      navigate("/");
    } catch (err) {
      toast.error(err.response?.data?.detail || "Invalid OTP, please try again.");
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 flex justify-center items-center z-50">
      {/* Background overlay */}
      <div className="absolute inset-0 bg-black/30 backdrop-blur-sm" onClick={onClose}></div>

      <div className="relative w-[90%] max-w-sm bg-white p-6 rounded-lg shadow-xl flex flex-col items-center">
        <h4 className="text-lg font-semibold text-center mb-4">Verify OTP</h4>
        <Label htmlFor="otp" className="mb-2 text-center">Enter OTP</Label>

        {/* Centered OTP Group & Added Gap Below */}
        <div className="flex justify-center w-full mb-6">
          <InputOTP
            maxLength={6}
            pattern={REGEXP_ONLY_DIGITS_AND_CHARS}
            value={otpCode}
            onChange={setOtpCode}
            disabled={loading}
            className="flex justify-center gap-3"
          >
            <InputOTPGroup className="flex justify-center gap-3">
              <InputOTPSlot index={0} />
              <InputOTPSlot index={1} />
              <InputOTPSlot index={2} />
              <InputOTPSlot index={3} />
              <InputOTPSlot index={4} />
              <InputOTPSlot index={5} />
            </InputOTPGroup>
          </InputOTP>
        </div>

        {/* Added Extra Gap Below OTP Box */}
        <Button onClick={handleVerifyOTP} disabled={loading} className="w-full mb-3">
          {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Verify OTP"}
        </Button>
        <Button variant="outline" onClick={onClose} className="w-full">
          Cancel
        </Button>
      </div>

    </div>
  );
}
