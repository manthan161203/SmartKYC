import { useState } from "react";
import { useNavigate } from "react-router-dom";
import UploadStep from "@/components/ui/UploadStep";
import Navbar from "@/components/ui/Navbar";
import { Button } from "@/components/ui/button";
import { ArrowRight, Loader2 } from "lucide-react"; // 🔥 Import Loader2 for a loading spinner
import api from "@/utils/api";
import { toast } from "react-toastify";

export default function DocumentUploadPage() {
    const [step, setStep] = useState(1);
    const [isUploadComplete, setIsUploadComplete] = useState(false);
    const [resetUpload, setResetUpload] = useState(false);
    const [loading, setLoading] = useState(false); // 🔥 Track loading state
    const navigate = useNavigate();

    const steps = [
        { id: 1, title: "Upload Aadhaar Front" },
        { id: 2, title: "Upload Aadhaar Back" },
        { id: 3, title: "Upload PAN Card" },
        { id: 4, title: "Upload Selfie" },
    ];

    const handleNext = async () => {
        if (step < steps.length) {
            setStep(step + 1);
            setIsUploadComplete(false);
            setResetUpload(true);
        } else {
            await handleVerifyKYC(); // 🔥 Call API when "Finish" is clicked
        }
    };

    const handleVerifyKYC = async () => {
        setLoading(true); // 🔥 Show loader before API call
        try {
            const response = await api.post("/verify_kyc/");
            toast.success("KYC Verified Successfully! ✅");
            setTimeout(() => {
                navigate("/"); // 🔥 Redirect after success
            }, 1500); // Small delay for better UX
        } catch (error) {
            console.error("KYC Verification Failed:", error);
            toast.error(error.response?.data?.detail || "KYC Verification Failed. Try again.");
        } finally {
            setLoading(false); // 🔥 Hide loader after API call completes
        }
    };

    return (
        <div>
            {/* Fixed Navbar */}
            <div className="fixed top-0 left-0 w-full bg-white shadow-md z-50">
                <Navbar />
            </div>

            <div className="flex min-h-screen flex-col items-center justify-center bg-muted p-6 md:p-10">
                <div className="w-full max-w-sm md:max-w-3xl pt-20">
                    {/* Progress Indicator */}
                    <div className="flex justify-center space-x-2 mb-6">
                        {steps.map((s) => (
                            <div
                                key={s.id}
                                className={`w-8 h-8 rounded-full flex items-center justify-center text-sm 
                                ${s.id < step ? "bg-black text-white" : s.id === step ? "bg-black text-white" : "bg-white text-black border border-black"}`}
                            >
                                {s.id}
                            </div>
                        ))}
                    </div>

                    {/* Upload Step */}
                    <UploadStep
                        step={steps[step - 1].id}
                        title={steps[step - 1].title}
                        onUploadComplete={() => setIsUploadComplete(true)}
                        resetUpload={resetUpload}
                        onResetHandled={() => setResetUpload(false)}
                    />

                    {/* Next Button */}
                    <div className="flex justify-end w-full px-5 mt-6">
                        <Button 
                            onClick={handleNext} 
                            className="w-full flex items-center justify-center" 
                            disabled={!isUploadComplete || loading} // 🔥 Disable when loading
                        >
                            {loading ? (
                                <>
                                    <Loader2 className="animate-spin w-5 h-5 mr-2" /> Processing...
                                </>
                            ) : step < steps.length ? (
                                <>
                                    Next <ArrowRight className="w-5 h-5" />
                                </>
                            ) : (
                                "Finish"
                            )}
                        </Button>
                    </div>
                </div>
            </div>
        </div>
    );
}