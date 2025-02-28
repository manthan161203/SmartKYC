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
import VerifyOTPPopup from "@/components/auth/VerifyOTPPopup";
import { toast } from "react-toastify";
import { Calendar } from "lucide-react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

const Profile = ({ isOpen, setIsOpen }) => {
    const [user, setUser] = useState(null);
    // formData holds the editable fields (including address fields mapped to top-level keys)
    const [formData, setFormData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [isEmailLoading, setIsEmailLoading] = useState(false);
    const [isPhoneLoading, setIsPhoneLoading] = useState(false);
    const [showOTPPopup, setShowOTPPopup] = useState(false);
    const [otpType, setOtpType] = useState(null);
    const [editMode, setEditMode] = useState(false);
    const [saving, setSaving] = useState(false);
    const [errors, setErrors] = useState({});

    const fetchUserProfile = async () => {
        setLoading(true);
        try {
            const response = await api.get("/user/profile", {
                headers: { Authorization: `Bearer ${getAccessToken()}` }
            });
            console.log("User Profile:", response.data);
            setUser(response.data);
            // Map address from user.addresses (first element) to top-level fields for editing
            let address =
                response.data.addresses && response.data.addresses.length > 0
                    ? response.data.addresses[0]
                    : {};
            setFormData({
                full_name: response.data.full_name || "",
                email: response.data.email || "",
                phone_number: response.data.phone_number || "",
                dob: response.data.dob || "",
                gender_id: response.data.gender_id || "",
                profile_photo: response.data.profile_photo_url || "",
                address_line1: address.address_line1 || "",
                address_line2: address.address_line2 || "",
                city: address.city || "",
                state: address.state || "",
                country: address.country || "",
                postal_code: address.postal_code || ""
            });
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
    // Use the same address from original data for display when not editing
    const address =
        user && user.addresses && user.addresses.length > 0
            ? user.addresses[0]
            : {};

    const getKYCStatus = (id) => {
        switch (id) {
            case 1:
                return { text: "Pending", color: "bg-yellow-100 text-yellow-600", icon: <MdPending size={18} /> };
            case 2:
                return { text: "Verified", color: "bg-green-100 text-green-600", icon: <MdVerified size={18} /> };
            case 3:
                return { text: "Rejected", color: "bg-red-100 text-red-600", icon: <MdCancel size={18} /> };
            default:
                return { text: "Unknown", color: "bg-gray-100 text-gray-600", icon: "" };
        }
    };

    const requestOTP = async (type) => {
        if (type === "email") setIsEmailLoading(true);
        if (type === "phone") setIsPhoneLoading(true);

        try {
            await api.post("/auth/request-otp", {}, {
                headers: { Authorization: `Bearer ${getAccessToken()}` }
            });
            toast.success(`OTP sent to your ${type}.`, { position: "top-right" });
            setOtpType(type);
            setShowOTPPopup(true);
            setIsOpen(false); // Close profile modal after OTP request is sent
        } catch (error) {
            console.error("Error requesting OTP:", error);
            toast.error(error.response?.data?.detail || "Failed to send OTP.", { position: "top-right" });
        } finally {
            if (type === "email") setIsEmailLoading(false);
            if (type === "phone") setIsPhoneLoading(false);
        }
    };

    const verifyOTP = async (otpCode) => {
        const endpoint = otpType === "email" ? "/auth/verify-email" : "/auth/verify-phone";
        try {
            await api.post(endpoint, { otp_code: otpCode }, {
                headers: { Authorization: `Bearer ${getAccessToken()}` }
            });
            toast.success("OTP verified successfully!", { position: "top-right" });
            fetchUserProfile(); // Refresh user data after verification
            setShowOTPPopup(false);
        } catch (error) {
            console.error("Error verifying OTP:", error);
            toast.error(error.response?.data?.detail || "Invalid OTP, please try again.", { position: "top-right" });
        }
    };

    // Validate form before saving changes
    const validateForm = () => {
        const newErrors = {};
        // Email must be present and in a valid format
        if (!formData.email) {
            newErrors.email = "Email is required";
        } else {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(formData.email)) {
                newErrors.email = "Invalid email address";
            }
        }
        // Phone number: check numeric part must be exactly 10 digits
        if (!formData.phone_number) {
            newErrors.phone_number = "Phone number is required";
        } else {
            const numericPart = formData.phone_number.startsWith("+91")
                ? formData.phone_number.slice(3)
                : formData.phone_number;
            const phoneRegex = /^\d{10}$/;
            if (!phoneRegex.test(numericPart)) {
                newErrors.phone_number = "Phone number must be exactly 10 digits";
            }
        }
        // DOB: must be provided and the age must be at least 18
        if (!formData.dob) {
            newErrors.dob = "Date of birth is required";
        } else {
            const dob = new Date(formData.dob);
            const today = new Date();
            let age = today.getFullYear() - dob.getFullYear();
            const m = today.getMonth() - dob.getMonth();
            if (m < 0 || (m === 0 && today.getDate() < dob.getDate())) {
                age--;
            }
            if (age < 18) {
                newErrors.dob = "You must be at least 18 years old";
            }
        }
        // Postal code (if provided) must contain only numbers
        if (formData.postal_code && !/^\d+$/.test(formData.postal_code)) {
            newErrors.postal_code = "Postal code must contain only numbers";
        }
        return newErrors;
    };

    // Update formData when inputs change in edit mode
    const handleChange = (e) => {
        const { name, value } = e.target;
        if (name === "phone_number") {
            // Remove any existing +91 prefix and then add +91
            const numericPart = value.replace(/^\+91/, "");
            setFormData({ ...formData, phone_number: "+91" + numericPart });
        } else {
            setFormData({ ...formData, [name]: value });
        }
    };

    const saveChanges = async () => {
        const errorsFound = validateForm();
        if (Object.keys(errorsFound).length > 0) {
            // Set errors and do not proceed
            setErrors(errorsFound);
            return;
        }
        setSaving(true);
        try {
            await api.put("/user/edit", formData, {
                headers: { Authorization: `Bearer ${getAccessToken()}` }
            });
            toast.success("Profile updated successfully!", { position: "top-right" });
            setEditMode(false);
            fetchUserProfile(); // refresh user data to reflect changes
        } catch (error) {
            console.error("Error updating profile:", error);
            toast.error(error.response?.data?.detail || "Failed to update profile.", { position: "top-right" });
        } finally {
            setSaving(false);
        }
    };

    return (
        <>
            <Sheet
                open={isOpen}
                onOpenChange={(open) => {
                    setIsOpen(open);
                    if (!open) setEditMode(false);
                }}
            >
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
                                            name="full_name"
                                            value={editMode ? formData.full_name : formatValue(user.full_name)}
                                            onChange={handleChange}
                                            readOnly={!editMode}
                                            className="col-span-3 bg-gray-100 pr-4"
                                        />
                                    </div>

                                    <div className="space-y-6">
                                        {/* Email Verification */}
                                        <div className="grid grid-cols-4 items-center gap-4">
                                            <Label className="text-right">Email</Label>
                                            <div className="col-span-3 flex items-center gap-2">
                                                <Input
                                                    name="email"
                                                    value={editMode ? formData.email : user.email}
                                                    onChange={handleChange}
                                                    readOnly={!editMode}
                                                    className="bg-gray-100 pr-4"
                                                />
                                                {!editMode && (
                                                    user.is_email_verified ? (
                                                        <span className="text-green-600 text-xs flex items-center gap-1">
                                                            <MdVerified size={16} /> Verified
                                                        </span>
                                                    ) : (
                                                        <Button
                                                            size="xs"
                                                            onClick={() => requestOTP("email")}
                                                            variant="outline"
                                                            className="px-2 py-2 h-auto text-xs"
                                                            disabled={isEmailLoading}
                                                        >
                                                            {isEmailLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Verify"}
                                                        </Button>
                                                    )
                                                )}
                                            </div>
                                            {editMode && errors.email && (
                                                <p className="text-red-500 text-xs col-span-4">{errors.email}</p>
                                            )}
                                        </div>


                                        {/* Phone Field */}
                                        {editMode ? (
                                            <div className="grid grid-cols-4 items-center gap-4">
                                                <Label className="text-right">Phone</Label>
                                                <div className="col-span-3 flex items-center gap-2">
                                                    <Input
                                                        id="country_code"
                                                        type="text"
                                                        value="+91"
                                                        disabled
                                                        className="text-center w-16"  // Fixed width so "+91" displays fully
                                                    />
                                                    <Input
                                                        id="phone_number"
                                                        type="text"
                                                        name="phone_number"
                                                        placeholder="Enter your phone number"
                                                        value={
                                                            formData.phone_number.startsWith("+91")
                                                                ? formData.phone_number.slice(3)
                                                                : formData.phone_number
                                                        }
                                                        onChange={handleChange}
                                                        className="flex-1"
                                                    />
                                                    {errors.phone_number && (
                                                        <p className="text-red-500 text-xs">{errors.phone_number}</p>
                                                    )}
                                                </div>
                                            </div>
                                        ) : (
                                            <div className="grid grid-cols-4 items-center gap-4">
                                                <Label className="text-right">Phone</Label>
                                                <div className="col-span-3 flex justify-start items-center gap-2">
                                                    <Input
                                                        name="phone_number"
                                                        value={user.phone_number}
                                                        readOnly
                                                        className="bg-gray-100 pr-4"
                                                    />
                                                    {user.is_phone_verified ? (
                                                        <span className="text-green-600 text-xs flex items-center gap-1">
                                                            <MdVerified size={16} /> Verified
                                                        </span>
                                                    ) : (
                                                        <Button
                                                            size="xs"
                                                            onClick={() => requestOTP("phone")}
                                                            variant="outline"
                                                            className="px-2 py-2 h-auto text-xs"
                                                            disabled={isPhoneLoading}
                                                        >
                                                            {isPhoneLoading ? (
                                                                <Loader2 className="w-4 h-4 animate-spin" />
                                                            ) : (
                                                                "Verify"
                                                            )}
                                                        </Button>
                                                    )}
                                                </div>
                                            </div>
                                        )}


                                    </div>

                                    {/* DOB */}
                                    <div className="grid grid-cols-4 items-center gap-4">
                                        <Label className="text-right">DOB</Label>
                                        <div className="col-span-3">
                                            {editMode ? (
                                                <DatePicker
                                                    selected={formData.dob ? new Date(formData.dob) : null}
                                                    onChange={(date) =>
                                                        setFormData({ ...formData, dob: date ? date.toISOString() : "" })
                                                    }
                                                    dateFormat="yyyy-MM-dd"
                                                    customInput={
                                                        <Input
                                                            name="dob"
                                                            className="bg-gray-100 pr-4"
                                                        />
                                                    }
                                                />
                                            ) : (
                                                <Input
                                                    name="dob"
                                                    type="text"
                                                    value={user.dob ? user.dob.slice(0, 10) : "-"}
                                                    readOnly
                                                    className="bg-gray-100 pr-4"
                                                />
                                            )}
                                            {editMode && errors.dob && (
                                                <p className="text-red-500 text-xs">{errors.dob}</p>
                                            )}
                                        </div>
                                    </div>


                                    {/* Gender */}
                                    <div className="grid grid-cols-4 items-center gap-4">
                                        <Label className="text-right">Gender</Label>
                                        {editMode ? (
                                            <select
                                                name="gender_id"
                                                value={formData.gender_id}
                                                onChange={handleChange}
                                                className="col-span-3 bg-gray-100 pr-4 py-2 border rounded"
                                            >
                                                <option value="">Select Gender</option>
                                                <option value="1">Male</option>
                                                <option value="2">Female</option>
                                                <option value="3">Other</option>
                                            </select>
                                        ) : (
                                            <Input
                                                value={user.gender_id === 1 ? "Male" : user.gender_id === 2 ? "Female" : "-"}
                                                readOnly
                                                className="col-span-3 bg-gray-100 pr-4"
                                            />
                                        )}
                                    </div>
                                </div>

                                {/* KYC Status (Always read-only) */}
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
                                            <Input
                                                name="address_line1"
                                                value={editMode ? formData.address_line1 : formatValue(address.address_line1)}
                                                onChange={handleChange}
                                                readOnly={!editMode}
                                                className="col-span-3 bg-gray-100 pr-4"
                                            />
                                        </div>
                                        <div className="grid grid-cols-4 items-center gap-4">
                                            <Label className="text-right">Add. Line 2</Label>
                                            <Input
                                                name="address_line2"
                                                value={editMode ? formData.address_line2 : formatValue(address.address_line2)}
                                                onChange={handleChange}
                                                readOnly={!editMode}
                                                className="col-span-3 bg-gray-100 pr-4"
                                            />
                                        </div>
                                        <div className="grid grid-cols-4 items-center gap-4">
                                            <Label className="text-right">City</Label>
                                            <Input
                                                name="city"
                                                value={editMode ? formData.city : formatValue(address.city)}
                                                onChange={handleChange}
                                                readOnly={!editMode}
                                                className="col-span-3 bg-gray-100 pr-4"
                                            />
                                        </div>
                                        <div className="grid grid-cols-4 items-center gap-4">
                                            <Label className="text-right">State</Label>
                                            <Input
                                                name="state"
                                                value={editMode ? formData.state : formatValue(address.state)}
                                                onChange={handleChange}
                                                readOnly={!editMode}
                                                className="col-span-3 bg-gray-100 pr-4"
                                            />
                                        </div>
                                        <div className="grid grid-cols-4 items-center gap-4">
                                            <Label className="text-right">Country</Label>
                                            <Input
                                                name="country"
                                                value={editMode ? formData.country : formatValue(address.country)}
                                                onChange={handleChange}
                                                readOnly={!editMode}
                                                className="col-span-3 bg-gray-100 pr-4"
                                            />
                                        </div>
                                        <div className="grid grid-cols-4 items-center gap-4">
                                            <Label className="text-right">Pin Code</Label>
                                            <div className="col-span-3 flex flex-col gap-1">
                                                <Input
                                                    name="postal_code"
                                                    value={editMode ? formData.postal_code : formatValue(address.postal_code)}
                                                    onChange={handleChange}
                                                    readOnly={!editMode}
                                                    className="bg-gray-100 pr-4"
                                                />
                                                {editMode && errors.postal_code && (
                                                    <p className="text-red-500 text-xs">{errors.postal_code}</p>
                                                )}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* Edit / Save Buttons */}
                            <div className="flex justify-center mt-6 pb-6">
                                {editMode ? (
                                    <>
                                        <Button className="w-[120px] py-2 text-sm mr-2" onClick={saveChanges}>
                                            {saving ? <Loader2 className="w-4 h-4 animate-spin" /> : "Save Changes"}
                                        </Button>
                                        <Button className="w-[120px] py-2 text-sm" variant="outline" onClick={() => setEditMode(false)}>
                                            Cancel
                                        </Button>
                                    </>
                                ) : (
                                    <Button className="w-[250px] py-2 text-sm" onClick={() => setEditMode(true)}>
                                        Edit Profile
                                    </Button>
                                )}
                            </div>
                        </>
                    ) : (
                        <p className="text-gray-400 text-center py-4">No profile data found.</p>
                    )}
                </SheetContent>
            </Sheet>

            {/* OTP Verification Popup */}
            <VerifyOTPPopup
                isOpen={showOTPPopup}
                onClose={() => setShowOTPPopup(false)}
                onVerifySuccess={verifyOTP}
            />
        </>
    );
};

export default Profile;
