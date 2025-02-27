import Profile from "@/components/ui/Profile";

const ProfilePage = () => {
  return (
    <div className="container mx-auto py-10">
      <Profile isOpen={true} setIsOpen={() => {}} />
    </div>
  );
};

export default ProfilePage;