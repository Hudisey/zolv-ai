import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

# 1. STATİK DOSYALARI TANIT (LOGO, FAVICON VB.)
# Bu satır, projenin ana klasöründeki tüm dosyaları dış dünyaya açar.
# render.com üzerinde çalışırken bu genellikle '/' kök dizinidir.
try:
    app.mount("/static", StaticFiles(directory="."), name="static")
except Exception as e:
    print(f"StaticFiles mount edilemedi (muhtemelen dizin boş veya yanlış): {e}")

# 2. ANA SAYFA YÖNLENDİRMESİ
@app.get("/", response_class=HTMLResponse)
async def read_index():
    """
    Tarayıcı ana sayfaya ('/') girdiğinde index.html dosyasını okuyup döndürür.
    """
    file_path = "index.html"
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return HTMLResponse(content=f.read(), status_code=200)
        except Exception as e:
            return HTMLResponse(content=f"<h1>Hata: index.html okunamadı</h1><p>{e}</p>", status_code=500)
    else:
        # Eğer index.html yoksa, render.com hata vermemesi için basit bir HTML dön
        return HTMLResponse(content="""
            <!DOCTYPE html>
            <html lang="tr">
            <head>
                <meta charset="UTF-8">
                <title>ZOLV.AI - Kurulum</title>
                <style>
                    body { font-family: sans-serif; background: #0e0e0e; color: white; text-align: center; padding-top: 50px; }
                </style>
            </head>
            <body>
                <h1>Hoş Geldiniz</h1>
                <p>Henüz bir <code>index.html</code> dosyası oluşturulmadı veya bulunamadı.</p>
                <p>Lütfen proje ana dizinine <code>index.html</code> dosyanızı yükleyin.</p>
            </body>
            </html>
        """, status_code=404)

# 3. CHAT İŞLEMLERİ İÇİN ÖRNEK ROTA
@app.post("/chat")
async def chat_endpoint(message: str = Form(...), file: UploadFile = File(None)):
    """
    Chat formundan gelen mesajı ve varsa dosyayı işler (şimdilik örnek yanıt).
    """
    try:
        file_info = f" (Dosya: {file.filename})" if file else ""
        return JSONResponse(content={"reply": f"Mesajınız alındı: '{message}'{file_info}. Yapay zeka yakında entegre edilecek."}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"detail": f"Chat işleminde hata oluştu: {str(e)}"}, status_code=500)

# 4. ÖZEL HATA YÖNETİMİ ({"detail":"Not Found"} yerine daha açıklayıcı olması için)
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    if exc.status_code == 404 and request.url.path.startswith("/"):
        # Eğer ana sayfadaki dosyalar (logo.png vb.) bulunamazsa hata sayfasına yönlendirme yapma, sadece 404 dön
        # veya özel bir hata mesajı döndür.
        return HTMLResponse(content="<h1>Sayfa Bulunamadı</h1><p>Aradığınız sayfa veya dosya sunucuda mevcut değil.</p>", status_code=404)
    return JSONResponse(content={"detail": exc.detail}, status_code=exc.status_code)
