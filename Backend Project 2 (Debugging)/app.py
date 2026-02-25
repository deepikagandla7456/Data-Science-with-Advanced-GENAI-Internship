from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

notes = []

# Single home route handles display and note creation
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        note = request.form.get("note")
        if note and note.strip() != "":
            notes.append(note.strip())

        # Post/Redirect/Get to prevent duplicate submissions on refresh
        return redirect(url_for("index"))

    return render_template("home.html", notes=notes)


if __name__ == '__main__':
    # Debug off for submission; set to True only during local development
    app.run(debug=False)