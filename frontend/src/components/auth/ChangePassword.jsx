import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent } from "@/components/ui/card";
import { ArrowLeft, Eye, EyeOff, Loader2 } from "lucide-react";
import { toast, ToastContainer } from "react-toastify";
import api from "@/utils/api";
import { getAccessToken } from "@/utils/getAccessToken";

export function ChangePassword() {
    const navigate = useNavigate();

    // Form states
    const [currentPassword, setCurrentPassword] = useState("");
    const [newPassword, setNewPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [showPassword, setShowPassword] = useState(false);
    const [loading, setLoading] = useState(false);

    // API Call to Change Password
    const handleChangePassword = async (e) => {
        e.preventDefault();

        if (!currentPassword || !newPassword || !confirmPassword) {
            toast.error("All fields are required.");
            return;
        }

        if (newPassword !== confirmPassword) {
            toast.error("New passwords do not match.");
            return;
        }

        setLoading(true);
        try {
            await api.post(
                "/auth/change-password",
                {
                    current_password: currentPassword,
                    new_password: newPassword,
                    confirm_new_password: confirmPassword,
                },
                {
                    headers: {
                        Authorization: `Bearer ${getAccessToken()}`, // ✅ Explicitly setting the token
                        "Content-Type": "application/json",
                    },
                }
            );

            toast.success("Password changed successfully! Redirecting...");
            setTimeout(() => navigate("/"), 2000);
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
            <Button
                variant="outline"
                onClick={() => navigate("/profile")}
                className="w-10 h-10 rounded-full flex items-center justify-center"
            >
                <ArrowLeft className="w-5 h-5" />
            </Button>

            {/* Card UI */}
            <Card className="overflow-hidden">
                <CardContent className="grid p-0 md:grid-cols-2">
                    {/* Form Section */}
                    <form className="p-6 md:p-8" onSubmit={handleChangePassword}>
                        <div className="flex flex-col gap-6">
                            <div className="flex flex-col items-center text-center">
                                <h1 className="text-2xl font-bold">Change Password</h1>
                                <p className="text-gray-500">Update your account password</p>
                            </div>

                            {/* Current Password */}
                            <div className="grid gap-2">
                                <Label htmlFor="current-password">Current Password</Label>
                                <Input
                                    id="current-password"
                                    type={showPassword ? "text" : "password"}
                                    value={currentPassword}
                                    placeholder="Enter current password"
                                    onChange={(e) => setCurrentPassword(e.target.value)}
                                    disabled={loading}
                                    required
                                />
                            </div>

                            {/* New Password */}
                            <div className="grid gap-2">
                                <Label htmlFor="new-password">New Password</Label>
                                <div className="relative">
                                    <Input
                                        id="new-password"
                                        type={showPassword ? "text" : "password"}
                                        value={newPassword}
                                        placeholder="Enter new password"
                                        onChange={(e) => setNewPassword(e.target.value)}
                                        disabled={loading}
                                        required
                                    />
                                    <button
                                        type="button"
                                        className="absolute right-3 top-3"
                                        onClick={() => setShowPassword(!showPassword)}
                                        disabled={loading}
                                    >
                                        {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                                    </button>
                                </div>
                            </div>

                            {/* Confirm New Password */}
                            <div className="grid gap-2">
                                <Label htmlFor="confirm-password">Confirm New Password</Label>
                                <div className="relative">
                                    <Input
                                        id="confirm-password"
                                        type={showPassword ? "text" : "password"}
                                        value={confirmPassword}
                                        placeholder="Confirm new password"
                                        onChange={(e) => setConfirmPassword(e.target.value)}
                                        disabled={loading}
                                        required
                                    />
                                    <button
                                        type="button"
                                        className="absolute right-3 top-3"
                                        onClick={() => setShowPassword(!showPassword)}
                                        disabled={loading}
                                    >
                                        {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                                    </button>
                                </div>
                            </div>

                            {/* Submit Button */}
                            <Button type="submit" className="w-full" disabled={loading}>
                                {loading ? <Loader2 className="animate-spin w-5 h-5" /> : "Change Password"}
                            </Button>
                        </div>
                    </form>

                    {/* Right side: Illustration */}
                    <div className="hidden md:flex items-center justify-center bg-white-100 p-4">
                        <img
                            src="change-password-illustration.png"
                            alt="Change Password"
                            className="w-3/4 h-auto max-w-xs object-contain"
                        />
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}

export default ChangePassword;