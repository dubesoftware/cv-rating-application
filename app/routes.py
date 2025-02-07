import os
from flask import render_template, request, redirect, url_for
from . import app
from app.utils import save_file, convert_pdf_to_text, get_openai_feedback

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
                return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            # Save the file temporarily
            file_path = save_file(file)
            # Convert PDF to text
            text = convert_pdf_to_text(file_path)
            # Get feedback from OpenAI
            feedback = get_openai_feedback(text)
            # Display the results
            return render_template('index.html', feedback=feedback)
    return render_template('index.html')
