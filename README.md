# AI Student Performance Monitoring System (Flask + MySQL + ML)

This is a Flask-based academic performance system that tracks student marks, analyzes weak subjects, predicts performance trends using Machine Learning, and generates visual reports. It helps identify at-risk students early instead of relying on simple class averages.

The system combines backend development, database management, and basic AI/ML prediction using Linear Regression.

---

## Features

- Admin authentication (login/register/logout)
- Add, update, delete student marks
- Term-based student management system
- Subject risk detection (weak subjects below 50%)
- Total marks calculation per student
- AI prediction of declining subjects using Linear Regression
- Student ranking system
- Data visualization using Plotly graphs
- MySQL database integration

---

## Tech Stack

Python (Flask), MySQL, NumPy, Scikit-learn, Plotly, HTML, CSS, Jinja2 templates

---

## Project Structure

- app.py → Main Flask application (routes & logic)
- utils.py → ML logic (risk detection, prediction, scoring)
- config.py → Database configuration
- templates/ → HTML pages (login, dashboard, students, ranking, predictions)
- static/ → CSS and images

---

## Setup Instructions

1. Clone the repository  
2. Install dependencies:
   pip install flask mysql-connector-python numpy scikit-learn plotly  

3. Configure database in config.py  
4. Create MySQL tables (term1, term2, term3, admins)  
5. Run the application:
   python app.py  

6. Open browser:
   http://localhost:5000  

---

## Default Admin Login

Username: lavingston  
Password: admin123  

---

## System Modules

- Login System → Secure admin authentication  
- Add Marks → Input student performance per term  
- Students Module → View and manage student records  
- AI Predictions → Detect weak performance trends  
- Ranking → Sort students by total marks  
- Update Module → Edit marks  
- Delete Module → Remove student records  

---

## AI / ML Logic

- Subjects analyzed: Math, English, Kiswahili, Science, Social  
- Weak subject detection: marks < 50  
- Total score calculation per student  
- Linear Regression predicts future performance trends  
- Identifies declining subjects per student  

---

## Endpoints

/ → Login  
/register → Register admin  
/dashboard → Main dashboard  
/add → Add student marks  
/students?term=1 → View students per term  
/update/<term>/<id> → Update marks  
/delete/<term>/<id> → Delete student  
/predictions → AI analysis + graphs  
/ranking → Student ranking system  
/logout → Logout  

---

## Author

Lovingstone Ochieng Peter  
GitHub: https://github.com/lovingstonepeter  
Email: lovingstonepeter@gmail.com  
Phone: 0712458284  

---

## License

This project is for academic and portfolio purposes.
