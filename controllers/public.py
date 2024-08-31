from flask import render_template

def index():
    return render_template('public/index.html')

def about():
    return render_template('public/about.html')

def event():
    return render_template('public/event.html')