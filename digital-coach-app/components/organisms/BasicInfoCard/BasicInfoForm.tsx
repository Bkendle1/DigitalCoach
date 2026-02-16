import { useState } from 'react';
import {
  TextField,
  FormControl,
  Button,
  FormControlLabel,
  Checkbox,
} from '@mui/material';
import { useForm } from 'react-hook-form';
// import InterviewSetsService from '@App/lib/interviewSets/interviewSetsService';
// import QuestionSetsService from '@App/lib/questionSets/QuestionSetsService';

interface BasicInfoFormProps {
  userId: string;
}

export default function BasicInfoForm({ userId }: BasicInfoFormProps) {
  const [questionSetName, setQuestionSetName] = useState("");
  const [timePerQ, setTimePerQ] = useState("");
  const [numRetries, setNumRetries] = useState("");
  const [makeInterview, setMakeInterview] = useState(true);

  const createInterviewSet = async (e: React.FormEvent) => {
    e.preventDefault();

    const questionSet = await QuestionSetsService.createQuestionSet({
      title: questionSetName,
      description: "",
      questions: [],
      isFeatured: false,
      createdBy: userId,
    };
    // const thisQuestionSet = await QuestionSetsService.createQuestionSet(
    //   questionSet
    // );
    console.log("hi");
    // A reference to the questionSet is stored in the newly created interviewSet
    if (makeInterview) {
      await InterviewSetsService.create(userId, {
        name: questionSetName,
        minutesToAnswer: parseInt(timePerQ),
        numberOfRetries: parseInt(numRetries),
        // questionSetRef: thisQuestionSet.id,
      };
      console.log('Calling create function in BasicInfoForm');
      // await InterviewSetsService.create(userId, interviewSet);
    }

    location.reload(); // refresh page after creation
  };

  return (
    <form onSubmit={createInterviewSet} className={styles.form}>
      <TextField
        title="Question Set Name"
        placeholder="Give the question set a fitting name"
        value={questionSetName}
        onChange={(e) => setQuestionSetName(e.target.value)}
        required
      />
      <TextField
        title="Minutes Per Question"
        type="number"
        placeholder="Time per question"
        value={timePerQ}
        onChange={(e) => setTimePerQ(e.target.value)}
      />
      <TextField
        title="Retries Per Question"
        type="number"
        placeholder="Number of retries"
        value={numRetries}
        onChange={(e) => setNumRetries(e.target.value)}
      />
      <div className={styles.buttonRow}>
        <Button type="submit">Create Question Set</Button>
      </div>
    </form>
  );
}
