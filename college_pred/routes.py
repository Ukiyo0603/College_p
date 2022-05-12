from crypt import methods
from flask import render_template, flash, redirect, url_for, request
from openpyxl import load_workbook
from college_pred.forms import RegistrationForm, LoginForm, InputDataForm
from college_pred.models import User, Post
from college_pred import app, db, login_manager, bcrypt
from flask_bcrypt import Bcrypt
from flask_login import current_user, login_user, logout_user

#Imports for result model 
import pandas as pd
import numpy as np
import seaborn as sns
from sqlalchemy import false

data = pd.read_csv('/Users/shivanimakde/PBLproject/College-Predictor/A_PBL_DATA_CLG.csv')

@app.route("/") 
@app.route("/home")
def home():
    return render_template('layouts.html')

@app.route("/about", methods = ['GET'])
def about():
    return render_template('about.html')

@app.route("/feature")
def feature():
    return render_template('feature.html')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/login", methods = ['POST', 'GET'])
def login():
    # if current_user.is_authenticated():
    #     return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember= form.remember.data)
            flash('You have been logged In!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful!', 'danger')
    return render_template('login.html', title = 'Log In', form = form)

@app.route("/signup", methods = ['POST','GET'])
def signup(): 
    # if current_user.is_authenticated:
    #     return(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account have now been created!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title = 'Sign Up', form= form)

@app.route("/mainpage", methods = ['POST', 'GET'])
def mainpage():
    form = InputDataForm()
    if form.validate_on_submit():
        return redirect(url_for('home'))
    return render_template('mainpage.html', title = 'Mainpage', form = form)

@app.route("/result", methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        output = request.form.to_dict()

        user_percent = float(output["percentile"])
        user_category = float(output["category"])
        user_branch = float(output["branch"])


        #CONVERT TO LIST
        marks = data['MeritScore'].tolist()
        Cllg = data['CollegeName'].tolist()
        Branch = data['CourseName'].tolist()
        Category = data['SeatTypeCode'].tolist()

        output = []
        output1 = []
        finaloutput = []
        finalCllg = []
        finalMarks = []

        def selected(user_percent, user_category, user_branch):
            # To filter the College in which the user can get admission according to his percent
            for i in range(18630):
                if marks[i] <= user_percent:
                    output.append(i)
            
            #To filter the College in which the user can get admission according to his percent, Category
            for i in range(len(output)):
                if Category[output[i]] == user_category:
                    output1.append(output[i])
            
            #To filter the College in which the user can get admission according to his percent, category and Branch

            for i in range(len(output1)):
                if Branch[output1[i]] == user_branch:
                    finaloutput.append(output1[i])

        selected(user_percent, user_category, user_branch)

        for j in finaloutput:
            finalCllg.append(Cllg[j])
            finalMarks.append(marks[j])

        df = pd.DataFrame({"College Name": finalCllg, "CutOff":finalMarks })
        
        df.to_excel('predicted.xlsx', sheet_name='Sheet1', index=false)

        df_html = df.to_html()

        return render_template("submit.html", data = df_html)
    return render_template("mainpage.html")

@app.route("/submit", methods = ['POST'])
def submit():
    if request.method == 'POST':
        s = request.form()
        return redirect(url_for('result', form = s))
    else:
        redirect(url_for('mainpage'))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
