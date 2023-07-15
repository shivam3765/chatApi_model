from fastapi import FastAPI
import uvicorn
from extract_text.extract_text_from_pdf import extract_text_from_pdf
from qa_pairs.generate_qa_pairs import generate_qa_pairs
import requests
from schama.Doc import Doc


app = FastAPI()

# here use get route
@app.get('/generate_qa_pairs')
def start():
    return "hello world"

# here use post route
@app.post('/generate_qa_pairs')
async def generate_qa_pairs_api(request: Doc):

    response = request.pdf_url
    subject_input = request.subject

    file = requests.get(response)

    if file.status_code == 200:
        filename = response.split("/")[-1]
        with open(filename, 'wb') as f:
            f.write(file.content)

    # filename = "english_subject.pdf"
    chunks = extract_text_from_pdf(filename)

    # return chunks

    qa_pairs = generate_qa_pairs(chunks, subject_input)

    return qa_pairs


if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8000)

    # uvicorn app:app --reload
