from flask import Flask, request, jsonify
from flask_cors import CORS
from main_single_sentence import polarity_prediction

app = Flask(__name__)
CORS(app)  # Cross-Origin Resource Sharing (CORS) desteği ekleyelim

@app.route("/analyze", methods=["POST"])
def analyze_sentiment():
    data = request.get_json()
    text = data.get("text", "")
    
    if not text.strip():
        return jsonify({"error": "Boş bir cümle gönderildi!"}), 400

    sentiment = polarity_prediction(text)
    print(f"Gelen metin: {text} | Hesaplanan sentiment: {sentiment}")  # Terminalde göster

    if sentiment is None:
        return jsonify({"error": "Analiz edilemedi!"}), 500  # Eğer `None` dönerse hata ver

    return jsonify({"sentiment": sentiment})


if __name__ == "__main__":
    app.run(debug=True)
