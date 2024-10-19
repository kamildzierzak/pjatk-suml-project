import { useAuth0 } from "@auth0/auth0-react";

const LogoutButton = () => {
  const { logout } = useAuth0();

  return (
    <button
      className="rounded bg-red-500 px-4 py-2 font-bold text-white hover:bg-red-700 sm:w-[150px]"
      onClick={() =>
        logout({ logoutParams: { returnTo: window.location.origin } })
      }
    >
      Wyloguj
    </button>
  );
};

export default LogoutButton;
