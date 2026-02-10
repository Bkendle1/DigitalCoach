import { WithRouterProps } from "next/dist/client/with-router";
import { withRouter } from "next/router";
import { PropsWithChildren, useEffect } from "react";
import AuthService from "./AuthService";
import useAuthContext from "./AuthContext";

function UnAuthGuard({ children, router }: PropsWithChildren<WithRouterProps>) {
  const { currentUser } = useAuthContext();

  useEffect(() => {
    AuthService.onAuthStateChanged((user) => {
      if (!!user) {
        // If user is authenticated but hasn't completed registration, go to register page
        if (currentUser && !currentUser?.data()?.registrationCompletedAt) {
          router.push("/auth/register");
        } else if (currentUser && currentUser?.data()?.registrationCompletedAt) {
          // If user is authenticated and has completed registration, go to home
          router.push("/");
        }
      }
    });
  }, [router, currentUser]);

  return <>{children}</>;
}

export default withRouter(UnAuthGuard);
