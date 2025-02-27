import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Disclosure, DisclosureButton, DisclosurePanel, Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/react";
import { Bars3Icon, BellIcon } from "@heroicons/react/24/outline";
import { Button } from "@/components/ui/button";
import Profile from "@/components/ui/Profile";

const navigation = [
  { name: "Dashboard", href: "/", current: true },
  { name: "Team", href: "/team", current: false },
  { name: "Projects", href: "/projects", current: false },
  { name: "Calendar", href: "/calendar", current: false },
];

function classNames(...classes) {
  return classes.filter(Boolean).join(" ");
}

const Navbar = () => {
  const navigate = useNavigate();
  const [isProfileOpen, setIsProfileOpen] = useState(false);

  const isAuthenticated = () => {
    return document.cookie.split("; ").some((cookie) => cookie.startsWith("access_token="));
  };

  const handleLogout = () => {
    document.cookie = "access_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC";
    navigate("/login");
  };

  return (
    <Disclosure as="nav" className="bg-[#1E1E1E] text-gray-700 shadow-lg">
      <div className="mx-auto w-full px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          {/* Mobile Menu Button */}
          <div className="absolute inset-y-0 left-0 flex items-center sm:hidden">
            <DisclosureButton className="p-2 rounded-md text-gray-400 hover:text-white hover:bg-gray-600 focus:ring-2 focus:ring-white">
              <span className="sr-only">Open main menu</span>
              <Bars3Icon className="block w-6 h-6" />
            </DisclosureButton>
          </div>

          {/* Logo & Navigation */}
          <div className="flex flex-1 items-center justify-center sm:justify-start">
            <h1 className="text-xl font-bold text-white">Smart KYC</h1>
            <div className="hidden sm:ml-6 sm:block">
              <div className="flex space-x-4">
                {navigation.map((item) => (
                  <a
                    key={item.name}
                    href={item.href}
                    className={classNames(
                      item.current ? "bg-gray-700 text-white" : "text-gray-300 hover:bg-gray-600 hover:text-white",
                      "rounded-md px-3 py-2 text-sm font-medium transition duration-300"
                    )}
                  >
                    {item.name}
                  </a>
                ))}
              </div>
            </div>
          </div>

          {/* Notifications & Profile */}
          <div className="absolute inset-y-0 right-0 flex items-center space-x-2 pr-2 sm:static sm:inset-auto">
            {/* Notification Icon */}
            <button className="relative p-2 rounded-full bg-gray-700 text-white hover:bg-gray-600 focus:ring-2 focus:ring-gray-500 border border-gray-600 flex items-center justify-center w-9 h-9">
              <span className="sr-only">View notifications</span>
              <BellIcon className="w-5 h-5" />
              <span className="absolute -top-1.5 -right-1.5 flex h-3 w-3">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-500 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span>
              </span>
            </button>

            {/* Profile Dropdown */}
            {isAuthenticated() ? (
              <Menu as="div" className="relative">
                <MenuButton className="relative flex rounded-full bg-gray-700 p-1 text-sm border border-gray-600">
                  <span className="sr-only">Open user menu</span>
                  <img
                    alt="User Avatar"
                    src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
                    className="w-8 h-8 rounded-full"
                  />
                </MenuButton>
                <MenuItems className="absolute right-0 mt-2 min-w-[10rem] bg-gray-700 text-white shadow-lg rounded-md py-1 z-50 border border-gray-600">
                  <MenuItem>
                    <button
                      onClick={() => setIsProfileOpen(true)}
                      className="block w-full px-4 py-2 text-sm text-right hover:bg-gray-600"
                    >
                      Profile
                    </button>
                  </MenuItem>
                  <MenuItem>
                    <button
                      onClick={() => navigate("/settings")}
                      className="block w-full px-4 py-2 text-sm text-right hover:bg-gray-600"
                    >
                      Settings
                    </button>
                  </MenuItem>
                  <MenuItem>
                    <button
                      onClick={handleLogout}
                      className="block w-full px-4 py-2 text-sm text-right text-red-500 hover:bg-gray-600"
                    >
                      Sign Out
                    </button>
                  </MenuItem>
                </MenuItems>
              </Menu>
            ) : (
              <div className="flex gap-2">
                <Button className="bg-gray-700 text-white border border-gray-600 hover:bg-gray-600" onClick={() => navigate("/login")}>
                  Login
                </Button>
                <Button className="bg-gray-700 text-white border border-gray-600 hover:bg-gray-600" onClick={() => navigate("/register")}>
                  Register
                </Button>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Profile Sheet */}
      <Profile isOpen={isProfileOpen} setIsOpen={setIsProfileOpen} />

      {/* Mobile Menu Panel */}
      <DisclosurePanel className="sm:hidden bg-[#252525]">
        <div className="px-2 pt-2 pb-3 space-y-1">
          {navigation.map((item) => (
            <DisclosureButton
              key={item.name}
              as="a"
              href={item.href}
              className={classNames(
                item.current ? "bg-gray-700 text-white" : "text-gray-300 hover:bg-gray-600 hover:text-white",
                "block px-3 py-2 rounded-md text-base font-medium transition duration-300"
              )}
            >
              {item.name}
            </DisclosureButton>
          ))}
        </div>
      </DisclosurePanel>
    </Disclosure>
  );
};

export default Navbar;