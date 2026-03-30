from transformers.pipelines import pipeline
from typing import Any
from schemas import StarClassification, StarFeedbackEvaluation, StarPercentages


def predict_star_scores(text: str) -> StarFeedbackEvaluation:
    """
    Predicts STAR scores and provides feedback.
    Parameters:
    data (dict: {"text": (The sentence to be predicted: str)}): The data to be predicted on
    Returns:
    str: The predicted STAR label
    """
    # Should only need to be set once
    classifier = pipeline("text-classification", model="dnttestmee/starclass_bert")  # type: ignore
    def predict(sentence) -> str:
        """
        Predicts a sentence's STAR label.
        Parameters:
        sentence (str): The sentence to predict the STAR label of
        Returns:
        str: The predicted STAR label
        """
        labels = {
            "LABEL_0": "Action",
            "LABEL_1": "Result",
            "LABEL_2": "Situation",
            "LABEL_3": "Task",
        }
        model_output: Any = classifier(sentence)
        # Single label output
        result: str = labels[str(model_output[0]["label"])]
        return result

    # Split the text into sentences
    sentences: list = text.split(".")

    # Contains sentence and label sentence type
    classifications: list[StarClassification] = []
    # Classify each sentence
    for sentence in sentences:
        if sentence == "":
            continue
        classifications.append(StarClassification(
            sentence=sentence,
            category=predict(sentence)
        ))

    # Figure out what percentage of the total text is Action, Result, Situation, Task
    action = 0
    result = 0
    situation = 0
    task = 0
    for i in classifications:
        if i.category == "Action":
            action += 1
        elif i.category == "Result":
            result += 1
        elif i.category == "Situation":
            situation += 1
        elif i.category == "Task":
            task += 1
    total = action + result + situation + task

    # STAR is fulfilled if all categories are each hit by a sentence
    fulfilled_star = action > 0 and result > 0 and situation > 0 and task > 0

    # Round to 2 decimal places
    percentages = StarPercentages(
        action=round(action / total * 100, 2),
        result=round(result / total * 100, 2),
        situation=round(situation / total * 100, 2),
        task=round(task / total * 100, 2)
    )

    # Evaluate feedback
    feedback = percentage_feedback(percentages)

    return StarFeedbackEvaluation(
        fulfilled_star=fulfilled_star,
        percentages=percentages,
        classifications=classifications,
        feedback=feedback
    )

def percentage_feedback(percentages: StarPercentages) -> list[str]:
    """
    Provides feedback based on the final STAR values produced.
    """
    feedback = []
    if (
        percentages.action > 0
        and percentages.result > 0
        and percentages.situation > 0
        and percentages.task > 0
    ):
        feedback.append(
            "You have fulfilled all of the parts the STAR method. Well done!"
        )

    if percentages.action < 60:
        feedback.append(
            "You need to work on the Action category. Percentage of your response that is Action: "
            + str(percentages.action)
            + " The Action category is the most important part of the STAR method. Try to focus on what you did and how you did it. The expected percentage for the Action category is 60% of your total response."
        )
    if percentages.result < 15:
        feedback.append(
            "You need to work on the Result category. Percentage of your response that is Result:"
            + str(percentages.result)
            + "The Result category is the most important part of the STAR method. Try to focus on outcomes related to your task or action. The expected percentage for the Result category is 15% of your total response."
        )
    if percentages.situation < 15:
        feedback.append(
            "You need to work on the Situation category. Percentage of your Response that is Situation:"
            + str(percentages.situation)
            + "Try to focus on the context of the Situation and the circumstances that lead you to the task. The expected percentage for the Result category is 15% of your total response."
        )
    if percentages.task < 10:
        feedback.append(
            "You need to work on the Task category. Percentage of your Response that is Task:"
            + str(percentages.task)
            + "The Task category is the most important part of the STAR method. Try to focus on the task itself. The expected percentage for the Task category is 10% of your total response."
        )

    return feedback
