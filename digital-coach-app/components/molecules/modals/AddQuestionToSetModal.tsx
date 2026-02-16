import { useState } from "react";
import Modal from "react-modal";
import { Card, Button } from "@App/components/atoms";
import styles from "./AddQuestionToSetModal.module.scss";

Modal.setAppElement("#__next");

interface Props {
  isOpen: boolean;
  handleClose: () => void;
  handleAdd: (questionId: string, questionSetId: string) => Promise<void>;
  modal: string;
  questionSets: any[];
  question: any;
}

export default function AddQuestionToSetModal(props: Props) {
  const { isOpen, handleClose, handleAdd, questionSets, question } = props;
  const [selectedQuestionSet, setSelectedQuestionSet] = useState(props.questionSets[0].id);

   const handleAddClick = () => {
    if (!selectedQuestionSet) return;
    handleAdd(selectedQuestionSet, question);
    handleClose();
  };

  return (
    <Modal
      isOpen={isOpen}
      onRequestClose={handleClose}
      className={styles.modal}
      overlayClassName={styles.overlay}
    >
      <Card>
        <h2 className={styles.title}>Add Question</h2>
        <select
          className={styles.select}
          value={selectedQuestionSet}
          onChange={(e) => setSelectedQuestionSet(e.target.value)}
        >
          {questionSets.map((qs) => (
            <option key={qs.id} value={qs.id}>
              {qs.title}
            </option>
          ))}
        </select>
        <div className={styles.buttonRow}>
          <Button onClick={handleAddClick}>Add</Button>
          <Button onClick={handleClose} className={styles.cancelButton}>
            Cancel
          </Button>
        </div>
      </Card>
    </Modal>
  );
}

