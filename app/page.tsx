"use client";

import { useState } from "react";
import { supabase } from "../lib/supabase";

export default function Home() {

  const [question, setQuestion] =
    useState("");
  
  const [image, setImage] =
    useState<File | null>(null);

  const [answer, setAnswer] =
    useState<any>(null);

  const [selectedOption, setSelectedOption] =
    useState("");

  const [result, setResult] =
    useState("");

  const [answered, setAnswered] =
    useState(false);

  const [loading, setLoading] =
    useState(false);
  
  const [speaking, setSpeaking] =
  useState(false);

  const signIn = async () => {
    await supabase.auth.signInWithOAuth({
      provider: "github",
    });
  };
  const startListening = () => {

  const recognition =
    new (window as any)
    .webkitSpeechRecognition();

  recognition.lang = "en-US";

  recognition.onresult = (
    event: any
  ) => {

    setQuestion(
      event.results[0][0].transcript
    );
  };

  recognition.start();
};
  const askAI = async () => {

    setLoading(true);

    setAnswered(false);

    setResult("");

    setSelectedOption("");

    setAnswer(null);

    try {

      const formData = new FormData();

      formData.append(
        "question",
          question
      );

      formData.append(
        "email",
        "aarav.gupta1@gemmaedu.com"
      );

      if (image) {

        formData.append(
         "image",
          image
      );
    }

const response = await fetch(
  "http://127.0.0.1:8000/ask",
  {
    method: "POST",
    body: formData,
  }
);

      const data = await response.json();

      setAnswer(data);
      const utterance =
        new SpeechSynthesisUtterance(
          data.explanation
        );

      utterance.onstart = () =>
        setSpeaking(true);

      utterance.onend = () =>
        setSpeaking(false);

      speechSynthesis.speak(
        utterance
      );

    } catch (error) {

      setResult(
        "❌ Failed to get response."
      );

    } finally {

      setLoading(false);
    }
  };
  const checkAnswer = (
    option: string,
    index: number
  ) => {

    if (answered) return;

    setAnswered(true);

    setSelectedOption(option);

    const correct =
  answer?.quiz?.correct_answer;

const letters =
  ["A", "B", "C", "D"];

const selectedLetter =
  letters[index];

let correctOption = correct;

if (letters.includes(correct)) {

  const correctIndex =
    letters.indexOf(correct);

  correctOption =
    answer?.quiz?.options?.[
      correctIndex
    ];
}

const isCorrect =

  selectedLetter === correct ||

  option === correct ||

  option === correctOption;

if (isCorrect) {

  setResult(
    "✅ Correct Answer!"
  );

} else {

  setResult(
    `❌ Wrong. Correct answer is ${correctOption}`
  );
}

    fetch(
      "http://127.0.0.1:8000/submit_quiz",
      {
        method: "POST",

        headers: {
          "Content-Type":
            "application/json",
        },

        body: JSON.stringify({
          student_id:
            "c0899ba0-3227-4a92-8bac-8da7aea14722",

          quiz_id: answer.quiz_id,

          selected_answer: option,

          is_correct: isCorrect,

          subject: answer.subject,

          score:
            isCorrect ? 100 : 0,
        }),
      }
    );
  };

  return (

    <main className="min-h-screen bg-black text-white p-6">

      <h1 className="text-4xl font-bold mb-6">
        PathFinder
      </h1>

      <button
        onClick={signIn}
        className="bg-green-500 text-black px-4 py-2 rounded-xl mb-4"
      >
        Login with GitHub
      </button>

      <div className="flex gap-2 mb-6">

        <input
          value={question}
          onChange={(e) =>
            setQuestion(e.target.value)
          }
          placeholder="Ask a question..."
          className="flex-1 p-3 rounded-xl bg-zinc-900"
        />
        <input
          id="image-upload"
          hidden
          type="file"
          accept="image/*"
          capture="environment"
          onChange={(e) => 
            setImage(e.target.files?.[0] || null)
          }
          className="mb-4"
        />
        <label
          htmlFor="image-upload"
          className="bg-purple-500 px-4 py-2 rounded-xl cursor-pointer"
        >
          Upload Image
        </label>

        <button
          onClick={askAI}
          disabled={loading}
          className="bg-white text-black px-5 rounded-xl disabled:opacity-50"
        >
          {loading
            ? "Thinking..."
            : "Ask"}
        </button>
        <button
          onClick={startListening}
          className="bg-blue-500 px-4 rounded-xl"
        >
          🎤
        </button>
        <button
          onClick={() =>
            speechSynthesis.pause()
         }
          className="bg-yellow-500 px-4 rounded-xl"
        >
        ⏸
        </button>

        <button
          onClick={() =>
            speechSynthesis.resume()
          }
          className="bg-green-500 px-4 rounded-xl"
        >
         ▶
        </button>
      </div>

      <div className="bg-zinc-900 p-6 rounded-2xl">

        <h2 className="text-2xl font-bold mb-3">
          Explanation
        </h2>
      <div className="bg-zinc-800 p-4 rounded-xl mb-4">

  <p className="text-sm text-zinc-300">
    Personalized AI Learning Active
    
  </p>
  {answer?.teacher_notes_used && (

  <div className="mt-2 inline-block bg-blue-600 px-3 py-1 rounded-full text-sm">

    Teacher Material Integrated

  </div>
)}

  <p className="text-lg font-semibold">
    Adapting to Weak Topic:
    {" "}
    {answer?.weak_topic || "General"}
  </p>
<div className="mt-4">

  <div className="flex justify-between mb-1">

    <span>
      Learning Progress
    </span>

    <span>
      {answer?.score || 0}%
    </span>

  </div>

  <div className="w-full bg-zinc-700 rounded-full h-4">

    <div
      className="bg-green-500 h-4 rounded-full"
      style={{
        width: `${answer?.score || 0}%`
      }}
    />

  </div>
</div>
</div>

        <p className="mb-6 leading-7">
          {answer?.explanation}
        </p>

        <h3 className="text-xl font-semibold mb-2">
          Follow Up
        </h3>

        <p className="mb-6">
          {answer?.follow_up}
        </p>

        <h3 className="text-xl font-semibold mb-3">
          Quiz
        </h3>

        <p className="mb-4 text-lg">
          {answer?.quiz?.question}
        </p>

        <div className="flex flex-col gap-3">

          {answer?.quiz?.options?.map(
            (
              option: string,
              index: number
            ) => (

              <button
                key={option}

                onClick={() =>
                  checkAnswer(
                    option,
                    index
                  )
                }

                disabled={answered}

                className={`p-4 rounded-xl text-left transition-all

                ${
                  selectedOption === option

                    ? result.includes(
                        "Correct"
                      )

                      ? "bg-green-700"

                      : "bg-red-700"

                    : "bg-zinc-800 hover:bg-zinc-700"
                }

                ${
                  answered
                    ? "opacity-90"
                    : ""
                }
                `}
              >
                {option}
              </button>
            )
          )}

          <p className="mt-4 text-lg font-semibold">
            {result}
          </p>
        </div>
      </div>
    </main>
  );
}