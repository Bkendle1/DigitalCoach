import { WithRouterProps } from "next/dist/client/with-router";
import { withRouter } from "next/router";
import { PropsWithChildren, useEffect } from "react";
import AuthService from "./AuthService";
import useAuthContext from "./AuthContext";
import UserService from "../user/UserService";

function UnAuthGuard({ children, router }: PropsWithChildren<WithRouterProps>) {
  const { currentUser } = useAuthContext();

  useEffect(() => {
    AuthService.onAuthStateChanged(async (user) => {
      if (!!user) {
        // Fetch the user document to check registration status
        const userDoc = await UserService.getUser(user.uid);
        
        // If user is authenticated but hasn't completed registration, go to register page
        if (userDoc.exists() && !userDoc.data()?.registrationCompletedAt) {
          router.push("/auth/register");
        } else if (userDoc.exists() && userDoc.data()?.registrationCompletedAt) {
          // If user is authenticated and has completed registration, go to home
          router.push("/");
        }
      }
    });
  }, [router]);

  return <>{children}</>;
}

export default withRouter(UnAuthGuard);
