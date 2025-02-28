import { ResetPassword } from "@/components/auth/ResetPassword";
import Navbar from "@/components/ui/Navbar"; // Make sure to import the Navbar component

export default function ResetPasswordPage() {
  return (
    <div>
      {/* Sticky Navbar */}
      <div className="fixed top-0 left-0 w-full bg-white shadow-md z-50">
        <Navbar />
      </div>
      <div className="flex min-h-svh flex-col items-center justify-center bg-muted p-6 md:p-10 mt-16"> {/* Add margin-top to avoid overlap */}
        <div className="w-full max-w-sm md:max-w-3xl">
          <ResetPassword />
        </div>
      </div>
    </div>
  );
}
