from flask import app, render_template, request

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Do some processing here
        pass
    return render_template('index.html')