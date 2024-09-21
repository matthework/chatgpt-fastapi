import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv

app = FastAPI()

# Load environment variables from a .env file
load_dotenv(override=True)

# OpenAI API v1.47.0
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

# CORS for cross-origin requests (React to FastAPI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for security in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return "FastAPI server is ready!"


@app.post("/api/chatgpt")
async def chat(request: Request):
    data = await request.json()
    user_input = data["message"]

    try:
        chat_completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": user_input,
                }
            ],
        )
        response = chat_completion.choices[0].message.content
        return {"response": response}

    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
