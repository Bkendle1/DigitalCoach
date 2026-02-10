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
        try {
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
          } else {
            // If user document doesn't exist, redirect to register page to create profile
            router.push("/auth/register");
          }
        } catch (error) {
          // If there's an error fetching user data, log it but don't crash the component
          console.error("Error fetching user document:", error);
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
