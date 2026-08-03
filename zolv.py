from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Groq istemcisi (OpenAI altyapısını kullanır ama tamamen ücretsizdir)
import os

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

class MesajIstegi(BaseModel):
    mesaj: str

@app.post("/yapay-zeka-sor")
def yapay_zeka_cevapla(istek: MesajIstegi):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Ücretsiz ve çok hızlı model
            messages=[{"role": "user", "content": istek.mesaj}]
        )
        cevap = response.choices[0].message.content
        return {"cevap": cevap}
    except Exception as e:
        return {"cevap": f"Bir hata oluştu: {str(e)}"}