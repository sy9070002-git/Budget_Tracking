
# 💰 Budget Tracker

A Python-based Budget Tracker that helps users manage their personal finances by recording income and expenses, tracking spending, and calculating their remaining balance.

## 📌 Project Overview

The Budget Tracker is a personal finance management project developed using Python. Its goal is to make it easier to monitor daily transactions, organize expenses into categories, and understand spending habits.

This project will be developed step-by-step, starting with a basic Python program and gradually adding data storage, analysis, visualization, and a web dashboard.

## 🎯 Objectives

- Track income and expenses.
- Categorize daily spending.
- Calculate total income, expenses, and balance.
- Store transaction records.
- Analyze monthly spending patterns.
- Visualize financial data using charts.
- Build a user-friendly dashboard.

## ✨ Features

### Basic Features
- Add income transactions.
- Add expense transactions.
- View transaction history.
- Categorize transactions.
- Calculate the remaining balance.

### Planned Features
- Save transactions using CSV files.
- Analyze data using Pandas.
- Create charts using Matplotlib.
- Store data in an SQLite database.
- Build a web dashboard using Flask.
- Set monthly budgets and spending limits.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming |
| CSV | Transaction storage |
| Pandas | Data analysis |
| Matplotlib | Data visualization |
| SQLite | Database management |
| Flask | Web application |
| HTML and CSS | Dashboard interface |
| Git and GitHub | Version control |

*Some technologies will be added in future development phases.*

## 📂 Project Structure

```text
Budget_Tracker/
│
├── main.py
├── transactions.csv
├── README.md
│
├── analysis.py       # Planned: data analysis
├── charts.py         # Planned: visualizations
├── database.db       # Planned: SQLite database
│
├── app.py            # Planned: Flask application
├── templates/
│   └── index.html
│
└── static/
    └── style.css
```

## ⚙️ Installation and Setup

### 1. Install Python

Download Python from:

https://www.python.org/downloads/

### 2. Clone the Repository

```bash
git clone https://github.com/sy9070002-git/Budget_tracker.git
```

### 3. Open the Project Folder

```bash
cd Budget_tracker
```

### 4. Run the Python Program

```bash
python main.py
```

## 📊 How It Works

1. Run the application.
2. Select an option from the menu.
3. Enter income or expense details.
4. View transaction history.
5. Check your total income, expenses, and available balance.

## 🗺️ Development Roadmap

- [x] Create the project structure.
- [ ] Build the basic Python application.
- [ ] Add income and expense management.
- [ ] Calculate the available balance.
- [ ] Implement CSV data storage.
- [ ] Perform data analysis using Pandas.
- [ ] Create charts using Matplotlib.
- [ ] Integrate an SQLite database.
- [ ] Develop a Flask web dashboard.
- [ ] Add budget limits and monthly reports.
- [ ] Deploy the application.

## 🚀 Future Improvements

- Monthly budget planning.
- Category-wise expense reports.
- Income-versus-expense dashboard.
- Search and filter transactions.
- Export financial reports.
- Responsive web interface.
- Secure user authentication.

## ☁️ Deploying to Vercel

1. Push the project to GitHub. Make sure `app.py`, `vercel.json`, and
   `requirements.txt` are in the repository root.
2. In Vercel, select **Add New → Project** and import the GitHub repository.
3. Set the **Root Directory** to the folder containing those files. Leave the
   framework preset as **Other** (or let Vercel detect Python), then deploy.
4. If the project was already deployed, trigger a new deployment after pushing
   the corrected `requirements.txt`.

The existing `vercel.json` sends incoming paths to the Flask app. If the
deployed URL still shows Vercel's 404 page, check the deployment's build and
runtime logs, confirm the project root contains `vercel.json`, and make sure
you are opening the URL for the latest successful deployment.

The app currently uses SQLite. Vercel's function filesystem is temporary, so
expenses stored in the deployed app are not reliable across deployments or
function instances. Use a hosted database for persistent production data.

## 👨‍💻 Author

**Sumit Yadav**

B.Tech Data Science Student

GitHub: [sy9070002-git](https://github.com/sy9070002-git)

## 📄 License

This project is intended for learning and educational purposes. An open-source license can be added when the project is ready for public distribution.

---

⭐ If you find this project useful, consider giving the repository a star!
