from datetime import date

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template(
        "index.html",
        today=date.today().isoformat(),
        categories=[
            "Food", "Transport", "Rent", "Entertainment",
            "Utilities", "Healthcare", "Other"
        ],
        income_categories=[
            "Salary", "Freelance", "Business", "Gift", "Other"
        ],
    )


if __name__ == "__main__":
    app.run(debug=True)
