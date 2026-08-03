import os
import urllib.parse
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__, template_folder='.', static_folder='.', static_url_path='')

gemini_api_key = os.environ.get("GEMINI_API_KEY")
if gemini_api_key:
    genai.configure(api_key=gemini_api_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    prompt = data.get('prompt', '')
    mode = data.get('mode', 'text')
    
    try:
        # 1. GÖRSEL ÜRETME MODU (Image AI)
        if mode == 'image':
            encoded_prompt = urllib.parse.quote(prompt)
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
            ai_response = f"İşte senin için ürettiğim görsel:<br><br><img src='{image_url}' alt='{prompt}' style='max-width:100%; border-radius:12px; margin-top:10px;'>"
            return jsonify({'response': ai_response})

        if not gemini_api_key:
            return jsonify({'response': "Hata: GEMINI_API_KEY ortam değişkeni bulunamadı!"})

        # 2. METİN VE KOD MODLARI (Text AI / Code AI)
        system_instructions = {
            'text': "Sen ZOLV.AI adında akıllı, samimi ve yardımsever bir yapay zeka asistanısın.",
            'code': "Sen uzman bir yazılım mühendisisin. Sorulara net, temiz kod blokları ve teknik açıklamalarla yanıt verirsin."
        }
        
        sys_prompt = system_instructions.get(mode, system_instructions['text'])

        model = genai.GenerativeModel(
            model_name='gemini-2.5-flash',
            system_instruction=sys_prompt
        )
        
        response = model.generate_content(prompt)
        ai_response = response.text
        
        return jsonify({'response': ai_response})

    except Exception as e:
        return jsonify({'response': f"Bir hata oluştu: {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
