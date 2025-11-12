import Link from "next/link";
import Avatar from "@App/components/atoms/Avatar";
import Card from "@App/components/atoms/Card";
import Grid from "@mui/material/Grid";
import useAuthContext from "@App/lib/auth/AuthContext";
import AuthGuard from "@App/lib/auth/AuthGuard";
import styles from "@App/styles/ProgressPage.module.scss";

function ProgressPage() {
  const { currentUser } = useAuthContext();
  return (
    <div className={styles.ProgressPage}>
      <h1>Your Progress</h1>
      <div className={styles.ProgressPage_avatarWrapper}>
        {currentUser?.data()?.avatarUrl && (
          <Avatar size={125} src={currentUser?.data()!.avatarUrl} />
        )}
      </div>
      <Grid
        className={styles.ProgressPage_body}
        container
        alignItems="center"
        justifyContent="center"
        columns={3}
      >
        <Card
          className={styles.ProgressPage_bodyCard}
          title="Get Started with Natural Conversation"
        >
          <p>Start practicing your conversation skills with the avatar.</p>
          <Link href="/naturalconversation" className={styles.linksText}>
            Start Natural Conversation
          </Link>
        </Card>
        <Card className={styles.ProgressPage_bodyCard} title="Progress Tracking">
          <p>Track your progress here.</p>
        </Card>
        <Card className={styles.ProgressPage_bodyCard} title="Tips">
          <p>Keep practicing to improve your communication skills!</p>
        </Card>
      </Grid>
    </div>
  );
}

export default function Progress() {
  return (
    <AuthGuard>
      <ProgressPage />
    </AuthGuard>
  );
}
