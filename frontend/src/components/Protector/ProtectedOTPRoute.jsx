import { Navigate, Outlet } from "react-router-dom";
import { getAccessToken } from "@/utils/getAccessToken";

export default function ProtectedOTPRoute() {
  return getAccessToken() ? <Outlet /> : <Navigate to="/login" replace />;
}
