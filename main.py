from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func, select
from datetime import datetime
from werkzeug import secure_filename
from flask_mail import Mail
import json
import os
app=Flask(__name__)
db = SQLAlchemy(app)


app.config['SQLALCHEMY_DATABASE_URI'] ="postgres://pwmrktgonjcssv:4b833fdabf64cbae502cb725eb6b3a7dfe0e75fd2fc15bf1b330e92d2b52dce3@ec2-54-247-169-129.eu-west-1.compute.amazonaws.com:5432/do6ekqf6agn0p"
class blogpost(db.Model):

    srno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content0 = db.Column(db.String(150), nullable=False)
    content1 = db.Column(db.String(150), nullable=False)
    content2= db.Column(db.String(150), nullable=False)
    content3 = db.Column(db.String(150), nullable=False)
    content4 = db.Column(db.String(150), nullable=False)
    content5= db.Column(db.String(150), nullable=False)
    content6 = db.Column(db.String(150), nullable=False)
    content7 = db.Column(db.String(150), nullable=False)
    content8 = db.Column(db.String(150), nullable=False)
    content9 = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(15), nullable=False)
    like = db.Column(db.Integer, nullable=True)

    date = db.Column(db.String(12), nullable=True)
 
class review1(db.Model):

    srno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    message = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(15), nullable=False)
    date = db.Column(db.String(12), nullable=True)
 class contact(db.Model):

    srno = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    message = db.Column(db.String(400), nullable=False)
    subject = db.Column(db.String(205), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    
@app.route('/')
def home():
    posts = blogpost.query.filter_by().all()
    return render_template('index.html',posts=posts)

@app.route('/about')
def about():
    reviews = review1.query.order_by(func.random()).all()
    return render_template('about.html', reviews=reviews)

@app.route('/review/<string:srno>', methods=['GET'])
def review_viewer(srno):

    reviews = review1.query.filter_by(srno=srno).first()
    return render_template('review_viewer.html', reviews=reviews)

@app.route('/submit', methods=['POST', 'GET'])
def feedback_form():

    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')
    entry = review1(name=name, email=email, subject=subject,
                    message=message, date=datetime.now())
    db.session.add(entry)
    db.session.commit()
    return redirect(url_for('about'))
@app.route('/contact', methods=['GET', 'POST'])
def contact1():
    if request.method == 'POST':
        username = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        entry = contact(username=username, email=email,
                        subject=subject, message=message, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from ' + username,
                          sender=email,
                          recipients=["fighter7415963@gmail.com"],
                          body="subject:" + subject + "\n" + "message:" + message
                          )

    return render_template('contact.html')
if __name__=='__main__':
    app.run()
