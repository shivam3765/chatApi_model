from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter


def extract_text_from_pdf(pdf):

    if pdf is not None:
        pdf_reader = PdfReader(pdf)

        raw_text = ''
        for i, page in enumerate(pdf_reader.pages):
            text = page.extract_text()
            if text:
                raw_text += text

        text_splitter = CharacterTextSplitter(
            separator = "\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )

        chunks_list = text_splitter.split_text(raw_text)

        # chunks.append(chunks_list)
        # print(chunks_list[0])
        return chunks_list
