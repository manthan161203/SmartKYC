import Navbar from "@/components/ui/Navbar";
import { Button } from "@/components/ui/button";

const Landing = () => {
  return (
    <div>
      {/* Sticky Navbar */}
      <div className="fixed top-0 left-0 w-full bg-white shadow-md z-50">
        <Navbar />
      </div>

      <main className="flex flex-col items-center justify-center h-screen text-center px-4 pt-20">
        <h1 className="text-4xl font-bold mb-4">Smart KYC Verification</h1>
        <p className="text-lg text-gray-600 max-w-2xl">
          Secure and seamless identity verification powered by AI. Get started
          with fast and reliable KYC processing.
        </p>
        <Button className="mt-6">Get Started</Button>
      </main>
      

      {/* Footer */}
      <footer className="p-6 text-center text-gray-600">
        &copy; 2025 Smart KYC. All rights reserved.
      </footer>
    </div>
  );
};

export default Landing;
