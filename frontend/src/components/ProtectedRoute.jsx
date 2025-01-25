import PropTypes from "prop-types";
import { useAuth0 } from "@auth0/auth0-react";
import { Navigate } from "react-router-dom";
import Spinner from "../components/Spinner";

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth0();

  if (isLoading) return <Spinner />;

  if (!isAuthenticated) return <Navigate to="/" />;

  return children;
};

ProtectedRoute.propTypes = {
  children: PropTypes.node.isRequired,
};

export default ProtectedRoute;
