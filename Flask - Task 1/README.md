# Flask Name Analyzer

A small Flask app that reads a name from the query parameter or form, analyzes it (casing, counts, palindrome, strength), and shows a shareable link. Also exposes a JSON API.

## Run locally
1) Create/activate a virtualenv (optional but recommended).
2) Install deps:
```
pip install -r requirements.txt
```
3) Start the app:
```
python app.py
```
4) Open http://127.0.0.1:5000 and try `?user=YourName`.

## API
- GET `/api/analyze?user=YourName`
  - 200: analysis payload
  - 400: `{ "error": "..." }` when validation fails

## Tests
```
pytest
```

## Notes
- Max name length: 80 chars.
- Printable characters only; trims leading/trailing whitespace.
