# 🤖 AI-Based Smart Task Scheduler

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-lightgrey.svg)
![Gemini AI](https://img.shields.io/badge/AI-Google%20Gemini-orange.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-green.svg)

## 📌 Overview
**AI-Based Smart Task Scheduler** is an intelligent web application designed to help users effectively manage their time and tasks. Instead of just maintaining a traditional to-do list, this application integrates with **Google Gemini AI** to automatically evaluate the urgency of each task and assign a dynamic priority score (1-10). It also provides daily AI-driven recommendations and productivity tips to keep users focused.

This project was built with a focus on clean architecture, secure user authentication, and seamless AI integration.
## System Diagram
<img width="1280" height="853" alt="Image" src="https://github.com/user-attachments/assets/a1094790-f1fd-477b-88b4-d9f5c8eaa1eb" /> 

## ✨ Key Features
- **Secure Authentication:** User registration and login system with password hashing (Werkzeug).
- **AI Priority Scoring:** Automatically calculates task urgency based on deadlines, estimated duration, and categories using Gemini AI.
- **Smart Daily Recommendations:** AI analyzes all pending tasks to recommend the most critical focus of the day along with a tailored productivity tip.
- **Interactive Dashboard:** Real-time analytics and task distribution visualized using Chart.js.
- **CRUD Operations:** Easily create, read, update (mark as done), and delete tasks.
- **Multi-User Support:** Each user has an isolated environment for their personal tasks.

## 🛠️ Tech Stack
- **Backend:** Python, Flask, SQLite3
- **AI Integration:** Google Gemini API (gemini-3.5-flash)
- **Frontend:** HTML5, Bootstrap 5, Vanilla JavaScript, Chart.js
- **Security:** Session Management, Werkzeug Password Hashing, Environment Variables (Dotenv)

## 🚀 Installation & Setup

To run this project locally on your machine, follow these steps:


```bash
1. Clone the repository
git clone [https://github.com/yourusername/Smart-Task-Scheduler.git](https://github.com/yourusername/Smart-Task-Scheduler.git)
cd Smart-Task-Scheduler

2. Create a Virtual Environment
python -m venv myenv
source myenv/Scripts/activate  # For Windows
# source myenv/bin/activate    # For Mac/Linux

3. Install Dependencies
pip install flask python-dotenv requests google-generativeai werkzeug

4.  Setup Environment Variables
GEMINI_API_KEY=your_actual_api_key_here

5.  Initialize Database & Run the App
python app.py
The application will automatically generate the database.db file with the required tables.
Open your browser and navigate to: http://127.0.0.1:5000.

💡 How It Works (AI Logic)
1. Task Submission: When a user adds a task, the details (title, deadline, duration) are sent to the backend.

2. AI Evaluation: A customized prompt alongside the task details is sent to the Gemini API. The AI uses a strict scoring rubric to return a JSON response containing a priority score (1-10).

3. Data Visualization: The frontend fetches the sorted data and categorizes them into High, Medium, and Low priorities dynamically rendering them into a Doughnut chart.

👨‍💻 Author
[WUT YEE HTET]

GitHub: [https://github.com/wutyeehtet/Smart-_-Task_Scheduler]
```
### AI Task Scheduler
<img width="903" height="762" alt="Image" src="https://github.com/user-attachments/assets/f03dbf83-aeb5-4911-89c4-97fbf4a1802b" />
