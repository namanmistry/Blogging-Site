from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func, select
from datetime import datetime
from werkzeug import secure_filename
from flask_mail import Mail
import json
import os

import math
with open('config.json', 'r') as c:
    params = json.load(c)

app = Flask(__name__)

db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = params['params']['data-base']
app.secret_key = params['params']['secret-key']
app.config['UPLOAD_FOLDER'] = params['params']['file-location']
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['params']['email-username'],
    MAIL_PASSWORD=params['params']['email-password']
)

mail = Mail(app)


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


class popular(db.Model):
    srno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(150), nullable=False)

    slug = db.Column(db.String(15), nullable=False)
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
class seo(db.Model):

  
    sseo0 = db.Column(db.String(20), nullable=False)
    eseo0 = db.Column(db.String(20), nullable=False)
    sseo1 = db.Column(db.String(20), nullable=False)
    eseo1 = db.Column(db.String(20), nullable=False)
    sseo2 = db.Column(db.String(20), nullable=False)
    eseo2 = db.Column(db.String(20), nullable=False)
    sseo3= db.Column(db.String(20), nullable=False)
    eseo3 = db.Column(db.String(20), nullable=False)
    sseo4 = db.Column(db.String(20), nullable=False)
    eseo4 = db.Column(db.String(20), nullable=False)
    sseo5 = db.Column(db.String(20), nullable=False)
    eseo5 = db.Column(db.String(20), nullable=False)
    sseo6 = db.Column(db.String(20), nullable=False)
    eseo6 = db.Column(db.String(20), nullable=False)
    sseo7= db.Column(db.String(20), nullable=False)
    eseo7 = db.Column(db.String(20), nullable=False)
    sseo8 = db.Column(db.String(20), nullable=False)
    eseo8 = db.Column(db.String(20), nullable=False)
    sseo9 = db.Column(db.String(20), nullable=False)
    eseo9 = db.Column(db.String(20), nullable=False)
    srno = db.Column(db.Integer,   primary_key=True, nullable=False)
    


# function section
@app.route('/')
def home():
    posts = blogpost.query.filter_by().all()
    # popularposts = popular.query.filter_by().all()
    
    last = math.ceil(len(posts)/3)
    page = request.args.get('page')
    if not str(page).isnumeric():
        page = 1
    page = int(page)
    posts = posts[(page-1)*3:(page-1)*3+3]
    if page == 1:
        prev1 = "#"
        next1 = "/?page="+str(page+1)

    elif page == last:
        next1 = "#"
        prev1 = "/?page="+str(page-1)
    else:
        next1 = "/?page="+str(page+1)
        prev1 = "/?page="+str(page-1)

    return render_template('index.html', posts=posts, next=next1, prev=prev1)


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


@app.route('/about')
def about():
    reviews = review1.query.order_by(func.rand()).all()
    return render_template('about.html', reviews=reviews)


@app.route('/post/<string:srno>', methods=['GET'])
def post_viewer(srno):
    posts = blogpost.query.filter_by(srno=srno).first()
    seo_tag=seo.query.filter_by(srno=srno).first()
    return render_template('post.html', post=posts,seo_tag=seo_tag)


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
    return redirect('about')


@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    content = blogpost.query.all()
    if 'user' in session and session['user'] == "naman":
        return render_template('dashboard.html', content=content)

    if request.method == "POST":
        user_name = request.form.get('username')
        user_password = request.form.get('pass')

        if user_name == params['params']['login-username'] and user_password == params['params']['login-password']:

            session['user'] = "naman"
            return render_template('dashboard.html', content=content)
        else:
            return render_template('login.html')

    else:
        return render_template('login.html')
    return render_template('login.html')


@app.route('/logout', methods=['POST'])
def logout():

    session['user'] = False
    return redirect('dashboard')


@app.route('/upload', methods=['GET', 'POST'])
def new_post_viewer():
    # last=blogpost.query.filter_by().all()
    # last_post=last[-1]
    return render_template('newpost.html')


