import { Navigate, Outlet } from "react-router-dom";

// Function to check if the user is authenticated
const isAuthenticated = () => {
  const token = document.cookie
    .split("; ")
    .find((row) => row.startsWith("access_token="));

  return !!token; // Return true if token exists, else false
};

// Wrapper for protected auth routes
export function ProtectedAuthRoute() {
  return isAuthenticated() ? <Navigate to="/" replace /> : <Outlet />;
}
