import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { ArrowLeft, Eye, EyeOff, Loader2 } from "lucide-react"; // Import Loader2 icon
import PasswordStrengthBar from "react-password-strength-bar";

const nameRegex = /^[A-Za-z]+$/;

const registerSchema = z.object({
  first_name: z.string()
    .min(2, "Min 2 characters.")
    .max(50, "Max 50 characters.")
    .regex(nameRegex, "Only letters allowed."),
  middle_name: z.string().optional(),
  last_name: z.string()
    .min(2, "Min 2 characters.")
    .max(50, "Max 50 characters.")
    .regex(nameRegex, "Only letters allowed."),

  email: z.string().email("Invalid email address."),

  phone_number: z.string()
    .regex(/^\d+$/, "Only numbers allowed.")
    .min(10, "Must be at least 10 digits."),

  dob: z.string()
    .nonempty("Date of birth is required.")
    .refine((date) => {
      const today = new Date();
      const dob = new Date(date);
      return dob <= today;
    }, "Date of birth must be in the past."),

  gender_id: z.enum(["1", "2", "3"], { errorMap: () => ({ message: "Select a valid gender" }) }),

  password: z.string().min(8, "At least 8 characters."),
});

export function RegisterForm() {
  const navigate = useNavigate();
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [phoneNumber, setPhoneNumber] = useState("");
  const [loading, setLoading] = useState(false); // Loading state

  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(registerSchema),
  });

  const handlePhoneNumberChange = (e) => {
    let value = e.target.value.replace(/\D/g, "");
    setPhoneNumber(value);
    setValue("phone_number", value);
  };

  const onSubmit = async (data) => {
    setLoading(true); // Start loading
    const full_name = `${data.first_name} ${data.middle_name} ${data.last_name}`;

    try {
      const fullPhoneNumber = `+91${phoneNumber}`;
      await axios.post("http://localhost:8000/auth/register", { ...data, full_name, phone_number: fullPhoneNumber });

      toast.success("Registration Successful!", { position: "top-right" });

      setTimeout(() => {
        navigate("/login");
      }, 2500);
    } catch (error) {
      toast.error(error.response?.data?.detail || "Registration failed.", {
        position: "top-right",
      });
    } finally {
      setTimeout(() => setLoading(false), 2500); // Stop loading after 2.5s
    }
  };

  return (
    <div className="flex flex-col gap-6">
      <ToastContainer />

      <Button
        variant="outline"
        onClick={() => navigate("/")}
        className="w-10 h-10 rounded-full flex items-center justify-center"
        disabled={loading} // Disable while loading
      >
        <ArrowLeft className="w-5 h-5" />
      </Button>

      <Card className="w-full max-w-4xl shadow-lg">
        <CardContent className="grid grid-cols-1 md:grid-cols-2 p-0">
          <div className="p-8 flex flex-col justify-center">
            <h1 className="text-2xl font-bold text-center mb-2">Create an Account</h1>
            <p className="text-gray-500 text-center mb-6">Sign up to start using Smart KYC</p>

            <form className="space-y-4" onSubmit={handleSubmit(onSubmit)}>
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="first_name">First Name <span className="text-red-500">*</span></Label>
                  <Input id="first_name" type="text" placeholder="First name" {...register("first_name")} disabled={loading} />
                  {errors.first_name && <p className="text-red-500 mt-0.5 text-xs">{errors.first_name.message}</p>}
                </div>

                <div>
                  <Label htmlFor="middle_name">Middle Name </Label>
                  <Input id="middle_name" type="text" placeholder="Middle name" {...register("middle_name")} disabled={loading} />
                  {errors.middle_name && <p className="text-red-500 mt-0.5 text-xs">{errors.middle_name.message}</p>}
                </div>

                <div>
                  <Label htmlFor="last_name">Last Name <span className="text-red-500">*</span></Label>
                  <Input id="last_name" type="text" placeholder="Last name" {...register("last_name")} disabled={loading} />
                  {errors.last_name && <p className="text-red-500 mt-0.5 text-xs">{errors.last_name.message}</p>}
                </div>
              </div>

              <div>
                <Label htmlFor="email">Email <span className="text-red-500">*</span></Label>
                <Input id="email" type="email" placeholder="Enter your email" {...register("email")} disabled={loading} />
                {errors.email && <p className="text-red-500 mt-0.5 text-xs">{errors.email.message}</p>}
              </div>
              <div className="flex flex-col gap-2">
                <Label htmlFor="phone_number">Phone number <span className="text-red-500">*</span></Label>
                <div className="flex gap-x-0.5">
                  <Input
                    id="country_code"
                    type="text"
                    value="+91"
                    disabled
                    className="text-center w-1/6"
                  />
                  <div className="w-5/6">
                    <Input
                      id="phone_number"
                      type="text"
                      placeholder="Enter your phone number"
                      value={phoneNumber}
                      onChange={handlePhoneNumberChange}
                    />
                    {errors.phone_number && (
                      <p className="text-red-500 mt-0.5 text-xs">{errors.phone_number.message}</p>
                    )}
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="dob">Date of Birth <span className="text-red-500">*</span></Label>
                  <Input id="dob" type="date" {...register("dob")} />
                  {errors.dob && <p className="text-red-500 mt-0.5 text-xs">{errors.dob.message}</p>}
                </div>

                <div>
                  <Label htmlFor="gender_id">Gender <span className="text-red-500">*</span></Label>
                  <select id="gender_id" {...register("gender_id")} className="border p-2 rounded-md w-full">
                    <option value="">Select Gender</option>
                    <option value="1">Male</option>
                    <option value="2">Female</option>
                    <option value="3">Other</option>
                  </select>
                  {errors.gender_id && <p className="text-red-500 mt-0.5 text-xs">{errors.gender_id.message}</p>}
                </div>
              </div>
              
              <div>
                <Label htmlFor="password">Password <span className="text-red-500">*</span></Label>
                <div className="relative">
                  <Input
                    id="password"
                    type={showPassword ? "text" : "password"}
                    placeholder="Enter your password"
                    {...register("password")}
                    onChange={(e) => setPassword(e.target.value)}
                    disabled={loading}
                  />
                  <button
                    type="button"
                    className="absolute right-3 top-3"
                    onClick={() => setShowPassword(!showPassword)}
                    disabled={loading}
                  >
                    {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
                {errors.password && <p className="text-red-500 mt-0.5 text-xs">{errors.password.message}</p>}

                <div className="mt-4">
                  <PasswordStrengthBar password={password} barWidth="100%" />
                </div>
              </div>

              <Button type="submit" className="w-full" disabled={loading}>
                {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Register"}
              </Button>

              <p className="text-center text-xs text-gray-600">
                Already have an account?{" "}
                <span
                  onClick={() => navigate("/login")}
                  className="font-semibold text-black hover:underline cursor-pointer"
                >
                  Login
                </span>
              </p>
            </form>
          </div>
          <div className="hidden md:flex items-center justify-center bg-white-100 p-4">
            <img
              src="login-illustration.png"
              alt="Register Illustration"
              className="w-3/4 h-auto max-w-xs object-contain"
            />
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
