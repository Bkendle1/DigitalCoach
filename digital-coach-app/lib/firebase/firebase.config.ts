// firebase.config.ts
import { initializeApp, getApps } from "firebase/app";
import { getAuth, connectAuthEmulator } from "firebase/auth";
import { getFirestore, connectFirestoreEmulator } from "firebase/firestore";
import { getStorage, connectStorageEmulator } from "firebase/storage";
import { getAnalytics, isSupported as analyticsSupported } from "firebase/analytics";

// Your "fake" config is fine for local emulators
export const firebaseConfig = {
  apiKey: "fake-api-key",
  authDomain: "localhost",
  projectId: "digitalcoach-local",
  storageBucket: "digitalcoach-local.appspot.com",
  messagingSenderId: "fake-sender-id",
  appId: "fake-app-id",
  measurementId: "G-FAKEMEASURE",
};

const app = !getApps().length ? initializeApp(firebaseConfig) : getApps()[0];

// Auth
const auth = getAuth(app);
connectAuthEmulator(auth, "http://127.0.0.1:9099", { disableWarnings: true });

// Firestore
const db = getFirestore(app);
connectFirestoreEmulator(db, "localhost", 8080);

// Storage
const storage = getStorage(app);
connectStorageEmulator(storage, "localhost", 9199);

// Analytics (optional)
(async () => {
  if (typeof window !== "undefined" && await analyticsSupported()) {
    getAnalytics(app);
  }
})();

export { app, auth, db, storage };


// import { getStorage, connectStorageEmulator } from "firebase/storage";
// import { getFirestore, connectFirestoreEmulator } from "firebase/firestore";
// import { getAuth, connectAuthEmulator } from "firebase/auth";
// import { getAnalytics } from "firebase/analytics";
// import { initializeApp, getApps } from "firebase/app";

// export const firebaseConfig = {
//   apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
//   authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
//   projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
//   storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET,
//   messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
//   appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID,
//   measurementId: process.env.NEXT_PUBLIC_FIREBASE_MEASUREMENT_ID,
// };
// const localIp = "localhost";

// if (!getApps().length) {
//   const app = initializeApp(firebaseConfig);

//   if (typeof window !== "undefined" && "measurementId" in firebaseConfig) {
//     getAnalytics(app);
//   }

//   const auth = getAuth(app);
//   // connectAuthEmulator(auth, `http://127.0.0.1:9099`, {
//   //   disableWarnings: true,
//   // });

//   const db = getFirestore(app);
//   // connectFirestoreEmulator(db, localIp, 8080);

//   const storage = getStorage(app);
//   // connectStorageEmulator(storage, localIp, 9199);
// }
