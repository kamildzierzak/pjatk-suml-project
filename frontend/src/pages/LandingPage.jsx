import { useAuth0 } from "@auth0/auth0-react";
import LoginButton from "../components/LoginButton"
import landingImg from "../assets/landing.jpg"

const LandingPage = () => {
  const {isAuthenticated} = useAuth0();

  return (
      <div className="flex flex-col items-center justify-center text-center h-screen">
        <div className="flex flex-col items-center justify-center sm:border-2 sm:p-8 sm:rounded-2xl">
          <img src={landingImg} alt="Dog and cat looking at the stars." className="w-[350px] rounded-full p-4" />
          <h1 className="text-4xl p-2 max-w-[350px] font-semibold text-pretty">Constellation Recognizer 6001X Deluxe</h1>

          <h2 className="text-neutral-500 p-4 max-w-[350px]">Aplikacja do rozpoznawania konstelacji na zdjęciach.</h2>

          {!isAuthenticated && <LoginButton />}
        </div>
      </div>
  )
}

export default LandingPage;