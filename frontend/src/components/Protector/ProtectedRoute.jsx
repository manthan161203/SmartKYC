import { Navigate, Outlet } from "react-router-dom";
import { getAccessToken } from "@/utils/getAccessToken";

const ProtectedRoute = () => {
  const token = getAccessToken(); // Fetch the access token

  return token ? <Outlet /> : <Navigate to="/login" replace />;
};

export default ProtectedRoute;