from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func, select
import os
import json
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
@app.route('/')
def home():
    posts = blogpost.query.filter_by().all()
    return render_template('index.html',posts=posts)

if __name__=='__main__':
    app.run()
