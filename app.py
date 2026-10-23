
from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
from sqlalchemy import func
import csv
import io
import os

app = Flask(__name__)

# Flask and database settings
database_url = os.environ.get("DATABASE_URL")

if database_url:
    if database_url.startswith("postgres://"):
        database_url = database_url.replace(
            "postgres://", "postgresql+psycopg://", 1
        )
    elif database_url.startswith("postgresql://"):
        database_url = database_url.replace(
            "postgresql://", "postgresql+psycopg://", 1
        )
elif os.environ.get("VERCEL"):
    database_url = "sqlite:////tmp/budget.db"
else:
    database_url = "sqlite:///budget.db"

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "BT-by-Sumit"

db = SQLAlchemy(app)

# Expense database table
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    category = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)


class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    category = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)


# Create the database table if it does not exist
with app.app_context():
    db.create_all()


# Available expense categories
Categories = [
    "Food", "Transport", "Rent", "Entertainment",
    "Utilities", "Healthcare", "Other"
]

IncomeCategories = [
    "Salary", "Freelance", "Business", "Gift", "Other"
]


# Convert a date string into a date object
def parse_date_or_none(value):
    if not value:
        return None

    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


# Home page: show expenses, income, totals and chart data
@app.route("/")
def index():
    start_str = (request.args.get("start") or "").strip()
    end_str = (request.args.get("end") or "").strip()
    selected_category = (request.args.get("categories") or "").strip()

    start_date = parse_date_or_none(start_str)
    end_date = parse_date_or_none(end_str)

    # Check the date range
    if start_str and not start_date:
        flash("Invalid start date.")
    if end_str and not end_date:
        flash("Invalid end date.")

    if start_date and end_date and start_date > end_date:
        flash("Start date cannot be after end date.")
        start_date = None
        end_date = None
        start_str = ""
        end_str = ""

    # Apply filters to the expense query
    q = Expense.query

    if start_date:
        q = q.filter(Expense.date >= start_date)

    if end_date:
        q = q.filter(Expense.date <= end_date)

    if selected_category in Categories:
        q = q.filter(Expense.category == selected_category)
    else:
        selected_category = ""

    expenses = q.order_by(
        Expense.date.desc(), Expense.id.desc()
    ).all()

    incomes = Income.query.order_by(
        Income.date.desc(), Income.id.desc()
    ).all()

    total_expenses = round(sum(e.amount for e in expenses), 2)
    total_income = round(sum(i.amount for i in incomes), 2)
    balance = round(total_income - total_expenses, 2)

    # Pie chart: total expense in each category
    cat_q = db.session.query(
        Expense.category,
        func.sum(Expense.amount)
    )

    if start_date:
        cat_q = cat_q.filter(Expense.date >= start_date)

    if end_date:
        cat_q = cat_q.filter(Expense.date <= end_date)

    if selected_category:
        cat_q = cat_q.filter(Expense.category == selected_category)

    cat_rows = cat_q.group_by(Expense.category).all()

    cat_labels = [category for category, _ in cat_rows]
    cat_values = [round(float(amount or 0), 2) for _, amount in cat_rows]

    # Bar chart: total expense for each day
    day_q = db.session.query(
        Expense.date,
        func.sum(Expense.amount)
    )

    if start_date:
        day_q = day_q.filter(Expense.date >= start_date)

    if end_date:
        day_q = day_q.filter(Expense.date <= end_date)

    if selected_category:
        day_q = day_q.filter(Expense.category == selected_category)

    day_rows = day_q.group_by(Expense.date).order_by(Expense.date).all()

    day_labels = [day.isoformat() for day, _ in day_rows]
    day_values = [round(float(amount or 0), 2) for _, amount in day_rows]

    return render_template(
        "index.html",
        categories=Categories,
        income_categories=IncomeCategories,
        today=date.today().isoformat(),
        expenses=expenses,
        incomes=incomes,
        total=total_expenses,
        total_income=total_income,
        balance=balance,
        start_str=start_str,
        end_str=end_str,
        selected_category=selected_category,
        cat_labels=cat_labels,
        cat_values=cat_values,
        day_labels=day_labels,
        day_values=day_values
    )


