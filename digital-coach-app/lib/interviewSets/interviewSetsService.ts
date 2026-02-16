import {
  addDoc,
  collection,
  CollectionReference,
  doc,
  DocumentReference,
  Firestore,
  getFirestore,
  getDoc,
  getDocs,
  setDoc,
  Timestamp,
} from "firebase/firestore";
import FirebaseService from "../firebase/FirebaseService";

export interface IInterviewSet {
  name: string;
  minutesToAnswer?: number;
  numberOfRetries?: number;
  questionSetRef: string;
  createdAt?: Timestamp;
}

class InterviewSetsService extends FirebaseService {
  private firestore: Firestore;

  constructor() {
    super();
    this.firestore = getFirestore(this.app);
  }

  private getCollectionRef(userId: string) {
    return collection(
      this.firestore,
      "users",
      userId,
      "interviewSets"
    ) as CollectionReference<IInterviewSet>;
  }

  async create(userId: string, interviewSet: IInterviewSet) {
    const collectionRef = this.getCollectionRef(userId);
    const docData: IInterviewSet = {
      ...interviewSet,
      createdAt: Timestamp.now(),
    };
    const docRef = await addDoc(collectionRef, docData);
    return getDoc(docRef);
  }

  async getUserInterviewSets(userId: string) {
    const collectionRef = this.getCollectionRef(userId);
    return getDocs(collectionRef);
  }

  async getInterviewSet(userId: string, interviewSetId: string) {
    const docRef = doc(
      this.firestore,
      "users",
      userId,
      "interviewSets",
      interviewSetId
    ) as DocumentReference<IInterviewSet>;
    return getDoc(docRef);
  }
}

export default new InterviewSetsService();
