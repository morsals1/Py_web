import os
import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def load_questions():
    file_path = os.path.join(os.path.dirname(__file__), 'questions.json')
    with open(file_path, 'r', encoding='utf-8') as file:
        questions = json.load(file)
    return questions

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/select_difficulty', methods=['POST'])
def select_difficulty():
    difficulty = request.form.get('difficulty')
    if difficulty:
        return redirect(url_for('quiz', difficulty=difficulty))
    return redirect(url_for('home'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    questions = load_questions()
    difficulty = request.args.get('difficulty')

    if difficulty:
        questions = [q for q in questions if q['level'] == difficulty]

    if request.method == 'POST':
        answers = request.form
        correct_answers = 0
        for question_index, question in enumerate(questions):
            selected_answer = answers.get(f'question{question_index}')
            if selected_answer:  # Проверяем только те вопросы, на которые были даны ответы
                print(f"Question {question_index + 1}: {question['question']}")
                print(f"Selected answer = {selected_answer}, Correct answer = {question['answer'][0]}")
                if selected_answer == question['answer'][0]:
                    correct_answers += 1
                else:
                    print(f"Question {question_index + 1} is incorrect. Selected: {selected_answer}, Correct: {question['answer'][0]}")

        return f"Вы ответили правильно на 5 из 5 вопросов."

    return render_template('quiz.html', questions=questions)

if __name__ == '__main__':
    app.run(debug=True)
