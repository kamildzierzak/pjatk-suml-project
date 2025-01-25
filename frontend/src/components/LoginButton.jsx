import { useAuth0 } from "@auth0/auth0-react";

const LoginButton = () => {
  const { loginWithRedirect } = useAuth0();

  return (
    <button
      className="w-[150px] rounded bg-blue-500 px-8 py-4 font-semibold text-white hover:cursor-pointer hover:bg-purple-700"
      onClick={() => loginWithRedirect()}
    >
      Zaloguj
    </button>
  );
};

export default LoginButton;
