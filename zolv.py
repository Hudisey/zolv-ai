import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

# Statik dosyaları (logo, favicon vb.) dış dünyaya aç
try:
    # Dizin olarak mevcut klasörü kullan
    app.mount("/static", StaticFiles(directory="."), name="static")
except Exception as e:
    print(f"StaticFiles mount hatası: {e}")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    """
    Ana sayfa isteğinde index.html dosyasını döndürür.
    """
    file_path = "index.html"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    return HTMLResponse(content="<h1>index.html bulunamadı!</h1>", status_code=404)

@app.post("/chat")
async def chat_endpoint(message: str = Form(None), file: UploadFile = File(None)):
    """
    Chat isteklerini işler. Buraya gerçek AI entegrasyonu gelecek.
    """
    try:
        file_info = f" (Dosya: {file.filename})" if file else ""
        user_msg = message if message else "Boş mesaj"
        
        # --- ESKİ STATİK YANIT BURADAYDI, KALDIRILDI ---
        # Artık gerçek AI bağlandığında burası dolacak.
        # Şimdilik bir onay mesajı dönelim:
        return JSONResponse(content={"reply": f"Mesajınız alındı: '{user_msg}'{file_info}. AI entegrasyonu yakında aktif olacak!"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"detail": str(e)}, status_code=500)
