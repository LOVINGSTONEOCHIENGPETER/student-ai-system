from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector
from config import DB_CONFIG, SECRET_KEY
from utils import subject_risk, total_marks, ml_predict_trend

import plotly
import plotly.graph_objs as go
import json

app = Flask(__name__)
app.secret_key = SECRET_KEY


def get_db():
    return mysql.connector.connect(**DB_CONFIG)


# ================= LOGIN =================
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']

        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM admins WHERE username=%s AND password=%s", (u, p))
        user = cur.fetchone()

        if user:
            session['admin'] = u
            flash("Login successful", "success")
            return redirect('/dashboard')
        else:
            flash("Wrong credentials", "danger")

    return render_template('login.html')


# ================= REGISTER =================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']

        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO admins(username,password) VALUES(%s,%s)", (u, p))
        db.commit()

        flash("Registered successfully", "success")
        return redirect('/')

    return render_template('register.html')


# ================= LOGOUT =================
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/')


# ================= DASHBOARD =================
@app.route('/dashboard')
def dashboard():
    if 'admin' not in session:
        return redirect('/')
    return render_template('dashboard.html')


# ================= ADD =================
@app.route('/add', methods=['GET', 'POST'])
def add():
    if 'admin' not in session:
        return redirect('/')

    if request.method == 'POST':
        regno = request.form['regno']
        name = request.form['name']
        term = request.form['term']

        # 🔥 BACKEND VALIDATION
        try:
            math = int(request.form['math'])
            english = int(request.form['english'])
            kiswahili = int(request.form['kiswahili'])
            science = int(request.form['science'])
            social = int(request.form['social'])

            for m in [math, english, kiswahili, science, social]:
                if m < 0 or m > 100:
                    flash("Marks must be between 0 and 100", "danger")
                    return redirect('/add')

        except:
            flash("Invalid input. Enter numbers only.", "danger")
            return redirect('/add')

        table = f"term{term}"

        db = get_db()
        cur = db.cursor()

        try:
            cur.execute(f"""
            INSERT INTO {table}(regno,name,math,english,kiswahili,science,social)
            VALUES(%s,%s,%s,%s,%s,%s,%s)
            """, (regno, name, math, english, kiswahili, science, social))
            db.commit()

        except mysql.connector.errors.IntegrityError:
            flash(f"RegNo {regno} already exists in Term {term}", "danger")
            return redirect('/add')

        # AI analysis
        cur.execute(f"SELECT * FROM {table} WHERE regno=%s", (regno,))
        record = cur.fetchone()

        risks = subject_risk(record)
        total = total_marks(record)

        if risks:
            flash(f"{name} weak in {', '.join(risks)}", "warning")

        if total < 350:
            flash(f"{name} scored {total}", "danger")

        flash("Marks added successfully", "success")
        return redirect(f"/students?term={term}")

    return render_template('add_marks.html')


# ================= VIEW =================
@app.route('/students')
def students():
    if 'admin' not in session:
        return redirect('/')

    term = request.args.get('term', '1')
    table = f"term{term}"

    db = get_db()
    cur = db.cursor()
    cur.execute(f"SELECT * FROM {table}")
    data = cur.fetchall()

    return render_template('students.html', students=data, term=term)


# ================= UPDATE =================
@app.route('/update/<term>/<int:id>', methods=['GET', 'POST'])
def update(term, id):
    db = get_db()
    cur = db.cursor()

    if request.method == 'POST':
        try:
            math = int(request.form['math'])
            english = int(request.form['english'])
            kiswahili = int(request.form['kiswahili'])
            science = int(request.form['science'])
            social = int(request.form['social'])

            for m in [math, english, kiswahili, science, social]:
                if m < 0 or m > 100:
                    flash("Marks must be between 0 and 100", "danger")
                    return redirect(f"/update/{term}/{id}")

        except:
            flash("Invalid input", "danger")
            return redirect(f"/update/{term}/{id}")

        cur.execute(f"""
        UPDATE term{term}
        SET math=%s, english=%s, kiswahili=%s, science=%s, social=%s
        WHERE id=%s
        """, (math, english, kiswahili, science, social, id))

        db.commit()
        return redirect(f"/students?term={term}")

    cur.execute(f"SELECT * FROM term{term} WHERE id=%s", (id,))
    student = cur.fetchone()

    return render_template('update_marks.html', student=student, term=term)


# ================= DELETE =================
@app.route('/delete/<term>/<int:id>')
def delete(term, id):
    db = get_db()
    cur = db.cursor()
    cur.execute(f"DELETE FROM term{term} WHERE id=%s", (id,))
    db.commit()
    return redirect(f"/students?term={term}")


# ================= PREDICTIONS + GRAPH =================
@app.route('/predictions')
def predictions():
    if 'admin' not in session:
        return redirect('/')

    term = request.args.get('term', '1')
    table = f"term{term}"

    db = get_db()
    cur = db.cursor()
    cur.execute(f"SELECT * FROM {table}")
    data = cur.fetchall()

    results = []

    # Graph data
    names = []
    totals = []

    for r in data:
        name = r[2]
        total = sum(r[3:8])

        names.append(name)
        totals.append(total)

        if total < 350:
            results.append((f"{name} low performance", "Needs improvement"))

    # Plotly graph
    fig = go.Figure([go.Bar(x=names, y=totals)])
    fig.update_layout(title="Student Performance", xaxis_title="Students", yaxis_title="Total Marks")

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("predictions.html", results=results, term=term, graphJSON=graphJSON)


# ================= RANKING =================
@app.route('/ranking')
def ranking():
    term = request.args.get('term', '1')
    table = f"term{term}"

    db = get_db()
    cur = db.cursor()
    cur.execute(f"SELECT * FROM {table}")
    data = cur.fetchall()

    ranked = []
    for row in data:
        total = total_marks(row)
        ranked.append((row, total))

    ranked.sort(key=lambda x: x[1], reverse=True)

    final = []
    pos = 1
    for r in ranked:
        final.append((pos, r[0], r[1]))
        pos += 1

    return render_template('ranking.html', ranking=final, term=term)


if __name__ == '__main__':
    app.run(debug=True)