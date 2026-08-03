import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__, template_folder='.', static_folder='.', static_url_path='')

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
        system_prompts = {
            'text': "Sen ZOLV.AI adında akıllı, samimi ve yardımsever bir yapay zeka asistanısın.",
            'code': "Sen uzman bir yazılım mühendisisin. Sorulara net, temiz kod blokları ve teknik açıklamalarla yanıt verirsin."
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
        return jsonify({'response': f"Bir hata oluştu: {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
