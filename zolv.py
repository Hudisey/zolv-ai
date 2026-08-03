import os
import base64
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__, template_folder='.', static_folder='.', static_url_path='')

# Render'daki GEMINI_API_KEY değişkenini alıyoruz
gemini_api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=gemini_api_key) if gemini_api_key else None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    prompt = data.get('prompt', '')
    mode = data.get('mode', 'text')
    
    if not client:
        return jsonify({'response': "Hata: GEMINI_API_KEY ortam değişkeni bulunamadı!"})

    try:
        # 1. GÖRSEL ÜRETME MODU (Image AI)
        if mode == 'image':
            result = client.models.generate_images(
                model='imagen-3.0-generate-002',
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    output_mime_type="image/jpeg",
                    aspect_ratio="1:1",
                )
            )
            
            for generated_image in result.generated_images:
                image_bytes = generated_image.image.image_bytes
                encoded_image = base64.b64encode(image_bytes).decode('utf-8')
                ai_response = f"İşte senin için ürettiğim görsel:<br><br><img src='data:image/jpeg;base64,{encoded_image}' alt='{prompt}' style='max-width:100%; border-radius:12px; margin-top:10px;'>"
                return jsonify({'response': ai_response})
            
            return jsonify({'response': "Görsel üretilemedi."})

        # 2. METİN VE KOD MODLARI (Text AI / Code AI)
        system_prompts = {
            'text': "Sen ZOLV.AI adında akıllı, samimi ve yardımsever bir yapay zeka asistanısın.",
            'code': "Sen uzman bir yazılım mühendisisin. Sorulara net, temiz kod blokları ve teknik açıklamalarla yanıt verirsin."
        }
        
        sys_prompt = system_prompts.get(mode, system_prompts['text'])

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=sys_prompt,
                temperature=0.7,
            ),
        )
        
        ai_response = response.text
        return jsonify({'response': ai_response})

    except Exception as e:
        return jsonify({'response': f"Gemini API hata oluştu: {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
