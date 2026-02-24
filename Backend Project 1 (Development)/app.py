from flask import Flask, render_template, request
from flask_wtf import CSRFProtect
import html
import os
import re

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-me-in-prod")
csrf = CSRFProtect(app)

@app.route("/", methods=["GET", "POST"])
def index():
    matches = []
    error = None
    highlighted_text = ""
    test_string = ""
    regex_pattern = ""
    ignore_case_checked = False
    global_search_checked = True

    if request.method == "POST":
        # Trim whitespace to avoid accidental leading/trailing spaces causing miss-matches
        test_string = request.form.get("test_string", "").strip()
        regex_pattern = request.form.get("regex_pattern", "").strip()
        ignore_case = request.form.get("ignore_case")
        global_search = request.form.get("global_search")

        ignore_case_checked = bool(ignore_case)
        global_search_checked = bool(global_search)

        if not regex_pattern:
            error = "Regex pattern is required."
        else:
            flags_value = re.IGNORECASE if ignore_case else 0

            try:
                pattern = re.compile(regex_pattern, flags_value)

                if global_search:
                    iterator = pattern.finditer(test_string)
                else:
                    single_match = pattern.search(test_string)
                    iterator = [single_match] if single_match else []

                highlighted_parts = []
                cursor = 0

                for match in iterator:
                    if not match:
                        continue

                    start, end = match.start(), match.end()

                    matches.append({
                        "match": match.group(),
                        "start": start,
                        "end": end,
                        "groups": match.groups(),
                    })

                    highlighted_parts.append(html.escape(test_string[cursor:start]))
                    highlighted_parts.append(f"<mark>{html.escape(test_string[start:end])}</mark>")
                    cursor = end

                highlighted_parts.append(html.escape(test_string[cursor:]))
                highlighted_text = "".join(highlighted_parts) if matches else html.escape(test_string)

            except re.error as e:
                error = str(e)

    return render_template(
        "index.html",
        matches=matches,
        error=error,
        highlighted_text=highlighted_text,
        test_string=test_string,
        regex_pattern=regex_pattern,
        ignore_case_checked=ignore_case_checked,
        global_search_checked=global_search_checked,
    )

if __name__ == "__main__":
    app.run()