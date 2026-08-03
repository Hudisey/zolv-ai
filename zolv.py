from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='.', static_folder='.', static_url_path='')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    prompt = data.get('prompt', '')
    mode = data.get('mode', 'text')
    
    # Buraya gerçek AI API entegrasyonunu (örn: Google Gemini API) bağlayabilirsin.
    # Şimdilik echo yapmaması için düzgün bir yanıt dönüyoruz:
    ai_response = f"ZOLV.AI ({mode} modu): '{prompt}' mesajını aldım. Sistemin bu şekilde çalışıyor!"
    
    return jsonify({'response': ai_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
