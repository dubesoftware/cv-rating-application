import os
import convertapi
from openai import OpenAI
from werkzeug.utils import secure_filename

# Instantiate OpenAI client
client = OpenAI(api_key=os.environ.get('OPENAI_KEY'))
# Create OpenAI assistant with file search enabled
assistant = client.beta.assistants.create(
    name="CV Reviewer Assistant",
    instructions="You are an expert CV reviewer. Use your knowledge of recruitment to provide feedback on a CV.",
    model="gpt-4o",
    tools=[{"type": "file_search"}],
)
# Create a vector store called "CVs"
vector_store = client.beta.vector_stores.create(name="CVs")

def save_file(file):
    file_path = os.path.join('uploads', secure_filename(file.filename))
    file.save(file_path) 
    return file_path

def convert_pdf_to_text(file_path):
    # Use ConvertAPI to convert PDF to text
    convertapi.api_credentials = os.environ.get('CONVERTAPI_SECRET')
    convertapi.convert('txt', {
        'File': file_path
    }, from_format = 'pdf').save_files(os.path.join('converted', 'converted.txt'))

def get_openai_feedback(text):
    # Prepare the file for upload to OpenAI
    file_path = "converted/converted.txt"
    file_stream = open(file_path, "rb")
    # Use the upload and poll SDK helper to upload the file, add it to the vector store,
    # and poll the status of the file for completion.
    client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=[file_stream]
    )
    # Update the assistant to use the vector store
    client.beta.assistants.update(
        assistant_id=assistant.id,
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )
    # Upload the user provided file to OpenAI
    message_file = client.files.create(
        file=file_stream, purpose="assistants"
    )
    # Create a thread and attach the file to the message
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": "Review the attached CV and return a quality score out of " +
                "10, as well as a list of recommendations.",
            
                # Attach the file to the message.
                "attachments": [
                    { "file_id": message_file.id, "tools": [{"type": "file_search"}] }
                ],
            }
        ]
    )
    # Close the file stream
    file_stream.close()
    # Create a Run and observe that the model uses the File Search tool to provide a response
    # to the user’s question
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id, assistant_id=assistant.id
    )
    messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
    message_content = messages[0].content[0].text
    annotations = message_content.annotations
    citations = []
    for index, annotation in enumerate(annotations):
        message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
        if file_citation := getattr(annotation, "file_citation", None):
            cited_file = client.files.retrieve(file_citation.file_id)
            citations.append(f"[{index}] {cited_file.filename}")
    return message_content.value

    def delete_file(file_path):
        os.remove(file_path)

    def clean_up_resources(file_path):
        # Clean up uploaded CV PDF and converted .txt files
        file_paths = [
            file_path,
            "converted/converted.txt"
        ]
        list(map(delete_file, file_paths))
        return True
