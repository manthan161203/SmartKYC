import axios from "axios";
import { getAccessToken } from "@/utils/getAccessToken"; // ✅ Reads token from cookies
import { jwtDecode } from "jwt-decode";
import { toast } from "react-toastify";

const API_BASE_URL = "http://localhost:8000"; // Update if needed

// Function to check if the token is expired
const isTokenExpired = (token) => {
  try {
    const decoded = jwtDecode(token);
    return decoded.exp * 1000 < Date.now(); // Convert to milliseconds
  } catch (error) {
    return true; // If decoding fails, assume expired
  }
};

// Function to remove access_token from cookies
const clearAccessToken = () => {
  document.cookie = "access_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC; Secure";
};

// Create an Axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true, // ✅ Ensures cookies are sent with requests
});

// Request interceptor to attach token and check expiration
api.interceptors.request.use(
  (config) => {
    const token = getAccessToken();
    if (!token) {
      toast.error("Unauthorized! Please login.");
      throw new axios.Cancel("No access token found.");
    }

    if (isTokenExpired(token)) {
      toast.error("Session expired. Please login again.");
      clearAccessToken(); // ✅ Clears expired token from cookies
      window.location.href = "/login"; // Redirect to login page
      throw new axios.Cancel("Token expired.");
    }

    config.headers.Authorization = `Bearer ${token}`;
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for handling errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      const { status, config } = error.response;

      // ✅ Ignore 401 errors from the change-password endpoint
      if (status === 401 && config.url === "/auth/change-password") {
        return Promise.reject(error); // Don't log out, just return the error
      }

      // ✅ Handle other 401 errors (expired token, invalid session)
      if (status === 401) {
        toast.error("Unauthorized! Please login again.");
        clearAccessToken();
        window.location.href = "/login";
      }
    }

    return Promise.reject(error);
  }
);

export default api;