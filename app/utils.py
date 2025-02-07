import os
import requests
import convertapi

def convert_pdf_to_text(file_path):
    # Use ConvertAPI to convert PDF to text
    convertapi.api_credentials = 'secret_lRQkjhj9nFEPNunH'
    convertapi.convert('txt', {
        'File': file_path
    }, from_format = 'pdf').save_files(os.path.join('uploads', 'converted'))

def get_openai_feedback(text):
    # To do: Implement OpenAI API call
    pass