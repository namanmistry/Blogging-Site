from flask import Flask,render_template

app=Flask(__name__)
with open('config.json', 'r') as c:
    params = json.load(c)
app.config['DATABASE_URL'] = params['params']['data-base']
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
    return render_template('index.html')

if __name__=='__main__':
    app.run()
