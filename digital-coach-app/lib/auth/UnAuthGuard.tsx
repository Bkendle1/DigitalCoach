import { WithRouterProps } from "next/dist/client/with-router";
import { withRouter } from "next/router";
import { PropsWithChildren, useEffect } from "react";
import AuthService from "./AuthService";
import UserService from "../user/UserService";

function UnAuthGuard({ children, router }: PropsWithChildren<WithRouterProps>) {
  useEffect(() => {
    let isMounted = true;
    
    const unsubscribe = AuthService.onAuthStateChanged(async (user) => {
      if (!!user && isMounted) {
        // Fetch the user document to check registration status
        const userDoc = await UserService.getUser(user.uid);
        
        if (!isMounted) return; // Check again after async operation
        
        if (userDoc.exists()) {
          // If user is authenticated but hasn't completed registration, go to register page
          if (!userDoc.data()?.registrationCompletedAt) {
            router.push("/auth/register");
          } else {
            // If user is authenticated and has completed registration, go to home
            router.push("/");
          }
        }
      }
    });
    
    return () => {
      isMounted = false;
      unsubscribe?.();
    };
  }, [router]);

  return <>{children}</>;
}

export default withRouter(UnAuthGuard);
