from supabase_client import supabase
import litert_lm


MODEL_PATH = "/Users/monica_sue/.cache/huggingface/hub/models--litert-community--gemma-4-E2B-it-litert-lm/snapshots/b4f4f4df93418ddb4aa7da8bf33b584602a5b9f8/gemma-4-E2B-it.litertlm"

with litert_lm.Engine(MODEL_PATH) as engine:
    with engine.create_conversation() as conversation:

        gemma_response = conversation.send_message(
            "You are an educational AI tutor. Teach me RTOS simply."
        )

        print(gemma_response["content"][0]["text"])


def get_student(email):
    response = supabase.table("students") \
        .select("*") \
        .eq("email", email) \
        .execute()

    return response.data
student = get_student(
    "aarav.gupta1@gemmaedu.com"
)

print(student)

def get_progress(student_id):
    response = supabase.table("student_progress") \
        .select("*") \
        .eq("student_id", student_id) \
        .execute()

    return response.data


def get_recommendations(student_id):
    response = supabase.table("learning_recommendations") \
        .select("*") \
        .eq("student_id", student_id) \
        .execute()

    return response.data 
response = supabase.table("students") \
    .select("*") \
    .execute()

print(response.data)


student_id = student[0]["student_id"]

progress = get_progress(student_id)

recommendations = get_recommendations(student_id)

print(student)
print(progress)
print(recommendations)
def save_chat(student_id, email, question, answer,subject):
    supabase.table("student_chats").insert({
        "student_id": student_id,
        "email": email,
        "question": question,
        "answer": answer,
        "subject": subject
    }).execute()
print(gemma_response["content"][0]["text"])
save_chat(
    student_id,
    student[0]["email"],
    "Teach me RTOS simply",
    gemma_response["content"][0]["text"],
    subject= "RTOS"
)

