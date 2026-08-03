from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles  # <-- BU EKLENDİ
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Resimlerin ve statik dosyaların okunabilmesi için kök dizini bağlıyoruz
app.mount("/static", StaticFiles(directory="."), name="static")

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

class MesajIstegi(BaseModel):
    mesaj: str

@app.get("/", response_class=HTMLResponse)
def ana_sayfa():
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "index.html bulunamadı!"

@app.post("/yapay-zeka-sor")
def yapay_zeka_cevapla(istek: MesajIstegi):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": istek.mesaj}]
        )
        cevap = response.choices[0].message.content
        return {"cevap": cevap}
    except Exception as e:
        return {"cevap": f"Bir hata oluştu: {str(e)}"}