@app.route('/upload_post', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        srno = request.form.get('srno')
        title = request.form.get('title')
        slug = request.form.get('slug')
        content0 = request.form.get('content0')
        content1 = request.form.get('content1')
        content2 = request.form.get('content2')
        content3 = request.form.get('content3')
        content4 = request.form.get('content4')
        content5 = request.form.get('content5')
        content6 = request.form.get('content6')
        content7 = request.form.get('content7')
        content8 = request.form.get('content8')
        content9 = request.form.get('content9')
        
        startseo=[]
        endseo=[]
        for i in range(10):
            startseo.append(request.form.get(f'startseotag{i}'))
            endseo.append(request.form.get(f'endseotag{i}'))
        entry_seo=seo(sseo0=startseo[0],
                    eseo0=endseo[0],
                    sseo1=startseo[1],
                    eseo1=endseo[1],
                    sseo2=startseo[2],
                    eseo2=endseo[2],
                    sseo3=startseo[3],
                    eseo3=endseo[3],
                    sseo4=startseo[4],
                    eseo4=endseo[4],
                    sseo5=startseo[5],
                    eseo5=endseo[5],
                    sseo6=startseo[6],
                    eseo6=endseo[6],
                    sseo7=startseo[7],
                    eseo7=endseo[7],
                    sseo8=startseo[8],
                    eseo8=endseo[8],
                    sseo9=startseo[9],
                    eseo9=endseo[9],
                    
                    srno=srno)
        db.session.add(entry_seo)
        db.session.commit()
        new_file=[]
        for i in range(10):
            new_file.append(request.files[f'file{i}'])
            if new_file[i].filename != "":
                new_file[i].save(os.path.join(
                    app.config['UPLOAD_FOLDER'], secure_filename(new_file[i].filename)))
                os.rename(
                f'static\img\\{new_file[i].filename}', f'static\img\\{srno+"."+str(i)}.jpg')

            elif new_file[i].filename=="":
                pass
        entry = blogpost(srno=srno, title=title, content0=content0,
         content1=content1,
          content2=content2,
           content3=content3,
            content4=content4,
             content5=content5,
              content6=content6,
               content7=content7,
                content8=content8,
                 content9=content9,


                         slug=slug,like=0, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('dashboard'))


@app.route('/edit_viewer/<string:srno>', methods=['GET', 'POST'])
def edit_viewer(srno):
    post = blogpost.query.filter_by(srno=srno).first()
    seo_viewer=seo.query.filter_by(srno=srno).first()
   
    return render_template('edit.html',post=post,seo=seo_viewer
    )


@app.route('/edit/<string:srno1>', methods=['GET', 'POST'])
def edit(srno1):
    if request.method == 'POST':
        post = blogpost.query.filter_by(srno=srno1).first()
        
        srno = request.form.get('srno')
        title = request.form.get('title')
        slug = request.form.get('slug')
        content=[]
        for i in range(10):
            content.append(request.form.get(f'content{i}'))
        
        post.content0=content[0]
        post.content1=content[1]
        post.content2=content[2]
        post.content3=content[3]
        post.content4=content[4]
        post.content5=content[5]
        post.content6=content[6]
        post.content7=content[7]
        post.content8=content[8]
        post.content9=content[9]

        post.srno = srno
        post.title = title
        post.slug = slug
        db.session.commit()
        #getting the sseo
        seo_viewer=seo.query.filter_by(srno=srno1).first()
        sseo=[]
        eseo=[]
        for i in range(10):
            sseo.append(request.form.get(f'startseotag{i}'))
        for i in range(10):
            eseo.append(request.form.get(f'endseotag{i}'))
        seo_viewer.sseo0=sseo[0]
        seo_viewer.sseo1=sseo[1]
        seo_viewer.sseo2=sseo[2]
        seo_viewer.sseo3=sseo[3]
        seo_viewer.sseo4=sseo[4]
        seo_viewer.sseo5=sseo[5]
        seo_viewer.sseo6=sseo[6]
        seo_viewer.sseo7=sseo[7]
        seo_viewer.sseo8=sseo[8]
        seo_viewer.sseo9=sseo[9]

        seo_viewer.eseo0=eseo[0]
        seo_viewer.eseo1=eseo[1]
        seo_viewer.eseo2=eseo[2]
        seo_viewer.eseo3=eseo[3]
        seo_viewer.eseo4=eseo[4]
        seo_viewer.eseo5=eseo[5]
        seo_viewer.eseo6=eseo[6]
        seo_viewer.eseo7=eseo[7]
        seo_viewer.eseo8=eseo[8]
        seo_viewer.eseo9=eseo[9]
        db.session.commit()
        new_file=[]
        for i in range(10):
            new_file.append(request.files[f'file{i}'])
            if new_file[i].filename != "":
                os.remove(f'static\img\\{srno1+"."+str(i)}.jpg')
                new_file[i].save(os.path.join(
                    app.config['UPLOAD_FOLDER'], secure_filename(new_file[i].filename)))
                os.rename(
                    f'static\img\\{new_file[i].filename}', f'static\img\\{srno+"."+str(i)}.jpg')
            elif new_file[i].filename == "":

                pass

        
        return redirect(url_for('dashboard'))

    else:
        return redirect(url_for('dashboard'))


@app.route('/delete/<string:srno>', methods=['GET', 'POST'])
def delete_post(srno):
    if request.method == 'POST':
        data = blogpost.query.filter_by(srno=srno).first()
        seo1=seo.query.filter_by(srno=srno).first()
        db.session.delete(seo1)
        db.session.commit()
        db.session.delete(data)
        db.session.commit()
        for i in range(10):
            if os.path.isfile(f'static\img\{srno+"."+str(i)}.jpg'):
                os.remove(f'static\img\{srno+"."+str(i)}.jpg')
        return redirect(url_for('dashboard'))

    else:
        return redirect(url_for('dashboard'))


@app.route('/likebutton/<string:srno>', methods=['GET', 'POST'])
def like(srno):

    posts = blogpost.query.filter_by(srno=srno).first()
    likes = posts.like
    new_like = likes+1
    posts.like = new_like

    db.session.commit()

    return render_template('section.html',likes=posts.like)


# end of function section
app.run(debug=True)
