
from email.mime import image
import json

from supabase_client import supabase
from PIL import Image
from fastapi import FastAPI
from fastapi import UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import litert_lm
import pytesseract

MODEL_PATH = "/Users/monica_sue/.cache/huggingface/hub/models--litert-community--gemma-4-E2B-it-litert-lm/snapshots/b4f4f4df93418ddb4aa7da8bf33b584602a5b9f8/gemma-4-E2B-it.litertlm"

app = FastAPI()

def calculator(
    expression: str
) -> str:

    print(
        "CALCULATOR TOOL USED:",
        expression
    )

    return str(eval(expression))



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = litert_lm.Engine(MODEL_PATH)
tools = [calculator]

def get_student(email):
    response = supabase.table("students") \
        .select("*") \
        .eq("email", email) \
        .execute()

    return response.data


def get_progress(student_id,subject):
    response = supabase.table("student_progress") \
        .select("*") \
        .eq("student_id", student_id) \
        .eq("subject", subject) \
        .execute()
    if len(response.data) == 0:

        supabase.table(
            "student_progress"
        ).insert({

            "student_id": student_id,

            "subject": subject,

            "score": 0,

            "completed_lessons": 0,

            "weak_topic": subject,

            "learning_streak": 0

        }).execute()

        response = supabase.table(
            "student_progress"
        ).select("*") \
        .eq("student_id", student_id) \
        .eq("subject", subject) \
        .execute()
    return response.data


def get_recommendations(student_id,subject):
    response = supabase.table("learning_recommendations") \
        .select("*") \
        .eq("student_id", student_id) \
        .eq("subject", subject) \
        .execute()

    return response.data


def save_chat(student_id, email, question, answer, subject):
    supabase.table("student_chats").insert({
        "student_id": student_id,
        "email": email,
        "question": question,
        "answer": answer,
        "subject": subject
    }).execute()

def detect_subject(question):

    q = question.lower()

    if "math" in q or "algebra" in q:
        return "Math"

    elif "physics" in q or "force" in q:
        return "Physics"

    elif "biology" in q or "cell" in q:
        return "Biology"

    elif "history" in q:
        return "History"

    elif "grammar" in q or "english" in q:
        return "English"

    elif "rtos" in q or "embedded" in q:
        return "Embedded Systems"

    return "General"
def get_recent_chats(student_id,subject):

    response = supabase.table("student_chats") \
        .select("*") \
        .eq("student_id", student_id) \
        .eq("subject", subject) \
        .order("created_at", desc=True) \
        .limit(3) \
        .execute()

    return response.data

def get_teacher_notes(
    question,
    subject,
    student_id,
    student_class
):

    response = supabase.table(
        "teacher_notes"
    ).select("*").eq(
        "subject",
        subject
    ).execute()

    notes = response.data

    relevant_notes = []

    question_words = [
        word.lower()
        for word in question.split()
        if len(word) > 3
    ]

    for note in notes:

        matches = 0

        note_text = (
            note["note"].lower()
        )

        for word in question_words:

            if word in note_text:
                matches += 1

        if (
            note["student_id"] == student_id
            or
            note["class"] == student_class
            or
            note["student_id"] is None
        ):

            if matches > 0:

                relevant_notes.append(
                    note["note"]
                )

    return relevant_notes[:3]

def update_progress(student_id, subject):

    current = supabase.table("student_progress") \
        .select("*") \
        .eq("student_id", student_id) \
        .eq("subject", subject) \
        .execute()

    if len(current.data) == 0:
        return

    current_score = current.data[0]["score"]

    new_score = min(current_score + 1, 100)

    supabase.table("student_progress") \
        .update({
            "score": new_score,
            "subject": subject
        }) \
        .eq("student_id", student_id) \
            .eq("subject", subject) \
        .execute()



