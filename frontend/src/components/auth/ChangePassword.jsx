import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod"; // Import Zod
import PasswordStrengthBar from "react-password-strength-bar"; // Password strength
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent } from "@/components/ui/card";
import { ArrowLeft, Eye, EyeOff, Loader2 } from "lucide-react";
import { toast, ToastContainer } from "react-toastify";
import api from "@/utils/api";

// ✅ Password validation schema
const passwordSchema = z.object({
    current_password: z.string().min(1, "Current password is required"),
    new_password: z
        .string()
        .min(8, "Password must be at least 8 characters long")
        .regex(/[A-Z]/, "Password must contain at least one uppercase letter")
        .regex(/[a-z]/, "Password must contain at least one lowercase letter")
        .regex(/[0-9]/, "Password must contain at least one number")
        .regex(/[@$!%*?&]/, "Password must contain at least one special character"),
    confirm_new_password: z.string().min(1, "Confirm password is required"),
}).refine((data) => data.new_password === data.confirm_new_password, {
    message: "Passwords do not match",
    path: ["confirm_new_password"],
});

export function ChangePassword() {
    const navigate = useNavigate();
    const [showPassword, setShowPassword] = useState(false);
    const [loading, setLoading] = useState(false);

    const {
        register,
        handleSubmit,
        watch,
        setError,
        formState: { errors },
    } = useForm({
        resolver: zodResolver(passwordSchema), // ✅ Apply Zod validation
    });

    const newPassword = watch("new_password");

    const handleChangePassword = async (data) => {
        setLoading(true);
        try {
            await api.post("/auth/change-password", data);

            toast.success("Password changed successfully! Redirecting to login...");

            // ✅ Clear token and redirect to login
            document.cookie = "access_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC; Secure";
            setTimeout(() => (window.location.href = "/login"), 2000);
        } catch (err) {
            toast.error(err.response?.data?.detail || "Failed to change password.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col gap-6">
            <ToastContainer />

            {/* Back Button */}
            <Button variant="outline" onClick={() => navigate("/")} className="w-10 h-10 rounded-full flex items-center justify-center">
                <ArrowLeft className="w-5 h-5" />
            </Button>

            {/* Card UI */}
            <Card className="overflow-hidden">
                <CardContent className="grid p-0 md:grid-cols-2">
                    <form className="p-6 md:p-8" onSubmit={handleSubmit(handleChangePassword)}>
                        <div className="flex flex-col gap-6">
                            <div className="flex flex-col items-center text-center">
                                <h1 className="text-2xl font-bold">Change Password</h1>
                                <p className="text-gray-500">Update your account password</p>
                            </div>

                            {/* Current Password */}
                            <div className="grid gap-2">
                                <Label htmlFor="current-password">Current Password</Label>
                                <div className="relative">

                                    <Input id="current-password" type={showPassword ? "text" : "password"} {...register("current_password")} disabled={loading} />
                                    <button type="button" className="absolute right-3 top-3" onClick={() => setShowPassword(!showPassword)} disabled={loading}>
                                        {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                                    </button>
                                </div>
                                {errors.current_password && <p className="text-red-500 text-sm">{errors.current_password.message}</p>}
                            </div>

                            {/* New Password */}
                            <div className="grid gap-2">
                                <Label htmlFor="new-password">New Password</Label>
                                <div className="relative">
                                    <Input id="new-password" type={showPassword ? "text" : "password"} {...register("new_password")} disabled={loading} />
                                    <button type="button" className="absolute right-3 top-3" onClick={() => setShowPassword(!showPassword)} disabled={loading}>
                                        {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                                    </button>
                                </div>
                                {errors.new_password && <p className="text-red-500 text-sm">{errors.new_password.message}</p>}

                                {/* Password Strength Bar */}
                                <div className="mt-2">
                                    <PasswordStrengthBar password={newPassword} />
                                </div>
                            </div>

                            {/* Confirm New Password */}
                            <div className="grid gap-2">
                                <Label htmlFor="confirm-password">Confirm New Password</Label>
                                <div className="relative">
                                    <Input id="confirm-password" type={showPassword ? "text" : "password"} {...register("confirm_new_password")} disabled={loading} />
                                    <button type="button" className="absolute right-3 top-3" onClick={() => setShowPassword(!showPassword)} disabled={loading}>
                                        {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                                    </button>
                                </div>
                                {errors.confirm_new_password && <p className="text-red-500 text-sm">{errors.confirm_new_password.message}</p>}
                            </div>

                            {/* Submit Button */}
                            <Button type="submit" className="w-full" disabled={loading}>
                                {loading ? <Loader2 className="animate-spin w-5 h-5" /> : "Change Password"}
                            </Button>
                        </div>
                    </form>

                    {/* Right side: Illustration */}
                    <div className="hidden md:flex items-center justify-center bg-white-100 p-4">
                        <img src="login-illustration.png" alt="Change Password" className="w-3/4 h-auto max-w-xs object-contain" />
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}

export default ChangePassword;
