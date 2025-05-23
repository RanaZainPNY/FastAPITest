from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from readData import read_excel_data
from readData import read_pdf_data
from groq import Groq

app = FastAPI()

client = Groq(
    api_key="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",
)
# Enable frontend connections (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple chatbot logic using query parameter ?q=hello
@app.get("/chat")
def simple_chatbot(q: str):
    user_question = q.lower().strip()
    akti_info = read_pdf_data('data/Arfa Karim Technology Incubator.pdf')
    courses_info = read_excel_data('data/Courses.xlsx')
    prompt_template = f"""
            Rules:
            1. The provided answer should not contain more than two lines
            2. If someone asks you about course dont disclose information about teacher
            3. Answers should only include what has been asked
            4. provide answers not more than two line?
            5. provide answers only from the given context.

            Context:
                Courses: 
                {courses_info}

                AKTI INFO:
                {akti_info}

            User Question:    
            {user_question}            
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt_template,
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    response  = chat_completion.choices[0].message.content

    return {"reply": response}
