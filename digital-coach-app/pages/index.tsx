import type { NextPage } from "next";
import { useState, useEffect } from "react";
import useAuthContext from "@App/lib/auth/AuthContext";
import AuthGuard from "@App/lib/auth/AuthGuard";
import styles from "@App/styles/Home.module.scss";
import Card from "@App/components/atoms/Card";
import ScoreChart from "@App/components/molecules/ScoreChart";
import PracticeCalendar from "@App/components/molecules/PracticeCalendar";
import Link from "next/link";
import useGetAnswersByUserId from "@App/lib/answer/useGetAnswerByUserId";

const Home: NextPage = () => {
  const { currentUser } = useAuthContext();

  const {
    data: answerData,
    isLoading: isAnswerLoading,
    isFetching: isAnswerFetching,
  } = useGetAnswersByUserId(currentUser?.id);

  const [tip, setTips] = useState("");

  useEffect(() => {
    const tips = [
      "Practice active listening during the interview. Pay attention to the questions asked and respond thoughtfully.",
      "Research common behavioral interview questions and prepare STAR (Situation, Task, Action, Result) stories to showcase your skills and experiences.",
      "Arrive early for the interview to allow time for unexpected delays and to demonstrate your punctuality.",
      "Turn off your phone or set it to silent mode before the interview to avoid distractions.",
      "Maintain good body language throughout the interview. Sit up straight, make eye contact, and smile to convey confidence.",
      "Research the salary range for similar positions in your industry and be prepared to discuss salary expectations if asked.",
      "Practice good hygiene and grooming before the interview. A neat appearance contributes to a positive first impression.",
      "Review the job description and customize your answers to align with the requirements of the role.",
      "Stay positive and enthusiastic during the interview. A positive attitude can leave a lasting impression on the interviewer.",
      "Start by researching the company and your interviewer. Understanding key information about the company you’re interviewing with can help you go into your interview with confidence.",
      "Practice answering common interview questions to build your confidence and improve your responses during the actual interview.",
      "Dress appropriately for your interview. Your attire should be professional and suitable for the company culture.",
      "Prepare questions to ask the interviewer. This shows your interest in the position and company and can help you gather important information.",
      "Stay calm and composed during the interview. Take a deep breath if you feel nervous and focus on articulating your thoughts clearly.",
      "Highlight your achievements and relevant experiences during the interview. Use specific examples to demonstrate your skills and capabilities.",
      "Follow up with a thank-you email after the interview. Express your gratitude for the opportunity and reiterate your interest in the position.",
    ];
    const randInd = Math.floor(Math.random() * tips.length);
    setTips(tips[randInd]);
  }, []);

  const events =
  answerData?.docs.map((answer) => {
    return {
      start: answer.data().createdAt.toDate().toISOString(),
      end: answer.data().createdAt.toDate().toISOString(),
    };
  }) || [];

  return (
    <AuthGuard>
      <div className={styles.Home}>
        <h1>Welcome back, {currentUser?.data()?.name}!</h1>
        <h2>Dashboard</h2>
        <div className={styles.cards}>
          <Card title={"Get Started with Natural Conversation"} multiline>
            <p>Start a natural conversation with the avatar to practice your skills.</p>
            <Link href="/naturalconversation">
              <button style={{ marginTop: "10px", padding: "10px 20px", cursor: "pointer" }}>
                Start Natural Conversation
              </button>
            </Link>
          </Card>
          <Card title={"Your Random Tip!"} multiline>
            <div className={styles.tipoftheday}>
              <p>{tip}</p>
            </div>
          </Card>
          <Card multiline>
            <div className={styles.calendarWrapper}>
              <PracticeCalendar events={events} />
            </div>
          </Card>
          <Card title={"Quick Links"} multiline>
            <ul style={{ listStyle: "none", padding: 0 }}>
              <li style={{ marginBottom: "10px" }}>
                <Link href="/naturalconversation">Natural Conversation</Link>
              </li>
              <li style={{ marginBottom: "10px" }}>
                <Link href="/progress">Progress Tracking</Link>
              </li>
              <li style={{ marginBottom: "10px" }}>
                <Link href="/profile">Profile</Link>
              </li>
            </ul>
          </Card>
        </div>
      </div>
    </AuthGuard>
  );
};

export default Home;
