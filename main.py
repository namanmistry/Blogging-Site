from flask import Flask,render_template



app=Flask(__name__)
@app.route('/')
def home():
    return "naman is my name"

if __name__ == "__main__":
    app.run()
