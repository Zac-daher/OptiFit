from flask import Flask, render_template, request
import requests
import os
import sqlite3
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
load_dotenv(dotenv_path=".env")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(" API key not loaded...")

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    workout = None

    default_data = {
        "hrv": "52",
        "battery": "41",
        "stress": "67",
        "sleep": "6.2",
        "goal": "Build endurance and maintain recovery",
        "equipment": "Dumbbells, treadmill"
    }

    if request.method == 'POST':
        hrv = request.form['hrv']
        battery = request.form['battery']
        stress = request.form['stress']
        sleep = request.form['sleep']
        goal = request.form['goal']
        equipment = request.form['equipment']

        prompt = f"""
        My HRV is {hrv}, body battery is {battery}, stress is {stress}, and sleep is {sleep} hours.
        My goal is {goal}.
        I have access to {equipment}.
        Generate a safe, effective workout plan for today with warm-up and cooldown.
        """

        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,
            "max_tokens": 500
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            workout = response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            workout = f"Error: {e}"

        default_data.update({
            "hrv": hrv,
            "battery": battery,
            "stress": stress,
            "sleep": sleep,
            "goal": goal,
            "equipment": equipment
        })

    return render_template('index.html', workout=workout, defaults=default_data)

@app.route('/data')
def data():
    conn = sqlite3.connect("fitness.db")
    c = conn.cursor()
    rows = c.execute("SELECT * FROM workouts ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("data.html", rows=rows)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
