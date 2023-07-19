from src.extract_text.create_chunk import extract_text_from_pdf
from src.qa_pairs.generate_qa_pairs import generate_qa_pairs
import requests
from src.schema.Doc import Doc
from src.utils.logger import logManager

logger = logManager()

from fastapi.routing import APIRouter

router = APIRouter()


# here use get route
@router.get('/generate_qa_pairs')
def start():
    return "hello world"

# here use post route
@router.post('/generate_qa_pairs')
async def generate_qa_pairs_api(request: Doc):

    logger.info("server waiting for request")
    response = request.pdf_url
    subject_input = request.subject

    file = requests.get(response)

    if file.status_code == 200:
        
        filename = response.split("/")[-1]
        with open(filename, 'wb') as f:
            f.write(file.content)
            logger.info("pdf successfully download...")
    else:
        logger.error("pdf url not get")

    # filename = "english_subject.pdf"
    chunks = extract_text_from_pdf(filename)



    qa_pairs = generate_qa_pairs(chunks, subject_input)

    logger.info("successfully get response from post request")
    return qa_pairs
