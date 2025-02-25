import { RegisterForm } from "@/components/ui/RegisterForm";

const RegisterPage = () => {
  return (
    <div className="flex flex-col items-center justify-center bg-muted p-6 md:p-10">
          <div className="w-full max-w-5 md:max-w-3xl">
            <RegisterForm />
          </div>
        </div>
  );
};

export default RegisterPage;
