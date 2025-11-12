const sampleAPIResponse = {
  aggregateScore: 0,
  facialStatistics: {
    frequencyOfSecondEmotion: 0.05714285714285714,
    frequencyOfThirdEmotion: 0.02857142857142857,
    frequencyOfTopEmotion: 0.9142857142857143,
    topThreeEmotions: ["neutral", "surprise", "fear"],
  },
  isStructured: 1,
  isStructuredPercent: 0.664770479416352,
  overallFacialEmotion: "neutral",
  overallSentiment: "NEUTRAL",
  timeline: [
    {
      audioSentiment: "NEUTRAL",
      end: 2158,
      facialEmotion: ["surprise", "neutral"],
      start: 430,
    },
    {
      audioSentiment: "POSITIVE",
      end: 7042,
      facialEmotion: ["neutral", "neutral"],
      start: 2194,
    },
    {
      audioSentiment: "NEUTRAL",
      end: 7290,
      facialEmotion: ["neutral", "neutral"],
      start: 7066,
    },
    {
      audioSentiment: "NEUTRAL",
      end: 8070,
      facialEmotion: ["neutral", "neutral"],
      start: 7340,
    },
    {
      audioSentiment: "NEUTRAL",
      end: 10650,
      facialEmotion: ["surprise", "neutral"],
      start: 8450,
    },
    {
      audioSentiment: "NEGATIVE",
      end: 14694,
      facialEmotion: ["neutral", "fear"],
      start: 10760,
    },
    {
      audioSentiment: "POSITIVE",
      end: 19700,
      facialEmotion: ["fear", "neutral"],
      start: 14852,
    },
    {
      audioSentiment: "NEUTRAL",
      end: 22362,
      facialEmotion: ["neutral", "neutral"],
      start: 21290,
    },
    {
      audioSentiment: "NEGATIVE",
      end: 23160,
      facialEmotion: ["neutral", "neutral"],
      start: 22436,
    },
  ],
  topFiveKeywords: [
    {
      count: 1,
      rank: 0.15,
      text: "computer science knowledge",
      timestamps: [{ end: 18682, start: 17840 }],
    },
    {
      count: 2,
      rank: 0.14,
      text: "computer science",
      timestamps: [
        { end: 5578, start: 4786 },
        { end: 18418, start: 17840 },
      ],
    },
    {
      count: 1,
      rank: 0.11,
      text: "Stevens Institute",
      timestamps: [{ end: 3922, start: 3356 }],
    },
    {
      count: 1,
      rank: 0.11,
      text: "Google technology",
      timestamps: [{ end: 19700, start: 18836 }],
    },
    {
      count: 1,
      rank: 0.09,
      text: "Hamsunasami",
      timestamps: [{ end: 2158, start: 1376 }],
    },
  ],
};

export const answerOneResponse = {
  evaluation: {
    timeline: [
      {
        start: 430,
        end: 2158,
        audioSentiment: "NEUTRAL",
        facialEmotion: ["fear", "neutral"],
      },
      {
        start: 2194,
        end: 7078,
        audioSentiment: "POSITIVE",
        facialEmotion: ["neutral", "neutral"],
      },
      {
        start: 7114,
        end: 8262,
        audioSentiment: "NEUTRAL",
        facialEmotion: ["neutral", "neutral"],
      },
      {
        start: 8456,
        end: 10230,
        audioSentiment: "NEUTRAL",
        facialEmotion: ["surprise", "neutral"],
      },
      {
        start: 10730,
        end: 14862,
        audioSentiment: "NEGATIVE",
        facialEmotion: ["happy", "neutral"],
      },
      {
        start: 15056,
        end: 19700,
        audioSentiment: "NEUTRAL",
        facialEmotion: ["neutral", "neutral"],
      },
      {
        start: 21290,
        end: 22422,
        audioSentiment: "NEUTRAL",
        facialEmotion: ["neutral", "neutral"],
      },
      {
        start: 22496,
        end: 23160,
        audioSentiment: "NEGATIVE",
        facialEmotion: ["neutral", "happy"],
      },
    ],
    isStructured: 1,
    isStructuredPercent: 0.7315355281979502,
    facialStatistics: {
      topThreeEmotions: ["neutral", "surprise", "happy"],
      frequencyOfTopEmotion: 0.9,
      frequencyOfSecondEmotion: 0.05714285714285714,
      frequencyOfThirdEmotion: 0.04285714285714286,
    },
    overallFacialEmotion: "neutral",
    overallSentiment: "NEUTRAL",
    topFiveKeywords: [
      {
        count: 1,
        rank: 0.14,
        text: "computer science knowledge",
        timestamps: [{ start: 17840, end: 18742 }],
      },
      {
        count: 2,
        rank: 0.13,
        text: "computer science",
        timestamps: [
          { start: 4786, end: 5578 },
          { start: 17840, end: 18478 },
        ],
      },
      {
        count: 1,
        rank: 0.12,
        text: "Climate change misinformation",
        timestamps: [{ start: 10730, end: 12718 }],
      },
      {
        count: 1,
        rank: 0.11,
        text: "genetic modification",
        timestamps: [{ start: 12814, end: 13702 }],
      },
      {
        count: 1,
        rank: 0.11,
        text: "Stevens Institute",
        timestamps: [{ start: 3356, end: 3922 }],
      },
    ],
    aggregateScore: 59.89,
  },
};