@app.post("/ask")
def ask(
    question: str = Form(...),
    email: str = Form(...),
    image: UploadFile = File(None)
):
    image_prompt = ""

    if image:

        try:
            img = Image.open(image.file)
        except:
            img = None

        extracted_text = (
            pytesseract.image_to_string(img)
        )

        image_prompt = f"""
        Text extracted from image:
        {extracted_text}
        """
    student = get_student(email)

    student_id = student[0]["student_id"]
    subject = detect_subject(question)
    is_math_query = any(
        char in question
        for char in ["+", "-", "*", "/"]
    )

    progress = get_progress(
    student_id,
    subject
    )
    

    recommendations = get_recommendations(student_id, subject)

    recent_chats = get_recent_chats(student_id, subject)
    teacher_notes = get_teacher_notes(

        question,

        subject,

        student_id,

        student[0]["class"]

    )
    print("TEACHER NOTES:", teacher_notes)
    
    prompt = f"""
    You are an educational AI tutor.

    Student Name:
    {student[0]["name"]}

    Student Class:
    {student[0]["class"]}

    Student Progress:
    {progress}

    Learning Recommendations:
    {
    recommendations
    if not is_math_query
    else "None"
    }

    IMPORTANT TEACHER MATERIAL:
    {teacher_notes}

    You MUST prioritize and reference the teacher material in your explanation whenever relevant.
    If the student's weak topic matches the question subject:
    - explain more carefully
    - use simpler examples
    - provide extra guidance
    Student Question:
    {question}
    Image Context:
    {image_prompt}

    Recent Question:
    {
    recent_chats[0]["question"]
    if len(recent_chats) > 0
    else "None"
    }

    Keep the answer concise.
    If the student score is low, explain more simply.
    If the student score is high, explain with slightly deeper concepts.
    Use examples suitable for class {student[0]["class"]} students.
    Focus especially on weak topic:
    {
    progress[0]["weak_topic"]
    if not is_math_query
    else "None"
    }
    Answer in under 120 words.
    Ask one follow-up question.
    Use teacher notes if relevant.
    
        IMPORTANT:
    If teacher notes are retrieved, prioritize them over general knowledge.
    Mention one relevant idea from the teacher notes naturally.
    If teacher notes are available, explicitly mention that you are using teacher-provided learning material.
    Return your response ONLY in valid JSON format.

    Use this exact structure:

    {{
    "explanation": "...",
    "follow_up": "...",
    "quiz": {{
        "question": "...",
        "options": [
        "A. ...",
        "B. ...",
        "C. ...",
        "D. ..."
        ],
        "correct_answer": "..."
     }}
    }}
    """

    if any(
        char in question
        for char in ["+", "-", "*", "/", "=", "(", ")","1","2","3","4","5","6","7","8","9","0"]
    ):

        active_tools = tools

    else:

        active_tools = []

    with engine.create_conversation(
        tools=active_tools
    ) as conversation:

        gemma_response = (
            conversation.send_message(
                prompt
            )
        )
    
    raw_text = gemma_response["content"][0]["text"]

    raw_text = raw_text.replace("```json", "")
    raw_text = raw_text.replace("```", "")
    raw_text = raw_text.strip()
    try:
        parsed_response = json.loads(raw_text)
        if "quiz" not in parsed_response:
            parsed_response["quiz"] = {
            "question": "",
            "options": [],
            "correct_answer": ""
        }

        if "follow_up" not in parsed_response:
            parsed_response["follow_up"] = ""
        if "explanation" not in parsed_response:
            parsed_response["explanation"] = (
            "No explanation generated."
        )

    except Exception as e:

        print("JSON ERROR:", e)
        print(raw_text)

        parsed_response = {
            "explanation": raw_text,
            "follow_up": "",
            "quiz": {
                "question": "",
                "options": [],
                "correct_answer": ""
            }
        }
    

    subject = detect_subject(question)

    save_chat(
        student_id,
        email,
        question,
        parsed_response["explanation"],
        subject
    )
    quiz_insert = supabase.table(
        "quizzes"
    ).insert({

    "subject": subject,

        "question":
            parsed_response["quiz"]["question"],

        "options":
            parsed_response["quiz"]["options"],

        "correct_answer":
            parsed_response["quiz"]["correct_answer"]

    }).execute()

    quiz_id = (
        quiz_insert.data[0]["quiz_id"]
    )
    return {
    "subject": subject,
    "explanation":
        parsed_response["explanation"],

    "follow_up":
        parsed_response["follow_up"],

    "quiz":
        parsed_response["quiz"],
    "quiz_id": quiz_id,

    "weak_topic":
        progress[0]["weak_topic"],
    "score":
        progress[0]["score"],
    "teacher_notes_used": True
}

@app.post("/submit_quiz")
def submit_quiz(data: dict):

    supabase.table("quiz_results").insert({
        "student_id": data["student_id"],
        "quiz_id": data["quiz_id"],
        "subject": data["subject"],
        "selected_answer": data["selected_answer"],
        "is_correct": data["is_correct"],
        "score": data["score"],
        "subject": data["subject"]
    }).execute()

    if data["is_correct"]:

        current = supabase.table("student_progress") \
            .select("*") \
            .eq("student_id", data["student_id"]) \
            .eq("subject", data["subject"]) \
            .execute()

        if len(current.data) > 0:

            current_score = current.data[0]["score"]

            new_score = min(current_score + 1, 100)

            supabase.table("student_progress") \
                .update({
                    "score": new_score
                }) \
                .eq("student_id", data["student_id"]) \
                .eq("subject", data["subject"]) \
                .execute()
        if not data["is_correct"]:

            supabase.table(
                "student_progress"
            ).update({

                "weak_topic":
                    data["subject"]

            }).eq(
                "student_id",
                data["student_id"]

            ).eq(
                "subject",
                data["subject"]

            ).execute()

    return {
        "message": "Quiz result saved"
    }
@app.get("/students")
def get_students():

    students_response = supabase.table(
        "students"
    ).select("*").execute()

    progress_response = supabase.table(
        "student_progress"
    ).select("*").execute()

    students =students_response.data

    progress =progress_response.data

    merged = []

    for student in students:

        student_progress = next(
            (
                p for p in progress
                if p["student_id"]
                == student["student_id"]
            ),
            {}
        )

        merged.append({

            "student_id":
                student["student_id"],

            "name":
                student["name"],

            "email":
                student["email"],

            "class":
                student["class"],

            "score":
                student_progress.get(
                    "score",
                    0
                ),

            "weak_topic":
                student_progress.get(
                    "weak_topic",
                    "N/A"
                )
        })

    return merged