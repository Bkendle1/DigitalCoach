import Link from "next/link";
import Button from "../atoms/Button";
import style from "./Navbar.module.scss";
import LogoutIcon from "@mui/icons-material/Logout";
import useAuthContext from "@App/lib/auth/AuthContext";

export default function NavBar() {
  const { logout } = useAuthContext();

  return (
    <div className={style.main}>
      <div className={style.barcontainer}>
        <Link href="/" className={style.logo_text}>
          Digital Coach
        </Link>
        <div className={style.links}>
          <Link href="/" className={style.linksText}>
            Dashboard
          </Link>
          <Link href="/naturalconversation" className={style.linksText}>
            Natural Conversation
          </Link>
          <Link href="/progress" className={style.linksText}>
            Progress Tracking
          </Link>
          <Link href="/profile" className={style.linksText}>
            Profile
          </Link>
        </div>

        <Button onClick={logout} className={style.logout}>
          <LogoutIcon />
          <div>Log out</div>
        </Button>
      </div>
    </div>
  );
}
