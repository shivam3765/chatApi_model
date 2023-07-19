  Generate Qurestion and Answer Model

  ------------- Flow Diagram --------------
  
  +-----------------------+
  | Get PDF file URL      |
  |   related to subject. |
  +-----------+-----------+
              |
              v
  +-----------------------+
  | Extract content from  |
  |         PDF           |
  +-----------+-----------+
              |
              v
  +-----------------------+
  |    Create chunks      |
  +-----------+-----------+
              |
              v
  +-------------------------+
  |   Pass each chunk       |
  |                         |
  |   +------------------+  |
  |   |Prompt to generate|  |
  |   |question & answer |  |
  |   |       pair.      |  |
  |   +--------+---------+  |
  |            |            |
  |            v            |
  |   +--------+--------+   |
  |   |    Chat model    |  |
  |   +--------+--------+   |
  |            |            |
  |            v            |
  +-----------+-------------+
              |
              v
  +-----------------------+
  |    Generated Q&A      |
  +-----------------------+


Description:

1. User : The user uses the server post method to give the pdf url to the model
        in order to retrieve a question and answer set depending on the contents of
        the pdf.

2. Extract pdf : To make it easier to understand each piece of content, extract
        all of it from the PDF file using the library (PyPDF2).

3. Create chunk : Create a chunk by splitting the content into smaller pieces
        once it has been extracted, saving each piece into a list, and then calling
        each list as a chunk using the lanchain (text_splitter) recursively.

4. Passing chunk : Providing each chunk to the model so it may produce a
        question and answer set based on the piece.

5. Prompt : A prompt is a process of model that explains how questions and
        answers will be created from PDF information.

6. Model : A model based on the OpenAI chat model that is implemented with
        Python using langchain library.

7. Result : the model outputs a question and answer pair in JSON format.