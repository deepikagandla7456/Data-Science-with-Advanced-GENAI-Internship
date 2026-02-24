# Regex Playground (Flask)

Small Flask app to test regular expressions with live highlights and match details.

## How to run
1. Create/activate a Python env (optional but recommended).
2. Install deps:
```
pip install -r requirements.txt
```
3. Set a secret key before starting (needed for CSRF):
- PowerShell: `$env:SECRET_KEY = "your-strong-secret-key"`
4. Start the app:
```
python app.py
```
5. Open http://127.0.0.1:5000/ in the browser.

## What it does
- Enter a regex and test string, toggle ignore-case and global flags.
- Highlights all matches and lists start/end positions.
- Presets: simple word, emails, URLs, name variant.
- CSRF protection enabled for the form.