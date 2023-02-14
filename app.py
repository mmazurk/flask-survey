from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "wow-a-secret"
debug = DebugToolbarExtension(app)

response = []
questions = [0]

@app.route("/")
def survey_start():
    """home page with survey instructions"""
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    
    return render_template("home.html", title = title, instructions = instructions)

@app.route("/questions/<int:number>", methods=['POST', 'GET'])
def show_question(number):
    """shows each of the survey questions"""

    # if done, always redirect to thank you
    if questions[-1] == len(satisfaction_survey.questions):
        flash("Tsk Tsk, don't try to redo questions.")
        return redirect("/thankyou")
    
    # if not done, redirect to appropriate question
    if number != questions[-1] & questions[-1] < len(satisfaction_survey.questions):
        flash("Tsk tsk, don't try to skip ahead.")
        return redirect(f"/questions/{questions[-1]}")

    current_question = satisfaction_survey.questions[number].question
    current_choices = satisfaction_survey.questions[number].choices
    current_allow_text = satisfaction_survey.questions[number].allow_text

    return render_template("questions.html", question = current_question, 
    choices = current_choices, allow_text = current_allow_text, title = satisfaction_survey.title) 

@app.route("/answer", methods=['POST', 'GET'])
def record_answer():
    """records survey answer in response list"""
    question_text = request.form['question']
    append_list = []
    question_number = 0

    for index, val in enumerate(satisfaction_survey.questions):
        if val.question == question_text:
            question_number = index
            break

    next_question = question_number + 1
       
    append_list.append(request.form['choices'])
    append_list.append(request.form['question'])
    append_list.append(request.form[question_text])  
    response.append(append_list)
    questions.append(next_question)  
        
    if next_question == len(satisfaction_survey.questions):
        return redirect("/thankyou")
    # for debugging - return render_template("answer.html")
    else:
        return redirect(f"/questions/{next_question}")

@app.route("/thankyou")
def thank_you():
    """thank you page"""
    return render_template("thankyou.html", responses = response)