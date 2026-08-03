from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    prompt = data.get('prompt', '')
    mode = data.get('mode', 'text')
    
    # Buraya kendi AI yanıt mantığını ekleyebilirsin
    ai_response = f"ZOLV.AI ({mode} modu) yanıtı: {prompt}"
    
    return jsonify({'response': ai_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
