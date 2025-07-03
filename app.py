from flask import Flask, render_template, request, redirect, url_for, session
import json, random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load all questions from JSON
with open('questions.json') as f:
    ALL_QUESTIONS = json.load(f)


@app.route('/')
def home():
    selected = random.sample(ALL_QUESTIONS, 10)
    session['questions'] = selected
    session['current'] = 0
    session['answers'] = {}  # Use dict to avoid index errors
    return redirect(url_for('question'))


@app.route('/question', methods=['GET', 'POST'])
def question():
    questions = session.get('questions', [])
    current = session.get('current', 0)
    total = len(questions)

    if request.method == 'POST':
        action = request.form.get('action')
        selected = request.form.getlist('answer')

        # Save answer
        answers = session.get('answers', {})
        answers[str(current)] = selected
        session['answers'] = answers

        if action == 'next':
            current += 1
        elif action == 'submit':
            # Final question answered
            session['current'] = current
            return redirect(url_for('result'))

        session['current'] = current
        return redirect(url_for('question'))

    # Render question
    if current >= total:
        return redirect(url_for('result'))

    return render_template('question.html',
                           question=questions[current],
                           index=current + 1,
                           total=total)

@app.route('/result', methods=['GET', 'POST'])
def result():
    answers = session.get('answers', {})
    questions = session.get('questions', [])

    # Optional score logic
    score = 0
    for i, q in enumerate(questions):
        correct = q.get('answer', [])
        user_answer = answers.get(str(i), [])
        if isinstance(correct, str):
            correct = [correct]
        if set(user_answer) == set(correct):
            score += 1

    return render_template('result.html',
                           answers=answers,
                           questions=questions,
                           total=len(questions),
                           score=score)





if __name__ == '__main__':
    app.run(debug=True)