export const answerTwoResponse = {
  evaluation: {
    timeline: [
      {
        start: 730,
        end: 2398,
        audioSentiment: "NEUTRAL",
        facialEmotion: ["neutral", "neutral"],
      },
      {
        start: 2434,
        end: 9642,
        audioSentiment: "POSITIVE",
        facialEmotion: ["neutral", "neutral"],
      },
      {
        start: 9836,
        end: 12090,
        audioSentiment: "NEUTRAL",
        facialEmotion: ["neutral", "neutral"],
      },
      {
        start: 12200,
        end: 21030,
        audioSentiment: "NEGATIVE",
        facialEmotion: ["neutral", "neutral"],
      },
      {
        start: 21410,
        end: 24138,
        audioSentiment: "NEGATIVE",
        facialEmotion: ["neutral", "neutral"],
      },
      {
        start: 24284,
        end: 31542,
        audioSentiment: "POSITIVE",
        facialEmotion: ["neutral", "neutral"],
      },
      {
        start: 31676,
        end: 35358,
        audioSentiment: "POSITIVE",
        facialEmotion: ["neutral", "neutral"],
      },
      {
        start: 35504,
        end: 49150,
        audioSentiment: "POSITIVE",
        facialEmotion: ["neutral", "neutral"],
      },
      {
        start: 49270,
        end: 55880,
        audioSentiment: "POSITIVE",
        facialEmotion: ["neutral", "neutral"],
      },
      {
        start: 56210,
        end: 56640,
        audioSentiment: "POSITIVE",
        facialEmotion: ["neutral", "neutral"],
      },
    ],
    isStructured: 1,
    isStructuredPercent: 0.6637054519845063,
    facialStatistics: {
      topThreeEmotions: ["neutral", "surprise", "N/A"],
      frequencyOfTopEmotion: 0.9866666666666667,
      frequencyOfSecondEmotion: 0.013333333333333334,
      frequencyOfThirdEmotion: 0.0,
    },
    overallFacialEmotion: "neutral",
    overallSentiment: "POSITIVE",
    topFiveKeywords: [
      {
        count: 2,
        rank: 0.09,
        text: "computer science",
        timestamps: [
          { start: 5338, end: 5902 },
          { start: 24284, end: 24982 },
        ],
      },
      {
        count: 1,
        rank: 0.08,
        text: "weird symbols",
        timestamps: [{ start: 17096, end: 17830 }],
      },
      {
        count: 1,
        rank: 0.08,
        text: "global issues",
        timestamps: [{ start: 45466, end: 46722 }],
      },
      {
        count: 1,
        rank: 0.08,
        text: "Steams Institute",
        timestamps: [{ start: 3944, end: 4522 }],
      },
      {
        count: 1,
        rank: 0.08,
        text: "Google Developer Student Club lead",
        timestamps: [{ start: 7856, end: 9642 }],
      },
    ],
    aggregateScore: 52.55,
  },
};

export default sampleAPIResponse;
