from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

students = ["Alice", "Bob", "Charlie"]

app = Flask(__name__)
app.secret_key = "dev"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        date = datetime.now().strftime("%Y-%m-%d")
        with open('attendance.txt', 'a', encoding='utf-8') as f:
            f.write(f"\n--- {date} ---\n")
            for s in students:
                status = request.form.get(s, 'A')
                record = 'Present' if status == 'P' else 'Absent'
                f.write(f"{s}: {record}\n")

        flash('✅ Attendance recorded!')
        return redirect(url_for('index'))

    return render_template('index.html', students=students)


@app.route('/records')
def records():
    try:
        with open('attendance.txt', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        content = 'No attendance records found.'
    return render_template('records.html', content=content)


if __name__ == '__main__':
    app.run(debug=True)
