from flask import Flask, jsonify, request, render_template
import os
from flask import Flask, jsonify, request
from groq import Groq
import google.generativeai as genai

app = Flask(__name__)

groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))


@app.route("/api/chat", methods=["POST"])
def chat():
  data = request.json
  prompt = data.get("prompt")
  mode = data.get("mode", "text")

  try:
    if mode == "text":
      res = groq_client.chat.completions.create(
          model="llama-3.3-70b-versatile",
          messages=[{"role": "user", "content": prompt}],
      )
      return jsonify({"response": res.choices[0].message.content})

    elif mode == "code":
      res = groq_client.chat.completions.create(
          model="llama-3.3-70b-versatile",
          messages=[
              {
                  "role": "system",
                  "content": (
                      "Sen kıdemli bir yazılım mühendisisin. Sadece temiz kod"
                      " üret."
                  ),
              },
              {"role": "user", "content": prompt},
          ],
      )
      return jsonify({"response": res.choices[0].message.content})

    elif mode == "image":
      model = genai.GenerativeModel("gemini-1.5-flash")
      res = model.generate_content(
          f"Görsel için detaylı prompt oluştur: {prompt}"
      )
      return jsonify({"response": res.text})

    return jsonify({"error": "Geçersiz mod!"}), 400
  except Exception as e:
    return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
  app.run(debug=True)
