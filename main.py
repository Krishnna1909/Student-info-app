from flask import Flask, request, render_template
import pandas as pd
from datetime import date

app = Flask(__name__)

# Load and clean data
df = pd.read_excel('students.xlsx', skiprows=1, usecols="C,D,E,F,G")
df.columns = ['Roll No', 'Name', 'Gender', 'Age', 'Birthday']
df['Roll No'] = df['Roll No'].astype(str).str.strip().str.replace("'", "")
df['Birthday'] = pd.to_datetime(df['Birthday'], errors='coerce')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_birthday', methods=['POST'])
def get_birthday():
    roll_no = str(request.form['roll_no']).strip().split('.')[0]
    student = df[df['Roll No'] == roll_no]

    if not student.empty:
        name = student.iloc[0]['Name']
        gender = student.iloc[0]['Gender']
        birthday_val = student.iloc[0]['Birthday']

        # Calculate age dynamically
        if pd.isna(birthday_val):
            birthday = "Not Available"
            age = "Not Available"
        else:
            birthday = birthday_val.strftime("%d %B %Y")
            today = date.today()
            age = today.year - birthday_val.year - ((today.month, today.day) < (birthday_val.month, birthday_val.day))

        return render_template('index.html', name=name, gender=gender, age=age, birthday=birthday, roll_no=roll_no)
    else:
        return render_template('index.html', error="Roll number not found.")

if __name__ == '__main__':
    app.run(debug=True)
