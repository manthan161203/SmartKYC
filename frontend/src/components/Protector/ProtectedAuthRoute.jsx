import { Navigate, Outlet } from "react-router-dom";
import { getAccessToken } from "@/utils/getAccessToken"; // Ensure this path is correct

// Function to check if the user is authenticated
const isAuthenticated = () => {
  const token = getAccessToken();
  return !!token; // Return true if token exists, otherwise false
};

// Wrapper for protected auth routes
export function ProtectedAuthRoute() {
  return isAuthenticated() ? <Navigate to="/" replace /> : <Outlet />;
}
