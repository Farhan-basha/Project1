from flask import Flask, render_template, request, jsonify
import openai
import random
import matplotlib.pyplot as plt
import os

# OpenAI API Key (replace with your own)
openai.api_key = "your_openai_api_key"

app = Flask(__name__)

# Simulated real-time monitoring data
stress_levels = []
mood_scores = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_input = request.form['message']
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a mental health assistant."},
            {"role": "user", "content": user_input}
        ]
    )
    reply = response['choices'][0]['message']['content']
    return jsonify({"reply": reply})

@app.route('/submit_mood', methods=['POST'])
def submit_mood():
    stress = int(request.form['stress'])
    mood = int(request.form['mood'])
    stress_levels.append(stress)
    mood_scores.append(mood)
    return jsonify({"message": "Data submitted successfully!"})

@app.route('/dashboard')
def dashboard():
    # Generate a simple chart
    if not stress_levels or not mood_scores:
        return "No data available yet."
    
    plt.figure(figsize=(10, 5))
    plt.plot(stress_levels, label='Stress Levels', marker='o')
    plt.plot(mood_scores, label='Mood Scores', marker='x')
    plt.title('Workplace Mental Health Trends')
    plt.xlabel('Entries')
    plt.ylabel('Scores')
    plt.legend()
    chart_path = os.path.join('static', 'chart.png')
    plt.savefig(chart_path)
    plt.close()
    return render_template('dashboard.html', chart_path=chart_path)

if __name__ == '__main__':
    app.run(debug=True)
