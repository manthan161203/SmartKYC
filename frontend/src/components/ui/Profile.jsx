import { useState, useEffect } from "react";
import { MdVerified } from "react-icons/md";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
    Sheet,
    SheetContent,
    SheetHeader,
    SheetTitle,
    SheetDescription
} from "@/components/ui/sheet";
import api from "@/utils/api";
import { getAccessToken } from "@/utils/getAccessToken";

const Profile = ({ isOpen, setIsOpen }) => {
    const [user, setUser] = useState(null);

    const fetchUserProfile = async () => {
        try {
            const response = await api.get("/user/profile", {
                headers: { Authorization: `Bearer ${getAccessToken()}` },
            });
            console.log("User Profile:", response.data);
            setUser(response.data);
        } catch (error) {
            console.error("Error fetching user profile:", error);
        }
    };

    useEffect(() => {
        if (isOpen) {
            fetchUserProfile();
        }
    }, [isOpen]);

    const formatValue = (value) => (value ? value : "-");
    const address = user?.addresses?.length > 0 ? user.addresses[0] : {};

    const handleVerifyEmail = async () => {
        try {
            await api.post("/user/verify-email", {}, {
                headers: { Authorization: `Bearer ${getAccessToken()}` },
            });
            alert("Verification email sent!");
        } catch (error) {
            console.error("Error sending verification email:", error);
        }
    };

    const handleVerifyPhone = async () => {
        try {
            await api.post("/user/verify-phone", {}, {
                headers: { Authorization: `Bearer ${getAccessToken()}` },
            });
            alert("Verification OTP sent!");
        } catch (error) {
            console.error("Error sending phone verification:", error);
        }
    };

    return (
        <Sheet open={isOpen} onOpenChange={setIsOpen}>
            <SheetContent>
                <SheetHeader>
                    <SheetTitle>Profile</SheetTitle>
                    <SheetDescription>View your profile details.</SheetDescription>
                </SheetHeader>

                {user ? (
                    <div className="space-y-6 pr-4">
                        {/* Basic Details */}
                        <div className="grid gap-4">
                            <div className="grid grid-cols-4 items-center gap-4">
                                <Label className="text-right">Full Name</Label>
                                <Input
                                    value={formatValue(user.full_name?.replace("undefined", "").trim())}
                                    readOnly
                                    className="col-span-3 bg-gray-100 pr-4"
                                />
                            </div>

                            {/* Email with Verification */}
                            <div className="grid grid-cols-4 items-center gap-4">
                                <Label className="text-right">Email</Label>
                                <div className="col-span-3 flex justify-start items-center gap-2">
                                    <Input value={formatValue(user.email)} readOnly className="bg-gray-100 pr-4" />
                                    {user.is_email_verified ? (
                                        <span className="text-green-600 text-xs flex items-center gap-1">
                                            <MdVerified size={16} /> Verified
                                        </span>
                                    ) : (
                                        <Button size="xs" onClick={handleVerifyEmail} variant="outline" className="px-2 py-2 h-full text-xs h-auto">
                                            Verify
                                        </Button>
                                    )}
                                </div>
                            </div>

                            {/* Phone with Verification */}
                            <div className="grid grid-cols-4 items-center gap-4">
                                <Label className="text-right">Phone</Label>
                                <div className="col-span-3 flex items-center gap-2">
                                    <Input value={formatValue(user.phone_number)} readOnly className="bg-gray-100 pr-4" />
                                    {user.is_phone_verified ? (
                                        <span className="text-green-600 text-xs flex items-center gap-1">
                                            <MdVerified size={16} /> Verified
                                        </span>
                                    ) : (
                                        <Button size="xs" onClick={handleVerifyPhone} variant="outline" className="px-2 py-2 text-xs">
                                            Verify
                                        </Button>
                                    )}
                                </div>
                            </div>

                            {/* DOB */}
                            <div className="grid grid-cols-4 items-center gap-4">
                                <Label className="text-right">DOB</Label>
                                <Input
                                    value={user.dob ? new Date(user.dob).toLocaleDateString() : "-"}
                                    readOnly
                                    className="col-span-3 bg-gray-100 pr-4"
                                />
                            </div>
                        </div>

                        {/* Address Section */}
                        <div className="border-t pt-4">
                            <h3 className="text-lg font-semibold text-gray-700">Address</h3>
                            <div className="grid gap-4 mt-2">
                                <div className="grid grid-cols-4 items-center gap-4">
                                    <Label className="text-right">Street</Label>
                                    <Input value={formatValue(address.street)} readOnly className="col-span-3 bg-gray-100 pr-4" />
                                </div>
                                <div className="grid grid-cols-4 items-center gap-4">
                                    <Label className="text-right">City</Label>
                                    <Input value={formatValue(address.city)} readOnly className="col-span-3 bg-gray-100 pr-4" />
                                </div>
                                <div className="grid grid-cols-4 items-center gap-4">
                                    <Label className="text-right">State</Label>
                                    <Input value={formatValue(address.state)} readOnly className="col-span-3 bg-gray-100 pr-4" />
                                </div>
                                <div className="grid grid-cols-4 items-center gap-4">
                                    <Label className="text-right">Country</Label>
                                    <Input value={formatValue(address.country)} readOnly className="col-span-3 bg-gray-100 pr-4" />
                                </div>
                            </div>
                        </div>
                    </div>
                ) : (
                    <p className="text-gray-400">Loading profile...</p>
                )}
            </SheetContent>
        </Sheet>
    );
};

export default Profile;