# Validate
📊 CSV Data Cleaner (Flask Web App)
This is a simple Flask-based web application that allows users to upload a .csv file, automatically cleans the data, and returns a downloadable cleaned version along with a summary report.

🚀 Features
✅ Drop rows with null values
✅ Drop duplicate rows (exact duplicates)
✅ Drop rows with duplicate keys (like clientid) — configurable
✅ Standardize column names (lowercase, underscores)
✅ Remove rows with invalid JSON (from JSON-like fields)
✅ Provide a cleaning report (rows removed, JSON errors, etc.)
✅ Download the cleaned CSV
✅ Frontend built with basic HTML/CSS & fetch API

🏗️ Tech Stack
Backend: Python, Flask

Frontend: HTML, CSS, JavaScript (Vanilla)

Libraries: Pandas, JSON, io

📦 Setup Instructions
1. Clone the Repo
bash
Copy
Edit
git clone https://github.com/shaivalya/csv-cleaner-app.git
cd csv-cleaner-app
2. Install Dependencies
Make sure you have Python 3.x installed.

bash
Copy
Edit
pip install flask pandas
3. Run the App
bash
Copy
Edit
python app.py
Visit http://127.0.0.1:5000 in your browser.

📁 Project Structure
bash
Copy
Edit
├── app.py                  # Flask backend
├── templates/
│   └── upload.html         # Frontend HTML form
└── README.md
