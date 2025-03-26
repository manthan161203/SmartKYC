import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "@/utils/api";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { ArrowLeft, Loader2 } from "lucide-react";
export default function UploadStep({ step, title, onUploadComplete, resetUpload, onResetHandled }) {
    const navigate = useNavigate();
    const [selectedFile, setSelectedFile] = useState(null);
    const [preview, setPreview] = useState(null);
    const [isUploading, setIsUploading] = useState(false);
    const [extractedData, setExtractedData] = useState(null);
    const [showPopup, setShowPopup] = useState(false);

    useEffect(() => {
        if (resetUpload) {
            setSelectedFile(null);
            setPreview(null);
            setExtractedData(null);
            setShowPopup(false);
            onResetHandled();
        }
    }, [resetUpload, onResetHandled]);

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        if (!file) return;

        setSelectedFile(file);

        // Preview image
        const reader = new FileReader();
        reader.onload = () => setPreview(reader.result);
        reader.readAsDataURL(file);
    };

    const handleUpload = async () => {
        if (!selectedFile) {
            toast.warn("Please select a file before uploading.");
            return;
        }

        setIsUploading(true);

        const formData = new FormData();
        formData.append("file", selectedFile);
        formData.append("document_type_id", step);

        try {
            const response = await api.post("/document_store_and_process/upload", formData, {
                headers: { "Content-Type": "multipart/form-data" },
            });

            toast.success(response.data.message);
            onUploadComplete();

            // 🔥 Skip Extraction & Verification for Step 4 (Selfie)
            if (step !== 4) {
                handleUploadSuccess();
            }
        } catch (error) {
            console.error("Upload Error:", error.response?.data);
            toast.error(error.response?.data?.detail || "Upload failed. Try again.");
        } finally {
            setTimeout(() => setIsUploading(false), 2000);
        }
    };

    const handleUploadSuccess = async () => {
        if (step === 4) return; // 🚀 Skip Extraction for Selfie

        try {
            const response = await api.post("/extract_details/", {
                document_type_id: step,
            });

            setExtractedData(response.data);
            setShowPopup(true);
        } catch (error) {
            console.error("Error extracting document details:", error);
            toast.error("Failed to extract details. Please try again.");
        }
    };

    const handleVerify = async () => {
        if (step === 4) return; // 🚀 Skip Verification for Selfie

        try {
            await api.patch("/verify_document/", {
                document_type_id: step,
            });

            toast.success("Document Verified Successfully! ✅");
            setShowPopup(false);
        } catch (error) {
            console.error("Error verifying document:", error);
            toast.error("Verification failed. Please try again.");
        }
    };

    return (
        <div className="flex flex-col gap-6 items-center w-full px-4">
            <ToastContainer />

            {/* Back Button */}
            <div className="w-full flex justify-start max-w-4xl">
                <Button
                    variant="outline"
                    onClick={() => navigate(-1)}
                    className="w-10 h-10 rounded-full flex items-center justify-center"
                    disabled={isUploading}
                >
                    <ArrowLeft className="w-5 h-5" />
                </Button>
            </div>

            {/* Upload Card */}
            <Card className="w-full max-w-4xl shadow-lg overflow-hidden">
                <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-8 p-10 items-center">
                    {/* Left Side: Upload Form */}
                    <div className="flex flex-col gap-6 w-full">
                        <h2 className="text-2xl font-semibold text-center">{title}</h2>

                        {preview && (
                            <div className="flex justify-center">
                                <img
                                    src={preview}
                                    alt="Preview"
                                    className="max-w-full max-h-64 rounded-md shadow-md object-contain"
                                />
                            </div>
                        )}

                        <div>
                            <Label htmlFor="file" className="text-lg">Upload Document</Label>
                            <Input id="file" type="file" accept="image/*" onChange={handleFileChange} disabled={isUploading} />
                        </div>

                        {/* Upload Button */}
                        <Button type="button" onClick={handleUpload} className="w-full py-2 text-lg" disabled={isUploading}>
                            {isUploading ? <Loader2 className="w-6 h-6 animate-spin" /> : "Upload & Process"}
                        </Button>
                    </div>

                    {/* Right Side: Illustration */}
                    <div className="hidden md:flex items-center justify-center bg-gray-100 p-6">
                        <img src="/aadhaar-card.jpg" alt="Upload Illustration" className="w-4/5 h-auto max-w-sm object-contain" />
                    </div>
                </CardContent>
            </Card>

            {/* Extracted Details Popup */}
            {showPopup && extractedData && step !== 4 && (
                <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 p-4">
                    <div className="bg-white rounded-lg shadow-lg p-6 max-w-lg w-full">
                        <h2 className="text-xl font-semibold mb-4">Extracted Details</h2>

                        {/* Table Format - Dynamically Rendered */}
                        <table className="w-full border border-gray-300 rounded-md">
                            <tbody>
                                {Object.entries(extractedData.document_details || {}).map(([key, value]) => (
                                    <tr key={key} className="border-b">
                                        <td className="p-3 font-semibold capitalize">{key.replace(/_/g, " ")}</td>
                                        <td className="p-3">{value || "N/A"}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>

                        {/* Verification Buttons */}
                        <div className="flex justify-end gap-4 mt-4">
                            <Button variant="outline" onClick={() => setShowPopup(false)}>Cancel</Button>
                            <Button onClick={handleVerify}>Verify</Button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}