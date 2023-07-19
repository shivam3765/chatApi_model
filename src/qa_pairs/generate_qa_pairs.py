import json
import re
from langchain import PromptTemplate, LLMChain
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
from src.utils.config import ConfigManager
from src.utils.logger import logManager

logger = logManager()
    

# geneate question and answer pairs function -------------------
def generate_qa_pairs(chunks, subject_input):

    try:

        # Load API key from config file
        config_manager = ConfigManager()
        api_key = config_manager.get_api_key()

        # Load prompt from config prompts file
        system_prompts = config_manager.get_system_prompts()
        assistent_prompts = config_manager.get_assistent_prompts()

        logger.info("Loading......")
        response_schemas = [
            ResponseSchema(
                name="question", description="The question should cover a range of difficulty levels, including both easy and hard questions."),
            ResponseSchema(
                name="answer", description="generate the answer according to the question in detail, with bullet points.")
        ]

        output_parser = StructuredOutputParser.from_response_schemas(
            response_schemas)

        # here define model ---------------------------
        chat = ChatOpenAI(
            model="gpt-3.5-turbo-0301",
            temperature=0,
            openai_api_key=api_key)

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
            template = system_prompts[0]
            system_message_prompt = SystemMessagePromptTemplate.from_template(template)

            # Here is a Assistent Prompt ------------------------------
            assistent_template = assistent_prompts[0]
            
            
        # Here the template for english subject -----------------------------
        elif subject_input == 'english':

            # Here is a System Prompt ---------------------
            template = system_prompts[1]
            system_message_prompt = SystemMessagePromptTemplate.from_template(template)

            # Here is a Assistent Prompt ------------------------------
            assistent_template = assistent_prompts[1]
            
        # Here the template for scuence subject --------------------------
        elif subject_input == 'science':

            # Here is a System Prompt ---------------------
            template = system_prompts[2]
            system_message_prompt = SystemMessagePromptTemplate.from_template(template)

            # Here is a Assistent Prompt ------------------------------ 
            assistent_template = assistent_prompts[2]
            
        # Here the template for social science subject -------------------------
        elif subject_input == 'social science':

            # Here is a System Prompt ---------------------
            template = system_prompts[3]
            system_message_prompt = SystemMessagePromptTemplate.from_template(template)

            # Here is a Assistent Prompt ------------------------------
            assistent_template = assistent_prompts[3]
            
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

        logger.info("Q & A successfully generated.....")
        return data
    
    except Exception as e:
        logger.error(f"Error message: {str(e)}")
