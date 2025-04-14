from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import HumanMessage, SystemMessage
from pypdf import PdfReader
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.chains import LLMChain, SequentialChain,ConversationChain
from system_promts import *
import os
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Access an environment variable
DEEPSEEK_API = os.getenv('DEEPSEEK_API')


# Schema for cover letter.
class CoverLetter(BaseModel):
    role: str = Field(description="Role from the job description")
    company: str = Field(description="Company from the job description")
    body: str = Field(description="Body of the cover letter without any salutation or regards")

class ResumeOutput(BaseModel):
    job_role: str = Field(description="Job role extracted from the job description")
    updated_skill_section: str = Field(description="Updated LaTeX formatted skill section for the resume")

class FollowUpEmail(BaseModel):
    subject: str = Field(description="Subject of the follow-up email")
    body: str = Field(description="Content of the follow-up email without signature or regards")
    
cover_letter_json_parser = JsonOutputParser(pydantic_object=CoverLetter)
resume_output_parser = JsonOutputParser(pydantic_object=ResumeOutput)
follow_up_email_parser = JsonOutputParser(pydantic_object=FollowUpEmail)


class AIBuilder:
    def __init__(self):
        self.llm = None

    def initialize_llm(self):
        self.llm = ChatDeepSeek(
            model="deepseek-chat",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=DEEPSEEK_API,
            # other params...
        )

    def build_cover(self, job_description, resume_path):
        prompt = PromptTemplate(
            template= system_message_cover,
            input_variables=["resume_input","job_description_input"],
            partial_variables={"format_instructions": cover_letter_json_parser.get_format_instructions()},
        )
        chain = prompt | self.llm | cover_letter_json_parser
        resume = self.load_pdf(resume_path)
        cover_letter = chain.invoke({"resume_input": resume, "job_description_input":job_description})
        cover_letter["company"] = self.make_latex_friendly(cover_letter["company"])
        cover_letter["body"] = self.make_latex_friendly(cover_letter["body"]).split("\n")
        return cover_letter
    
    
    def build_resume(self, job_description, skill_section, resume_path):
        # chain
        prompt = PromptTemplate(
            template= system_message_resume,
            input_variables=["resume_input","job_description_input","skill_section","format_instructions"],
        )
        chain = prompt | self.llm | resume_output_parser
        resume = self.load_pdf(resume_path)
        result = chain.invoke({"resume_input": resume, "job_description_input": job_description, "skill_section": skill_section, "format_instructions": resume_output_parser.get_format_instructions()})
        response = result
        return (self.make_latex_friendly(response["job_role"]), self.make_skills_latex_friendly(response["updated_skill_section"]))
    
    def draft_follow_up_email(self, job_description, receiver_mail, resume_path):
        prompt = PromptTemplate(
            template= system_message_follow_up_email,
            input_variables=["resume_input","job_description_input", "receiver_mail","format_instructions"],
        )
        chain = prompt | self.llm | follow_up_email_parser
        resume = self.load_pdf(resume_path)
        followup_email = chain.invoke({"resume_input": resume, "job_description_input":job_description, "receiver_mail": receiver_mail, "format_instructions": follow_up_email_parser.get_format_instructions()})
        return followup_email

    def answer_questions(self, job_description, resume_path):
        global system_message_answer_questions
        resume = self.load_pdf(resume_path)
        system_message_answer_questions = system_message_answer_questions.format(resume=resume, job_description=job_description)
        memory = ConversationBufferMemory()
        prompt = PromptTemplate(
            template= '''You are a Job Application Assistant Bot. Provide a comprehensive, specific, and human-like response that is optimistic and excited, keeping it concise in a single paragraph.
              Your answer should reflect the enthusiasm and the candidate's alignment with the job role while being clear and to the point. Answer the following question: {question} using the provided context: {context}, along with the candidate's resume and the job description.
              Answer in the first person, imagining yourself as the candidate while responding.''',
            input_variables=["question","context"],
        )
        memory.chat_memory.add_user_message(system_message_answer_questions)
        chain = ConversationChain(
            llm= self.llm,
            memory=memory,
        )
        system_message_answer_questions.format()
          
        while True:
            question = input("AI > Enter the question: ")
            if question == "quit" or question == "exit":
                break
            context = input("AI > Give the context: ")
            inputMessage = prompt.format(question=question, context=context)
            response = chain.invoke({"input": inputMessage})
            print("\n"+ response["response"] + "\n")
           
    # helper
    def load_pdf(self, path):
        reader = PdfReader(path)
        # print(len(reader.pages))
        page = reader.pages[0]
        # print(page.extract_text())
        return page.extract_text()

    def make_latex_friendly(self, text):
        special_chars = {
            '%': r'\%',
            '&': r'\&',
            '#': r'\#',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '$': r'\$',
            '^': r'\^{}',
            '~': r'\~{}',
            # '\\': r'\textbackslash{}'
        }
        for char, replacement in special_chars.items():
            text = text.replace(char, replacement)
        text = text.replace('c++', r'C\texttt{++}')
        return text
    
    def make_skills_latex_friendly(self, text):
        special_chars = {
            ' & ': r' \& ',
            '#': r'\#'
        }
        for char, replacement in special_chars.items():
            text = text.replace(char, replacement)
        text = text.replace('C++', r'C\texttt{++}')
        text = text.replace('c++', r'C\texttt{++}')
        return text


    


# ai_builder = AIBuilder()
# ai_builder.initialize_llm()
# skill_suggestions = ai_builder.build_resume(test_job_description, test_skill_section, "../python/resume_python.pdf")
# print(skill_suggestions)