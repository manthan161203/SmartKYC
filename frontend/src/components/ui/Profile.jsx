import { useState, useEffect } from "react";
import { MdPending, MdVerified, MdCancel } from "react-icons/md";
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
import { Loader2 } from "lucide-react";
import api from "@/utils/api";
import { getAccessToken } from "@/utils/getAccessToken";

const Profile = ({ isOpen, setIsOpen }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(false);

    const fetchUserProfile = async () => {
        setLoading(true);
        try {
            const response = await api.get("/user/profile", {
                headers: { Authorization: `Bearer ${getAccessToken()}` },
            });
            console.log("User Profile:", response.data);
            setUser(response.data);
        } catch (error) {
            console.error("Error fetching user profile:", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (isOpen) {
            fetchUserProfile();
        }
    }, [isOpen]);

    const formatValue = (value) => (value ? value : "-");
    const address = user?.addresses?.length > 0 ? user.addresses[0] : {};

    const getKYCStatus = (id) => {
        switch (id) {
            case 1:
                return { text: "Pending", color: "bg-yellow-100 text-yellow-600", icon: <MdPending size={18} /> };
            case 2:
                return { text: "Verified", color: "bg-green-100 text-green-600", icon: <MdVerified size={18} /> };
            case 3:
                return { text: "Rejected", color: "bg-red-100 text-red-600", icon: <MdCancel size={18} /> };
            default:
                return { text: "Unknown", color: "bg-gray-100 text-gray-600", icon: "❓" };
        }
    };

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

    const getInitials = (name) => {
        if (!name) return "?";
        const words = name.split(" ");
        return words.map(word => word[0]?.toUpperCase()).join("");
    };

    return (
        <Sheet open={isOpen} onOpenChange={setIsOpen}>
            <SheetContent className="max-h-screen overflow-y-auto max-w-[600px] w-full">
                <SheetHeader>
                    <SheetTitle>Profile</SheetTitle>
                    <SheetDescription>View your profile details.</SheetDescription>
                </SheetHeader>

                {loading ? (
                    <div className="flex justify-center items-center h-32">
                        <Loader2 className="animate-spin text-gray-500 w-10 h-10" />
                    </div>
                ) : user ? (
                    <>
                        {/* Profile Image */}
                        <div className="flex items-center justify-center py-4">
                            {user?.profile_photo_url ? (
                                <img
                                    src={user.profile_photo_url}
                                    alt="Profile"
                                    className="w-24 h-24 rounded-full object-cover border border-gray-300 shadow-sm"
                                />
                            ) : (
                                <img
                                    src={user?.gender_id === 2 ? "/female.png" : "/male.png"}
                                    alt="Default Profile"
                                    className="w-24 h-24 rounded-full object-cover border border-gray-300 shadow-sm"
                                />
                            )}
                        </div>

                        <div className="space-y-6 pr-4">
                            {/* Basic Details */}
                            <div className="grid gap-4">
                                <div className="grid grid-cols-4 items-center gap-4">
                                    <Label className="text-right">Full Name</Label>
                                    <Input
                                        value={formatValue(user.full_name)}
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
                                            <Button size="xs" onClick={handleVerifyEmail} variant="outline" className="px-2 py-2 h-auto text-xs">
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

                                <div className="grid grid-cols-4 items-center gap-4">
                                    <Label className="text-right">Gender</Label>
                                    <Input
                                        value={user.gender_id === 1 ? "Male" : user.gender_id === 2 ? "Female" : "-"}
                                        readOnly
                                        className="col-span-3 bg-gray-100 pr-4"
                                    />
                                </div>
                            </div>
                            {/* KYC Status */}
                            <div className="grid grid-cols-4 items-center gap-4">
                                <Label className="text-right">KYC Status</Label>
                                <div className={`col-span-3 flex items-center gap-2 px-3 py-1 rounded-full font-medium ${getKYCStatus(user.kyc_status_id).color}`}>
                                    {getKYCStatus(user.kyc_status_id).icon}
                                    {getKYCStatus(user.kyc_status_id).text}
                                </div>
                            </div>

                            {/* Address Section */}
                            <div className="border-t pt-4">
                                <SheetHeader>
                                    <SheetTitle>Address</SheetTitle>
                                </SheetHeader>
                                <div className="grid gap-4 mt-2">
                                    <div className="grid grid-cols-4 items-center gap-4">
                                        <Label className="text-right">Add. Line 1</Label>
                                        <Input value={formatValue(address.address_line1)} readOnly className="col-span-3 bg-gray-100 pr-4" />
                                    </div>
                                    <div className="grid grid-cols-4 items-center gap-4">
                                        <Label className="text-right">Add. Line 2</Label>
                                        <Input value={formatValue(address.address_line2)} readOnly className="col-span-3 bg-gray-100 pr-4" />
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
                                    <div className="grid grid-cols-4 items-center gap-4">
                                        <Label className="text-right">Pin Code</Label>
                                        <Input value={formatValue(address.postal_code)} readOnly className="col-span-3 bg-gray-100 pr-4" />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </>
                ) : (
                    <p className="text-gray-400 text-center py-4">No profile data found.</p>
                )}
                {/* Edit Profile Button */}
                <div className="flex justify-center mt-6 pb-6">
                    <Button className="w-[250px] py-2 text-sm">
                        Edit Profile
                    </Button>
                </div>
            </SheetContent>
        </Sheet>
    );
};

export default Profile;
