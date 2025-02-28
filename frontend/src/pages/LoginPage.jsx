import { LoginForm } from "@/components/auth/LoginForm";
import Navbar from "@/components/ui/Navbar";

export default function LoginPage() {
  return (
    <>
      {/* Sticky Navbar */}
      <div className="fixed top-0 left-0 w-full bg-white shadow-md z-50">
        <Navbar />
      </div>
      <div className="flex min-h-svh flex-col items-center justify-center bg-muted p-6 md:p-10">
        <div className="w-full max-w-sm md:max-w-3xl">
          <LoginForm />
        </div>
      </div>
    </>
  );
}