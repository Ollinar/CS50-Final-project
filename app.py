from crypt import methods
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
import re
from extra import login_required


# Configure application
app = Flask(__name__)


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure CS50 Library to use SQLite database
users_db = SQL("sqlite:///users.db")
quiz_db = SQL("sqlite:///quiz.db")


@app.route("/")
def index():
    if session.get("user_id") is None:
        return render_template("welcome.html")
    else:
        return render_template("index.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    """Logs user in"""
    # if the request comes from form
    if request.method == 'POST':
        # makes sure the inputs are not empty
        if not request.form.get("username") or not request.form.get("password"):
            flash("Invalid input")
            return redirect('/login')
        # validates the passed credantials
        cred = users_db.execute('SELECT * FROM users WHERE username = ?',
                                request.form.get("username"))
        if len(cred) != 1 or not check_password_hash(cred[0]['hash'], request.form.get("password")):
            flash("Wrong username or password")
            return redirect('/login')
        # if everythin is valid, remembers the user with session
        session['user_id'] = cred[0]['id']
        return redirect("/")
    # if request comes from visiting the page
    else:
        return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registers a user"""
    # handles the submition of the form
    if request.method == 'POST':
        # makes sure all fileds are filled up
        if not request.form.get('username') or not request.form.get('password') or not request.form.get('confirm'):
            flash('Please Fill up all the fields')
            return redirect('/register')
        username = request.form.get('username')
        password = request.form.get('password')

        # validates the username making sure its not taken yet
        if len(users_db.execute('SELECT username FROM users WHERE username = ?', username)) != 0:
            flash('Username is already taken')
            return redirect('/register')

        # validates the password. must have a number, capital, lower and 8 long
        if len(password) < 8:
            flash("Invalid password, must be at least 8 characher long")
            return redirect('/register')
        elif re.search("[a-z]", password) is None:
            flash("Password needs to have atleast 1 lowercase letter")
            return redirect('/register')
        elif re.search("[A-Z]", password) is None:
            flash("Password needs to have atleast 1 uppercase letter")
            return redirect('/register')
        elif re.search("[0-9]", password) is None:
            flash("Password must have atleast 1 number")
            return redirect('/register')

         # validates the confirm password
        if password != request.form.get('confirm'):
            flash("Password and Confirm password doesn't match")
            return redirect('/register')

         # if everything chacks out, generate a hash for the password then add it to database
        passhash = generate_password_hash(password)
        users_db.execute('INSERT INTO users (username, hash) VALUES(?,?)',
                         username, passhash)
        session['user_id'] = users_db.execute(
            'SELECT id FROM users WHERE username = ?', username)[0]['id']
        return redirect('/')

    # handles the rendering of the form
    else:
        return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    """Logs the user out"""
    session.clear()
    return redirect('/')


@app.route('/makequiz', methods=['GET', 'POST'])
@login_required
def makequiz():
    """Creating a Quiz"""
    # preocess submit request
    if request.method == 'POST':
        # makes sure theres a quiz name
        if not request.form.get('name'):
            flash('No Quiz Name')
            return redirect('/makequiz')
        # makes sre there is a question
        if not request.form.get('questNum'):
            flash('No question entered!')
            return redirect('/makequiz')

        # goes through all the questions
        numberOfQuestion = int(request.form.get('questNum'))
        for i in range(1, numberOfQuestion + 1):
            # if theres an empty question return error
            if not request.form.get(f'question_{i}'):
                flash(f'Question {i} is empty')
                return redirect('/makequiz')
            # if theres a question that have no answer return an error
            if not request.form.get(f'quest{i}AnswerCount'):
                flash(f"Question number {i} have no answer")
                return redirect('/makequiz')
            # if theres a question with no correct answer return error
            if not request.form.get(f'correctQuest{i}'):
                flash(f'Question number {i} have no correct answer!')
                return redirect('/makequiz')

            # loops through all the answers in each question
            ansNum = int(request.form.get(f'quest{i}AnswerCount'))
            for j in range(1, ansNum + 1):
                # if theres isn empty answer return error
                if not request.form.get(f'ans{i}-{j}'):
                    flash(f"Answer {j} in question {i} is empty!")
                    return redirect('/makequiz')
        # end of validation
        # takes the user's username and make new entry to quizlist
        username = users_db.execute("SELECT username FROM users WHERE id = ?",session["user_id"])[0]['username']
        quiz_db.execute("INSERT INTO quizList (quiz_name, maker_id, maker_username) VALUES(?,?,?)",request.form.get('name') , session["user_id"], username)
        
        # using the quiz id of the newly made entry, make a new table to put the data of the quiz into
        # this query should take the newest entry by the user, whis is this current quiz
        quiz_id = quiz_db.execute("SELECT quiz_id FROM quizList WHERE maker_id = ? ORDER BY timestamp DESC", session['user_id'])[0]['quiz_id']
        quiz_db.execute(f'CREATE TABLE IF NOT EXISTS "quiz/{quiz_id}" ("question_id" INTEGER, "question" TEXT NOT NULL, "correct_answer" TEXT NOT NULL, "answer_1" TEXT, "answer_2" TEXT, "answer_3" TEXT, "answer_4" TEXT, PRIMARY KEY("question_id" AUTOINCREMENT))')
        
        # goes thorugh all the question and add it to the new table
        for i in range(1, numberOfQuestion + 1):
            question = request.form.get(f'question_{i}')
            correct_answer = request.form.get(f'correctQuest{i}')
            quiz_db.execute(f'INSERT INTO "quiz/{quiz_id}" (question, correct_answer) VALUES(?,?)', question, correct_answer)
            
            # adds the answer
            ansNum = int(request.form.get(f'quest{i}AnswerCount'))
            for j in range(1, ansNum + 1):
                answer = request.form.get(f'ans{i}-{j}')
                quiz_db.execute(f'UPDATE "quiz/{quiz_id}" SET answer_{j} = ? WHERE question_id =? ', answer, i)
            
        return redirect('/makequiz')
    else:
        return render_template('makequiz.html')


@app.route('/quizlist', methods=['GET', 'POST'])
@login_required
def quizlist():
    """List down All the Quiz in the database"""
    listOfQuiz = quiz_db.execute('SELECT * FROM quizList')
    return render_template('quiz_list.html', listOfQuiz = listOfQuiz)


@app.route('/takequiz', methods=['GET', 'POST'])
@login_required
def takequiz():
    """page where user takes the quiz"""
    # handles the request from the submition of the quiz
    if request.method =='POST':
        # if somehow the quiz id wasnt able to make it with the submition, return an error and return to quiz list
        if not request.form.get('quizId'):
            flash('no quiz id')
            return redirect('/quizlist')
        
        quiz_id = request.form.get('quizId')
        questCount = quiz_db.execute(f'SELECT COUNT(question_id) AS questCount FROM "quiz/{quiz_id}" ')[0]["questCount"]
        score = 0
        quiz  = quiz_db.execute(f'SELECT * FROM "quiz/{quiz_id}"')
        # goes through all the question
        for i in range(1, questCount + 1):
            # if this question disnt have an answer, will retun an error
            if not request.form.get(f'{i}'):
                flash(f'No answer at Number {i}')
                return redirect('/quizlist')
            # adds 1 to score if the users answer is in the correct answer
            if quiz_db.execute(f"SELECT * FROM 'quiz/{quiz_id}' WHERE question_id = {i} AND correct_answer LIKE ?", "%" + request.form.get(f'{i}') + "%"):
                score += 1
        # shows the user treir score
        return render_template("score.html",score = score, questCount = questCount)
    # handles the request if it comes from the redirect from quizlist
    else:
        # if the link is acceses with out a quiz id, return an error and redirect the user back to quiz list
        if not request.args.get('quiz_id'):
            flash('Error, Invalid Quiz Id')
            return redirect('/quizlist')
        # takes the table from the quiz id, quiz id is used to name the table for each quiz. "quiz/Quiz_id"
        # returns an error and redirect the user if the quiz id is invalid
        try:
            quiz_id = int(request.args.get('quiz_id'))
            quiz_name = quiz_db.execute(f'SELECT quiz_name FROM quizList WHERE quiz_id = ?', quiz_id)[0]["quiz_name"]
            quiz = quiz_db.execute(f'SELECT * FROM "quiz/{quiz_id}"')
        except:
            flash('Error, Invalid Quiz Id')
            return redirect('/quizlist')
        return render_template('takequiz.html', quiz = quiz, quizId = quiz_id, quizName = quiz_name)