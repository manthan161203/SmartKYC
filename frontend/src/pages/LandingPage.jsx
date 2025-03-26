import Navbar from "@/components/ui/Navbar";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { Loader2 } from "lucide-react";

const Landing = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const handleGetStarted = () => {
    setLoading(true); // ✅ Start loading
    setTimeout(() => {
      navigate("/upload-documents"); // ✅ Navigate after 2s
    }, 2000);
  };

  return (
    <div>
      {/* Sticky Navbar */}
      <div className="fixed top-0 left-0 w-full bg-white shadow-md z-50">
        <Navbar />
      </div>

      <main className="flex flex-col items-center justify-center min-h-screen text-center px-4 pt-20">
        <h1 className="text-5xl font-bold mb-6">Welcome to Smart KYC Verification</h1>
        <p className="text-xl text-gray-600 max-w-2xl">
          Please follow the steps below to complete your KYC process:
        </p>

        {/* Instructions Box */}
        <div className="bg-gray-100 p-8 rounded-lg shadow-md mt-8 text-left max-w-2xl">
          <h2 className="text-2xl font-semibold mb-4">Steps to Complete KYC:</h2>
          <ul className="list-disc list-inside text-gray-700 space-y-3">
            <li><strong>Aadhaar Verification:</strong> Upload your Aadhaar front and back images. Once uploaded, extract and verify the details.</li>
            <li><strong>PAN Verification:</strong> Upload your PAN card image and extract the details. Verify the information provided.</li>
            <li><strong>Face Verification:</strong> Upload your selfie, and we will match it with your Aadhaar or PAN details.</li>
          </ul>
          <p className="mt-4 text-gray-600 text-base">
            <strong>Note:</strong> Only valid image files (JPG, JPEG, PNG) up to 5MB are allowed. Follow the instructions and messages displayed on each step.
          </p>
          <p className="mt-4 text-red-600 text-base">
            <strong>Warning:</strong> Please do not click the back button or refresh the page during the KYC process.
          </p>
        </div>

        {/* Get Started Button with Loader */}
        <Button className="mt-8" onClick={handleGetStarted} disabled={loading}>
          {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Get Started"}
        </Button>
      </main>

      <footer className="p-6 text-center text-gray-600">
        &copy; 2025 Smart KYC. All rights reserved.
      </footer>
    </div>
  );
};

export default Landing;