from flask import Flask, jsonify, render_template, request, url_for
from datetime import datetime

app = Flask(__name__)

MAX_NAME_LENGTH = 80

def validate_name(user: str):
    if not user or not user.strip():
        return None, "Please enter a valid name in the URL or the form."
    cleaned = user.strip()
    if len(cleaned) > MAX_NAME_LENGTH:
        return None, "Name is too long (max 80 characters)."
    if not cleaned.isprintable():
        return None, "Name contains unsupported characters."
    return cleaned, None

def analyze_text(user):
    vowels = set("aeiou")
    normalized = user.lower()
    vowel_count = sum(1 for ch in normalized if ch in vowels)
    consonant_count = sum(1 for ch in normalized if ch.isalpha() and ch not in vowels)
    digit_count = sum(1 for ch in normalized if ch.isdigit())
    space_count = sum(1 for ch in user if ch.isspace())
    words = [w for w in user.split() if w]
    unique_characters = len({ch for ch in normalized if ch.isalnum()})

    repeating = {ch: normalized.count(ch) for ch in set(normalized) if normalized.count(ch) > 1 and ch.isalpha()}

    strength_score = min(100, 20 + len(user) * 2 + len(words) * 5 + unique_characters * 3)
    strength_label = "Strong" if strength_score >= 75 else "Medium" if strength_score >= 50 else "Light"

    return {
        "original": user,
        "uppercase": user.upper(),
        "lowercase": normalized,
        "reversed": user[::-1],
        "length": len(user),
        "is_palindrome": normalized == normalized[::-1],
        "titlecase": user.title(),
        "vowels": vowel_count,
        "consonants": consonant_count,
        "digits": digit_count,
        "spaces": space_count,
        "words": len(words),
        "unique_characters": unique_characters,
        "repeating_characters": repeating,
        "strength_score": strength_score,
        "strength_label": strength_label,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None

    submitted = "user" in request.values
    user = request.values.get("user", "")

    if submitted:
        cleaned, error = validate_name(user)
        if cleaned:
            result = analyze_text(cleaned)
            result["share_link"] = url_for("home", user=cleaned, _external=True)

    return render_template("index.html", result=result, error=error)


@app.get("/api/analyze")
def api_analyze():
    user = request.args.get("user", "")
    cleaned, error = validate_name(user)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(analyze_text(cleaned))

if __name__ == "__main__":
    app.run(debug=True)