import json
from flask import Flask, render_template, request

app = Flask(__name__)

def load_questions():
    with open('questions.json', 'r', encoding='utf-8') as file:
        questions = json.load(file)
    return questions

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    questions = load_questions()
    if request.method == 'POST':
        answers = request.form
        correct_answers = 0
        for i, question in enumerate(questions):
            selected_answer = answers.get(f'question{i+1}')
            if selected_answer == question['answer']:
                correct_answers += 1

        return f"Вы ответили правильно на {correct_answers} из {len(questions)} вопросов."

    return render_template('quiz.html', questions=questions)

if __name__ == '__main__':
    app.run(debug=True)
