from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openai import OpenAI
import os
import base64

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="."), name="static")

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

@app.get("/", response_class=HTMLResponse)
def ana_sayfa():
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "index.html bulunamadı!"

@app.post("/yapay-zeka-sor")
async def yapay_zeka_cevapla(
    mesaj: str = Form(...), 
    file: UploadFile = None
):
    try:
        messages_content = [{"type": "text", "text": mesaj}]
        
        # Eğer kullanıcı bir görsel yüklediyse base64 formatına çevirip modele verelim
        if file:
            image_bytes = await file.read()
            base64_image = base64.b64encode(image_bytes).decode("utf-8")
            messages_content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            })

        response = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",  # Groq görsel okuma destekli modeli
            messages=[{"role": "user", "content": messages_content}],
            max_tokens=1024
        )
        cevap = response.choices[0].message.content
        return {"cevap": cevap}
    except Exception as e:
        return {"cevap": f"Bir hata oluştu: {str(e)}"}
