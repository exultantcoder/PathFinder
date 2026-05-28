"use client";

import { useEffect, useState } from "react";

export default function Dashboard() {

  const [students, setStudents] =
    useState<any[]>([]);

  useEffect(() => {

    fetch(
      "https://ended-untangled-parted.ngrok-free.dev/students"
    )
      .then((res) => res.json())
      .then((data) =>
        setStudents(data)
      );

  }, []);

  return (

    <main className="min-h-screen bg-black text-white p-6">

      <h1 className="text-4xl font-bold mb-6">
        Teacher Dashboard
      </h1>

      <div className="grid gap-4">

        {students.map((student) => (

          <div
            key={student.student_id}
            className="bg-zinc-900 p-5 rounded-2xl"
          >

            <h2 className="text-2xl font-bold">
              {student.name}
            </h2>

            <p>
              Class: {student.class}
            </p>

            <p>
              Score: {student.score}
            </p>

            <p>
              Weak Topic:
              {" "}
              {student.weak_topic}
            </p>

          </div>
        ))}
      </div>
    </main>
  );
}