from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import HumanMessage, SystemMessage
from pypdf import PdfReader
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
import os

# Access an environment variable
DEEPSEEK_API = os.getenv('DEEPSEEK_API')


# Schema for cover letter.
class CoverLetter(BaseModel):
    role: str = Field(description="Role from the job description")
    company: str = Field(description="Company from the job description")
    body: str = Field(description="Body of the cover letter without any salutation or regards")

parser = JsonOutputParser(pydantic_object=CoverLetter)

system_message = '''
You are a cover letter generator. Your task is to create professional and concise cover letters. 
To compose a compelling cover letter, you must scrutinise the job description for key qualifications. Begin with a succinct introduction about the candidate's identity and career goals. 
Highlight skills aligned with the job, underpinned by tangible examples. Incorporate details about the company, emphasising its mission or unique aspects that align with the candidate's values. 
Conclude by reaffirming the candidate's suitability, inviting further discussion. 
Use job-specific terminology for a tailored and impactful letter, maintaining a professional style suitable for a software developer. Please provide the body of the coever letter in around 750 words (1 page).
The cover letter should be in json format:
{format_instructions}

For eg:
"role": <role>
"company": <company name>
"body": <cover letter>

I don't want my info, to info, sincerly, regards or even salutation. just the content, only the body of the cover letter and body alone.
your output is directly parsed by a script. hence, I dont want any other words other than mentioned here. Thanks
I have attached my resume for this role.
{resume_input}
Also I have attached the job description for the role I am applying for.
{job_description_input}

I strongly emphazise that I want a 750 words cover letter body. Multiple paragraphs, each seperated by newlines \\n.
'''

test_job_description = '''
About the job
About Citi:

Citi, the leading global bank, has approximately 200 million customer accounts and does business in more than 160 countries and jurisdictions. Citi provides consumers, corporations, governments, and institutions with a broad range of financial products and services, including consumer banking and credit, corporate and investment banking, securities brokerage, transaction services, and wealth management.

As a bank with a brain and a soul, Citi creates economic value that is systemically responsible and in our clients’ best interests. As a financial institution that touches every region of the world and every sector that shapes your daily life, our Operations & Technology teams are charged with a mission that rivals any large tech company. Our technology solutions are the foundations of everything we do from keeping the bank safe, managing global resources, and providing the technical tools our workers need to be successful to designing our digital architecture and ensuring our platforms provide a first-class customer experience. We reimagine client and partner experiences to deliver excellence through secure, reliable, and efficient services.

The Software Engineer is an intermediate level position responsible for participation in the establishment and implementation of new or revised application systems and programs in coordination with the Technology team. The overall objective of this role is to contribute to applications systems analysis and programming activities.

Responsibilities:

Utilize knowledge of applications development procedures and concepts, and basic knowledge of other technical areas to identify and define necessary system enhancements, including using script tools and analyzing/interpreting code
Consult with users, clients, and other technology groups on issues, and recommend programming solutions, install, and support customer exposure systems
Apply fundamental knowledge of programming languages for design specifications.
Analyze applications to identify vulnerabilities and security issues, as well as conduct testing and debugging
Serve as advisor or coach to new or lower level analysts
Identify problems, analyze information, and make evaluative judgements to recommend and implement solutions
Resolve issues by identifying and selecting solutions through the applications of acquired technical experience and guided by precedents
Has the ability to operate with a limited level of direct supervision. 
Can exercise independence of judgement and autonomy. 
Acts as SME to senior stakeholders and /or other team members.
Appropriately assess risk when business decisions are made, demonstrating particular consideration for the firm's reputation and safeguarding Citigroup, its clients and assets, by driving compliance with applicable laws, rules and regulations, adhering to Policy, applying sound ethical judgment regarding personal behavior, conduct and business practices, and escalating, managing and reporting control issues with transparency.
Collaborate with cross-functional teams, including product managers, designers, and other engineers, to gather requirements, brainstorm solutions, and deliver high-quality software.
Write clean, efficient, and well-documented code.
Conduct code reviews and participate in peer programming to ensure code quality and knowledge sharing.
Troubleshoot and debug software issues, identifying and resolving bugs effectively.
Stay up-to-date with the latest technologies and trends in full-stack development.
Contribute to the continuous improvement of our development processes and best practices.

Qualifications:

2+ years of relevant experience in the Financial Service industry with Back End, preferred Full Stack experience
2+ years of professional experience in software engineering, with a strong focus on full-stack development.
Expertise in AngularJS for front-end development.
Design, develop, and implement scalable and maintainable web applications using AngularJS, Spring Boot, and SQL.
Proficiency in Spring Boot for building robust and scalable backend systems.
Strong SQL skills for database design, querying, and optimization.
Experience with RESTful APIs and microservices architecture.
Excellent problem-solving and analytical skills.
Strong communication and collaboration skills

'''


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
            template= system_message,
            input_variables=["resume_input","job_description_input"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        chain = prompt | self.llm | parser
        # Build cover letter logic here
        resume = self.load_pdf(resume_path)
        
        cover_letter = chain.invoke({"resume_input": resume, "job_description_input":job_description})
        cover_letter["body"] = self.make_latex_friendly(cover_letter["body"]).split("\n")
        # print(cover_letter["body"])
        return cover_letter
    

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

    


# ai_builder = AIBuilder()
# ai_builder.initialize_llm()
# cover_letter = ai_builder.build_cover(test_job_description, "../python/resume_python.pdf")
# print(cover_letter)