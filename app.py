import os
import json
import re
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain import PromptTemplate, LLMChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    AIMessagePromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

from fastapi import FastAPI
import requests
import uvicorn
from pydantic import BaseModel


app = FastAPI()


# this function extract text from pdf
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
        print(chunks_list[0])
        return chunks_list


# this function generate Q&A Pairs
def generate_qa_pairs(chunks, subject_input):

    response_schemas = [
        ResponseSchema(
            name="question", description="The question should cover a range of difficulty levels, including both easy and hard questions."),
        ResponseSchema(
            name="answer", description="generate the answer according to the question in detail, with bullet points.")
    ]

    output_parser = StructuredOutputParser.from_response_schemas(
        response_schemas)

    # load_dotenv()
    # openapi key -------------------
    openai_api_key = "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"

    # here define model ---------------------------
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-0301",
        temperature=0,
        openai_api_key=openai_api_key)

    # here written prompt---------------------
    prompt = PromptTemplate(
        template="""\ncontext: <{chunks}>\n{format_instructions}""",
        input_variables=["chunks"],
        partial_variables={
            "format_instructions": output_parser.get_format_instructions()}
    )

    # Here the template for maths subject ------------------------------
    if subject_input == 'maths':

        # Here is a System Prompt ---------------------
        template = """You are a maths teacher's assistant who uses the given context to help you come up with five question-and-answer pairs.\n

        Chain of thought:
        [step 1]: Identify the problem: Read the question and identify the key information, such as the variables, units, and relationships between them.\n
        [step 2]: [Identify the intermediate steps]: Break down the question into smaller steps and identify the intermediate calculations that need to be performed to arrive at the final answer.\n
        [step 3]: [Develop a chain of thought]: Create a structured sequence of context that correspond to the intermediate steps identified in the previous step. Each context should be phrased in a clear and concise manner to guide the language model through the thought process. Ensure that the context maintain a logical flow, moving from one step to the next.\n
        [step 4]: [Generate the question and answer pair]: Use the provided context to generate the question and answer pair for the problem. The question should be phrased in a natural language that reflects the problem, while the answer should be a numerical value with the appropriate units.\n

    give the desired outcome, using chain of thought."""
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)

        # Here is a Assistent Prompt ------------------------------
        assistent_template = '''use the example below as a guide when creating question and answer pairings.\n
        For example, let's consider the following problem:
    <question>: A recipe calls for 2 cups of flour to make 12 cookies. How many cups of flour are needed to make 36 cookies?\n

    <answer>:
    Identify the problem: The problem is asking for the amount of flour needed to make 36 cookies, given the amount needed to make 12 cookies.
    Identify the intermediate steps: We need to use proportions to find the amount of flour needed. We can set up a proportion: 2 cups / 12 cookies = x cups / 36 cookies. We can solve for x by cross-multiplying and simplifying: x = (2 cups * 36 cookies) / 12 cookies = 6 cups.
    Develop a chain of thought:
    Prompt 1: What is the given amount of flour needed to make 12 cookies?
    Prompt 2: What is the given number of cookies that the recipe makes?
    Prompt 3: Use proportions to find the amount of flour needed to make 36 cookies.
    Generate the question and answer pair: How many cups of flour are needed to make 36 cookies if the recipe calls for 2 cups of flour to make 12 cookies? Answer: 6 cups.
    Therefore, the amount of flour needed to make 36 cookies is 6 cups. This chain of thought prompt can be used by teachers to generate question and answer pairs for their students, making it easier for them to practice and learn mathematical word problems.'''
        
        
    # Here the template for english subject -----------------------------
    elif subject_input == 'english':

        # Here is a System Prompt ---------------------
        template = """You are a teacher's assistant who helps them make five question-and-answer pairs Using the provided context.\n"""
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)

        # Here is a Assistent Prompt ------------------------------
        assistent_template = '''use the example below as a guide when creating question and answer pairings.\n

        For example, let's consider the following problem:
    <question>:  What is the Question-Answer Relationship (QAR) comprehension strategy and how is it used in the classroom?\n

    <answer>:  The QAR comprehension strategy is a teaching method that helps students ask key questions about their reading and find the answers to their questions, whether it means locating a specific fact, drawing an inference, or connecting the reading to their own experience. This strategy is used within the classroom to facilitate learning of a topic, revision of the material, and to help students understand the relationship between questions and answers......'''
        
    # Here the template for scuence subject --------------------------
    elif subject_input == 'science':

        # Here is a System Prompt ---------------------
        template = """You are a assistant for a school teachers to help, Generate a five pairs of question and its corresponding answer based on the given context."""
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)

        # Here is a Assistent Prompt ------------------------------ 
        assistent_template = '''use the example below as a guide when creating question and answer pairings.\n
        For example, let's consider the following problem:
    <question>: A ball of mass M is thrown vertically upwards at speed V.
It reaches a maximum height of H in a time T.
A second ball of mass M/2 is thrown vertically upwards at the same speed.
Ignoring air resistance, how long does it take the second ball to reach its maximum height?\n

    <answer>: Sure, I can help you with that question.
The time it takes for the second ball to reach its maximum height can be found using the same equations that we use for the first ball. The only difference is that we use the mass M/2 instead of M.
When the first ball is thrown upwards, it experiences a constant acceleration due to gravity, which we can assume to be approximately equal to 9.81 m/s^2. The initial velocity of the ball is V, and its final velocity at the maximum height is 0.
Using the equation of motion for constant acceleration:
H = V*T - (1/2)gT^2
where H is the maximum height, V is the initial velocity, T is the time taken to reach the maximum height, and g is the acceleration due to gravity.
Solving for T, we get:
T = V/g + sqrt((V/g)^2 + 2H/g)
Now, for the second ball of mass M/2, we can use the same equation with the initial velocity V and acceleration due to gravity g, but with the mass M/2:
T' = V/g + sqrt((V/g)^2 + 2H/g)
Therefore, the time it takes for the second ball to reach its maximum height is also T'.
So, the answer is that it takes the second ball the same amount of time T' as it takes for the first ball to reach its maximum height.'''
        
    # Here the template for social science subject -------------------------
    elif subject_input == 'social science':

        # Here is a System Prompt ---------------------
        template = """You are a assistant for a social science teachers to help, Generate a pairs of question and its corresponding answer based on the given context.\n"""
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)

        # Here is a Assistent Prompt ------------------------------
        assistent_template = '''use the example below as a guide when creating question and answer pairings.\n

        For example, let's consider the following problem:
    <question>:\n

    <answer>: '''
        
    else:
        return "Enter the valid subject like: (maths, english, social science, science)"
    


    assistent_message_prompt = AIMessagePromptTemplate.from_template(
        assistent_template)
    human_message_prompt = HumanMessagePromptTemplate(prompt=prompt)
    chat_prompt = ChatPromptTemplate.from_messages(messages=[system_message_prompt,
                                                             assistent_message_prompt,
                                                             human_message_prompt,
                                                             ])

    chain = LLMChain(llm=chat, prompt=chat_prompt)

    data = []  # list of question and answer --------------------

    # here each chunk pass into llm -----------------
    for chunk in chunks[:1]:
        llm_output = chain.run({"chunks": chunk,
                                })
        
    
        # here output format in JSON -------------------
        pattern = r'\{[^{}]*\}'
        json_strings = re.findall(pattern, llm_output)

        for json_string in json_strings:
            clean_string = json_string.replace(
                '```json\n', '').replace('```', '')
            obj = json.loads(clean_string)
            question = obj['question']
            answer = obj['answer']
            data.append({'question': question, 'answer': answer})

    questions = [item["question"] for item in data]
    answers = [item["answer"] for item in data]

    for i in range(len(questions)):
        ques = f"Question {i+1}: {questions[i]}"
        ans = f"Answer {i+1}: {answers[i]}"
        print(ques)
        print(ans)
        print()

    return data


class Doc(BaseModel):
    pdf_url: str
    subject: str

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
