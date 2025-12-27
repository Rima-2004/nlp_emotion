from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

emotion_keywords = {
    "happy": ["happy", "joy", "excited", "great", "awesome", "fantastic"],
    "sad": ["sad", "down", "depressed", "unhappy", "cry"],
    "angry": ["angry", "mad", "furious", "hate"],
    "fear": ["fear", "afraid", "scared", "nervous", "anxious"]
}

emotion_emojis = {
    "happy": "😄",
    "sad": "😢",
    "angry": "😡",
    "fear": "😨",
    "neutral": "😐"
}


def detect_emotion_with_confidence(text):
    text_lower = text.lower()
    scores = {emotion: 0 for emotion in emotion_keywords}
    matched_words = []

    for emotion, keywords in emotion_keywords.items():
        for word in keywords:
            if word in text_lower:
                scores[emotion] += 1
                matched_words.append(word)

    total_matches = sum(scores.values())

    if total_matches == 0:
        return "neutral", 0, [], emotion_emojis["neutral"]

    emotion = max(scores, key=scores.get)
    confidence = int((scores[emotion] / total_matches) * 100)

    return emotion, confidence, matched_words, emotion_emojis[emotion]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/emotion", methods=["POST"])
def emotion():
    data = request.get_json(force=True)
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "Empty input"}), 400

    emotion, confidence, keywords, emoji = detect_emotion_with_confidence(text)

    return jsonify({
        "text": text,
        "emotion": emotion,
        "confidence": confidence,
        "keywords": keywords,
        "emoji": emoji
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
