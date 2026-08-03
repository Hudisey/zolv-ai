import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from groq import Groq

app = FastAPI()

# Render.com Environment Variables'tan Groq API Key'i güvenle çekiyoruz
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

try:
    app.mount("/static", StaticFiles(directory="."), name="static")
except Exception as e:
    print(f"StaticFiles mount hatası: {e}")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    file_path = "index.html"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    return HTMLResponse(content="<h1>index.html bulunamadı!</h1>", status_code=404)

@app.post("/chat")
async def chat_endpoint(message: str = Form(None), file: UploadFile = File(None)):
    try:
        user_msg = message if message else "Merhaba"
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": user_msg,
                }
            ],
            model="llama-3.1-8b-instant",
        )
        
        ai_reply = chat_completion.choices[0].message.content
        return JSONResponse(content={"reply": ai_reply}, status_code=200)
        
    except Exception as e:
        return JSONResponse(content={"detail": str(e)}, status_code=500)