# Add a new expense
@app.route("/add", methods=["POST"])
def add_expense():
    description = (request.form.get("description") or "").strip()
    category = (request.form.get("category") or "").strip()
    amount_str = (request.form.get("amount") or "").strip()
    date_str = (request.form.get("date") or "").strip()

    # Check that all fields are filled
    if not description or not category or not amount_str or not date_str:
        flash("Please fill in all fields.")
        return redirect(url_for("index"))

    if category not in Categories:
        flash("Please select a valid category.")
        return redirect(url_for("index"))

    # Validate the amount
    try:
        amount = float(amount_str)

        if amount <= 0:
            raise ValueError

    except ValueError:
        flash("Amount must be a positive number.")
        return redirect(url_for("index"))

    # Validate the date
    expense_date = parse_date_or_none(date_str)

    if not expense_date:
        flash("Please enter a valid date.")
        return redirect(url_for("index"))

    # Save the expense in the database
    expense = Expense(
        description=description,
        category=category,
        amount=amount,
        date=expense_date
    )

    db.session.add(expense)
    db.session.commit()

    flash("Expense added successfully.")
    return redirect(url_for("index"))


@app.route("/add-income", methods=["POST"])
def add_income():
    description = (request.form.get("description") or "").strip()
    category = (request.form.get("category") or "").strip()
    amount_str = (request.form.get("amount") or "").strip()
    date_str = (request.form.get("date") or "").strip()

    if not description or not category or not amount_str or not date_str:
        flash("Please fill in all fields.")
        return redirect(url_for("index"))

    if category not in IncomeCategories:
        flash("Please select a valid income category.")
        return redirect(url_for("index"))

    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError
    except ValueError:
        flash("Income amount must be a positive number.")
        return redirect(url_for("index"))

    income_date = parse_date_or_none(date_str)
    if not income_date:
        flash("Please enter a valid date.")
        return redirect(url_for("index"))

    income = Income(
        description=description,
        category=category,
        amount=amount,
        date=income_date
    )

    db.session.add(income)
    db.session.commit()

    flash("Income added successfully.")
    return redirect(url_for("index"))


# Delete an expense
@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    expense = Expense.query.get_or_404(id)

    db.session.delete(expense)
    db.session.commit()

    flash("Expense deleted successfully.")
    return redirect(url_for("index"))


@app.route("/delete-income/<int:id>", methods=["POST"])
def delete_income(id):
    income = Income.query.get_or_404(id)

    db.session.delete(income)
    db.session.commit()

    flash("Income deleted successfully.")
    return redirect(url_for("index"))


# Show the edit form
@app.route("/edit/<int:id>", methods=["GET"])
def edit(id):
    expense = Expense.query.get_or_404(id)

    return render_template(
        "edit.html",
        expense=expense,
        categories=Categories,
        today=date.today().isoformat()
    )


# Update an existing expense
@app.route("/edit/<int:id>", methods=["POST"])
def edit_post(id):
    expense = Expense.query.get_or_404(id)

    description = (request.form.get("description") or "").strip()
    category = (request.form.get("category") or "").strip()
    amount_str = (request.form.get("amount") or "").strip()
    date_str = (request.form.get("date") or "").strip()

    # Validate the form fields
    if not description or not category or not amount_str or not date_str:
        flash("Please fill in all fields.")
        return redirect(url_for("edit", id=id))

    if category not in Categories:
        flash("Please select a valid category.")
        return redirect(url_for("edit", id=id))

    try:
        amount = float(amount_str)

        if amount <= 0:
            raise ValueError

    except ValueError:
        flash("Amount must be a positive number.")
        return redirect(url_for("edit", id=id))

    expense_date = parse_date_or_none(date_str)

    if not expense_date:
        flash("Please enter a valid date.")
        return redirect(url_for("edit", id=id))

    # Update the expense and save changes
    expense.description = description
    expense.category = category
    expense.amount = amount
    expense.date = expense_date

    db.session.commit()

    flash("Expense updated successfully.")
    return redirect(url_for("index"))


# Export filtered expenses as a CSV file
@app.route("/export.csv")
def export_csv():
    start_str = (request.args.get("start") or "").strip()
    end_str = (request.args.get("end") or "").strip()
    selected_category = (request.args.get("categories") or "").strip()

    start_date = parse_date_or_none(start_str)
    end_date = parse_date_or_none(end_str)

    # Create the query and apply available filters
    q = Expense.query

    if start_date:
        q = q.filter(Expense.date >= start_date)

    if end_date:
        q = q.filter(Expense.date <= end_date)

    if selected_category in Categories:
        q = q.filter(Expense.category == selected_category)

    expenses = q.order_by(Expense.date, Expense.id).all()

    # Write CSV data safely, including descriptions with commas
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["DATE", "DESCRIPTION", "CATEGORY", "AMOUNT"])

    for expense in expenses:
        writer.writerow([
            expense.date.isoformat(),
            expense.description,
            expense.category,
            f"{expense.amount:.2f}"
        ])

    # Send the CSV file to the browser
    response = make_response(output.getvalue())
    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    response.headers["Content-Disposition"] = (
        f"attachment; filename=expenses_{start_str or 'all'}_{end_str or 'all'}.csv"
    )

    return response


# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)
