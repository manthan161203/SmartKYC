import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";

const Navbar = () => {
    const navigate = useNavigate();
  return (
    <nav className="flex justify-between items-center p-3 shadow-md bg-white">
      <h1 className="text-xl font-bold">Smart KYC</h1>
      <div className="space-x-3 flex justify-center items-center">
        <Button variant="outline" className='hover:cursor-pointer' onClick={() => navigate("/login")}>Login</Button>
        <Button className='hover:cursor-pointer' onClick={() => navigate("/register")}>Register</Button>
      </div>
    </nav>
  );
};

export default Navbar;
