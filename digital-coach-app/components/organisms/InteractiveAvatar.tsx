import { useRef, useEffect } from "react";
import { LiveAvatarSession, AgentEventsEnum } from "@heygen/liveavatar-web-sdk";
import styles from "@App/styles/interview/NaturalConversationPage.module.scss";
import { VideoOff } from "lucide-react";

interface InteractiveAvatarProps {
  sessionToken: string;
  onTranscriptUpdate?: (transcript: string, isFinal: boolean) => void;
}

function InteractiveAvatar({sessionToken, onTranscriptUpdate}: InteractiveAvatarProps) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const sessionRef = useRef<LiveAvatarSession>(null);
  const userConfig = {
    voiceChat: true,
  };
  
  /**
   * Starts HeyGen LiveAvatar session using the given session token and configurations. Recommend referring to the reviewing heygen/liveavatar-web-sdk library as API documentation is sparse as of writing this.
   */
  const startSession = async () => {
    console.log("Starting mock interview...");
    // create new session
    const session = new LiveAvatarSession(sessionToken, userConfig);
    sessionRef.current = session;
    

    // register event listener for when the avatar talks so we can add it to the transcript
    // the event returns the text that the avatar speaks so we don't have to use AssemblyAI for this
    session.on(AgentEventsEnum.AVATAR_TRANSCRIPTION, ({text}) => {
      if (onTranscriptUpdate) {
        onTranscriptUpdate(`Interviewer: ${text}`, true);
      }
      // console.log(`Avatar said: ${text}\n`);
    });

    // HeyGen LiveAvatar keeps a user transcription (we currently use AssemblyAI for transcription) 
    // session.on(AgentEventsEnum.USER_TRANSCRIPTION, ({text}) => {
    //   if (onTranscriptUpdate) {
    //     onTranscriptUpdate(`User: ${text}`, true);
    //   }
    // })

    // start the session
    try {
      await session.start();
    } catch (e) {
      console.error(`Error starting HeyGen LiveAvatar session: ${e}`);
    }

    // when video element is mounted, attach it to the session
    if (videoRef.current) {
      session.attach(videoRef.current);
    }
    
  }

  /**
   * Stops HeyGen LiveAvatar Session.
   */
  const stopSession = async () => {
    console.log("Stopping session...");
    // stop session
    if (sessionRef.current) {
      await sessionRef.current.stop();
    }
  }

  useEffect(() => {
    // start session once session token is received
    if (sessionToken) {
      startSession();
    }

    // stop heygen session when component unmounts
    return () => {
      stopSession();
    }
  }, [sessionToken]);

  return (
    <div className={styles.videoCard}>
      <div className={`${styles.videoHeader} ${styles.aiHeader}`}>
        <p>Interviewer</p>
      </div>
      <div className={`${styles.videoContent} ${styles.aiContainer}`}>
        <video 
          ref={videoRef}
          autoPlay
          playsInline
          style={{display: sessionToken ? "block" : "none"}}
          />
        {!sessionToken && (
          <div className={styles.cameraOff}>
              <VideoOff/>
              <p>Waiting</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default InteractiveAvatar;