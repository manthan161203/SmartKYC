import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";

const Navbar = () => {
  const navigate = useNavigate();

  // Function to check if the user is logged in
  const isAuthenticated = () => {
    return document.cookie
      .split("; ")
      .some((cookie) => cookie.startsWith("access_token="));
  };

  // Handle Logout
  const handleLogout = () => {
    // Remove the token from cookies
    document.cookie = "access_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC";

    // Redirect to login page after logout
    navigate("/");
  };

  return (
    <nav className="flex justify-between items-center p-3 shadow-md bg-white">
      <h1 className="text-xl font-bold">Smart KYC</h1>
      <div className="space-x-3 flex justify-center items-center">
        {isAuthenticated() ? (
          // Show Logout Button if Logged In
          <Button variant="outline" className="hover:cursor-pointer" onClick={handleLogout}>
            Logout
          </Button>
        ) : (
          // Show Login & Register Buttons if Not Logged In
          <>
            <Button variant="outline" className="hover:cursor-pointer" onClick={() => navigate("/login")}>
              Login
            </Button>
            <Button className="hover:cursor-pointer" onClick={() => navigate("/register")}>
              Register
            </Button>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
