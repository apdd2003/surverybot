from flask import Flask, render_template, request, redirect, url_for
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

# Create a new instance of a ChatBot
# bot = ChatBot('SurveyBot')

# Train the bot with the survey questions
# trainer = ListTrainer(bot)

app = Flask(__name__)

# Your SurveyBot logic here
questions = [
    "Have you ever drank alcohol regularly?",
    "Do you still drink alcohol, ever, at all?",
    "Have you taken any controlled substances either in the last six months or for a long period in the past?",
    "What medications do you take?",
    "Other than for the surgeries or procedures you have entered, have you ever been admitted to a hospital?",
    "For what reason were you admitted to the hospital?",
    "Have you ever had cancer?"
]
# trainer.train(questions)

class SurveyBot:
    def __init__(self, questions, skip_logic=None):
        self.questions = questions
        self.current_question_index = 0
        self.responses = []
        self.skip_logic = skip_logic or {}

    def get_next_question(self):
        while self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]
            self.current_question_index += 1

            # Check if the question should be skipped based on skip logic
            if question in self.skip_logic:
                skip_condition, skip_question = self.skip_logic[question]
                if skip_condition(self.responses):
                    continue
                else:
                    return skip_question
            
            return question
        else:
            return None

    def record_response(self, response):
        self.responses.append(response)

# Define skip logic
def skip_alcohol_questions(responses):
    # Skip alcohol-related questions if the user has never drank alcohol regularly
    print(responses)
    return "No" in responses[:2]

def skip_hosp_questions(responses):
    # Skip alcohol-related questions if the user has never drank alcohol regularly
    print(responses[-1:])
    return "Yes" in responses[-1:]

skip_logic = {
    "Do you still drink alcohol, ever, at all?": (skip_alcohol_questions, "What medications do you take?"),
    "What medications do you take?": (lambda x: False, "Other than for the surgeries or procedures you have entered, have you ever been admitted to a hospital?"),
    "For what reason were you admitted to the hospital?":(skip_hosp_questions, "What medications do you take?"), 
}

# Create SurveyBot instance with skip logic
survey_bot = SurveyBot(questions, skip_logic)

# survey_bot = SurveyBot(questions)

# Flask routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        response = request.form['response']
        survey_bot.record_response(response)
        return redirect(url_for('index'))

    question = survey_bot.get_next_question()
    if question:
        return render_template('index.html', question=question)
    else:
        return render_template('survey_completed.html', responses=survey_bot.responses)

if __name__ == '__main__':
    app.run(debug=True)
