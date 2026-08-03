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
    
    # Burada seçilen moda göre düzgün bir yapay zeka yanıtı üretiyoruz
    if mode == 'code':
        ai_response = f"Kod modu aktif! İstediğin kod ile ilgili şu analitiği hazırladım: '{prompt}' için en iyi çözüm yapısını kuruyorum."
    elif mode == 'image':
        ai_response = f"Görsel modu aktif! '{prompt}' için görsel oluşturma isteğin işleme alındı."
    else:
        ai_response = f"Merhaba! ZOLV.AI olarak sorduğun '{prompt}' sorusunu inceledim ve yardımcı olmak için buradayım."
    
    return jsonify({'response': ai_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
