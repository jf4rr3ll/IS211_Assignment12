#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Assignment 12 Module"""

import sqlite3
from flask import Flask, request, session, g, redirect, url_for, render_template, flash


DATABASE = 'hw12.db'
DEBUG = True
SECRET_KEY = "key"
USERNAME = "admin"
PASSWORD = "p@ssw0rd"

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != USERNAME:
            error = 'The system does not recognize that username.'
            return render_template('login.html', error=error)
        elif request.form['password'] != PASSWORD:
            error = 'The password is incorrect; please try again.'
            return render_template('login.html', error=error)
        else:
            session['logged_in'] = True
            return redirect('/dashboard')
    else:
        return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out')
    return redirect(url_for('/login'))


@app.route('/dashboard', methods = ['GET'])
def dashboard():
    if session['logged_in'] != True:
        return redirect('/login')
    else:
        cur = g.db.execute('select StudentID, StudentFirstName, StudentLastName from students')
        students = [dict(StudentID = row[0], StudentFirstName = row[1], StudentLastName = row[2])
                    for row in cur.fetchall()]
        cur = g.db.execute('select QuizID, QuizSubject, QuizQuestions, QuizDate from quizzes')
        quizzes = [dict(QuizID = row[0], QuizSubject = row[1], QuizQuestions = row[2], QuizDate = row[3])
                   for row in cur.fetchall()]
        return render_template("dashboard.html", students = students, quizzes = quizzes)


@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif request.method == 'GET':
        return render_template('studentadd.html')
    elif request.method == 'POST':
        g.db.execute('insert into students (StudentFirstName, StudentLastName) values (?, ?)',
                     [request.form['StudentFirstName'], request.form['StudentLastName']])
        g.db.commit()
    return redirect(url_for('dashboard'))


@app.route('/quiz/add', methods=['GET', 'POST'])
def add_quiz():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif request.method == 'GET':
        return render_template('quizadd.html')
    elif request.method == 'POST':
        g.db.execute('insert into quizzes (QuizSubject, QuizQuestions, QuizDate) '
                     'values (?, ?, ?)', [request.form['QuizSubject'],
                                          request.form['QuizQuestions'],
                                          request.form['QuizDate']])
        g.db.commit()
    return redirect(url_for('dashboard'))


@app.route('/results/add', methods=['GET', 'POST'])
def add_result():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif request.method == 'GET':
        return render_template('resultsadd.html')
    elif request.method == 'POST':
        g.db.execute("insert into RESULTS (StudentID, QuizID, Score) values "
                     "(?, ?, ?)", (request.form['StudentID'], request.form['QuizID'], request.form['Score']))
        g.db.commit()
    return redirect('/dashboard')


if __name__ == '__main__':
    app.run()