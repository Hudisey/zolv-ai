import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__, template_folder='.', static_folder='.', static_url_path='')

# Render'a eklediğin Groq API anahtarını alıyoruz
groq_api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=groq_api_key) if groq_api_key else None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    prompt = data.get('prompt', '')
    mode = data.get('mode', 'text')
    
    if not client:
        return jsonify({'response': "Hata: GROQ_API_KEY ortam değişkeni bulunamadı!"})

    try:
        # Modlara göre sistem komutları (istemciye davranış biçimi)
        system_prompts = {
            'text': "Sen ZOLV.AI adında akıllı ve yardımsever bir yapay zeka asistanısın.",
            'code': "Sen uzman bir yazılım mühendisisin. Sadece temiz kodlar ve teknik açıklamalar sunarsın.",
            'image': "Sen yaratıcı bir görsel tasarım asistanısın. Görsel fikirleri ve promptlar üretebilirsin."
        }
        
        sys_prompt = system_prompts.get(mode, system_prompts['text'])

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2048,
        )
        
        ai_response = completion.choices[0].message.content
        return jsonify({'response': ai_response})

    except Exception as e:
        return jsonify({'response': f"AI bağlantı hatası: {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
