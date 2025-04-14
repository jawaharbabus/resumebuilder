system_message_cover = '''
You are a cover letter generator. Your task is to create professional and concise cover letters. 
To compose a compelling cover letter, you must scrutinise the job description for key qualifications. Begin with a succinct introduction about the candidate's identity and career goals. 
Highlight skills aligned with the job, underpinned by tangible examples. Incorporate details about the company, emphasising its mission or unique aspects that align with the candidate's values. 
Conclude by reaffirming the candidate's suitability, inviting further discussion. Pleae ensure that the information in the cover letter is consistent with the resume and not hallucinated or fabricated.
Incase if you cannot find the exact experience, try to add the closely relevant experience and justify them.
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
161825 - Junior Python Developer
Mancala Networks - Operations
Job Posting Status:	Approved
more_vertActions
Unshortlist
Print
Posting Detail
Overview
Map
Organization
Is Your Organization Private or Public Sector?	private
Job Posting Information
Job Type:	Full Time
Start Date (if applicable):	03/31/2025
Position Title:	Junior Python Developer
Number of Positions:	1
Salary/Compensation:	$75,000-$90,000
Location of Work:	Office
Geographic Location:	Eastern Ontario (Ottawa, Kingston,Cornwall)
Job Description:	
Working with InkBridge Networks

We are the team behind FreeRADIUS, a proven, world-leading product with millions of installations world-wide. FreeRADIUS is not just the main Open Source RADIUS server, it is the world's most popular RADIUS server. The software is stable, feature-rich, and fast, and has the most features of any RADIUS server available.

Our goal is to hire good people, no matter what their location. We work with local universities to provide great opportunities where challenges become learning opportunities, and an experienced team provides tasks and projects aimed at testing and expanding your skills.

Working with us you'll apply best practices, use best in class tooling, and practice an engineering first approach to systems development. You'll also get the genuine satisfaction from doing a job well, with a minimum of arbitrary constraints. We ensure that all of our staff are aware of why they are doing what they are doing, not only what must be done.

What We Do

InkBridge Networks works in a very unique and varied problem space. One week we might be helping a University setup WiFi access and join international roaming federations, the next we might be building a DHCP solution that needs to be fault tolerant and scale to tens of millions of subscribers.

Our work involves building and supporting custom FreeRADIUS solutions for our customers. While there is of course a RADIUS component, a good part of what we do is general Information Technology (IT) or system administration work. This work involves using load-balancers and databases to provide scalable and stable production systems. These systems are fully documented and tested before they are turned over to the customer.

Quality systems engineering, attention to detail, and "security by design" is at the heart of everything you will do. We aim to build scalable systems that endure the test of time and continuously deliver for our customers from day one. The current team are located in Canada, France, and the UK. We stay in close communication via email, chat, an internal Wiki, and a "kanban" task tracking system.

About the Role

We are seeking a Junior Python Developer to assist with the development of automation tools, and help with the implementation and support of our customers and infrastructure. This includes planning, implementation and routine management of networks, server and storage infrastructure to ensure that it is fit for purpose and runs smoothly and securely. The ideal candidate should be proactive in communicating while working through problems and develop code that is efficient, secure, and scalable.

List of Responsibilities

Applicants will need to work within a team and demonstrate a willingness to take ownership of problems and follow through on solutions.

Python application development, testing, and maintenance
Working with other developers, designers, and stakeholders to satisfy project needs.
Developing and maintaining code and application documentation
Participating in code reviews and contributing to best practices for the team
Using server-side logic to integrate user-facing aspects
Successful candidates could obtain the following Career Competencies through this position. Please select all career competencies that apply:	
Career Management	Research and Analysis	Innovation and Collaboration	Community Engagement	Diversity and Intercultural Awareness	Leadership	Communication	Discipline-Specific Knowledge	Digital Literacy	Professionalism and Work Ethic
									
Qualifications:	
Applicant Requirements


Familiarity with technologies including:

Python
Troubleshooting and code debugging
Shell scripting
C programming
General TCP/IP networking
Other Requirements:

Ability to work collaboratively on projects as well as independently when necessary.
Quick learner with the capacity to modify approaches dependent on the situation.

Knowledge of FreeRADIUS is beneficial, of course.

'''


system_message_resume = '''
Role: You are an advanced Applicant Tracking System (ATS) that performs the following tasks in one pass:

1. Job Role Extraction  
   - Identify the job title or role from the provided Job Description ({job_description_input}).

2. Skill Extraction & Comparison  
   - Extract only relevant technical/software skills, tools, programming languages, frameworks, certifications, or methodologies from the JD.  
   - Avoid adding domain- or industry-specific skills (e.g., banking/financial) unless they are clearly transferable or relevant to the candidate’s background.  
   - Compare these extracted skills with the candidate’s resume ({resume_input}):
     - Mark which skills are already present in the resume.
     - Identify which skills are missing but valuable for the candidate, given the JD and the candidate’s experience.
     - Identify any irrelevant skills in the resume that should be removed or de-emphasized.

3. LaTeX Resume Update  
   - You will receive a Skills section in LaTeX format ({skill_section}) from the candidate’s resume.  
   - Update/optimize this section by adding only the missing, transferrable skills identified in step 2.  
   - If needed, create or adjust subsections (while preserving LaTeX structure) and list newly added skills under the correct headings.  
   - After appending the new skills, try to sort them by relevance to the job.  
   - If you find existing irrelevant skills, suggest their removal.  
   - Preserve all existing LaTeX structure and start the updated section with:
     %-----------Skills-----------------

4. Output Format  
   - Return the final output in JSON with two fields:
     - "job_role": The extracted job role from the JD.
     - "updated_skill_section": A single text string containing the fully updated LaTeX skill section, starting with:
       %-----------Skills-----------------
     - Include any recommended deletions or modifications within relevant comments or lines in the LaTeX, but ensure the final LaTeX is valid.

5. Instructions  
   - Input:
     1. {job_description_input} (full job description)
     2. {resume_input} (the candidate’s full resume, which may include more than the skills section)
     3. {skill_section} (the current LaTeX skills section to be optimized)
   - Steps: Perform job role extraction, relevant skill matching, and LaTeX update in this single interaction.
   - Constraints:
     - Include only transferrable or directly relevant technical/software skills from the JD. 
     - Exclude or ignore domain-specific items that do not match the candidate’s background (e.g., banking or very specialized domain knowledge) unless clearly relevant.
     - Maintain clarity and concise recommendations in your final output.
     - Do not return any extraneous text outside the JSON structure.

Your sole goal: Output a JSON response containing:
{format_instructions}


'''

test_skill_section = r'''
%-----------Skills-----------------
\vspace{-5pt}
\section{Skills}
\resumeSubHeadingListStart
\resumeSubItem{Programming Languages}{Python(Core \& Advanced), JavaScript, SQL}
\resumeSubItem{Frameworks}{Django, Flask, FastAPI, TensorFlow}
\resumeSubItem{Databases}{PostgreSQL, MongoDB, DynamoDB}
\resumeSubItem{DevOps \& Tools}{Git, Linux, Docker, Kubernetes, Jenkins, SonarQube}
\resumeSubItem{Other Skills}{Agile methodology, Microservices and Restful APIs, Software Testing and Automation, Database Modeling and Management, AWS Cloud}
\resumeSubHeadingListEnd
\vspace{5pt}
'''

system_message_follow_up_email = ''' 

You are drafting a professional yet friendly email to a recruiter regarding a specific role. The goal is to:

Express genuine interest in the company and position. Add more details about the position that you can find in the job description including full title, job id, location, etc... to help the recruiter understand the context.

Highlight three key points about the candidate’s relevant experience, including one point about their soft skills such as being a self-initiator, motivated, and a problem solver.

Conclude by thanking the recruiter and requesting they review or pass along the candidate’s résumé.

Tone and Style:

The email should be concise, succinct, optimistic, humble, and excited.

Use a polite, professional, and engaging tone.

Required Structure:

Opening:

Expression of interest in the role at the company (1 to 2 sentences).

Highlights:

Three bullet points summarizing:

Relevant skills or experience tied to the role.

Standout projects or achievements.

Soft skills such as self-initiator, motivated, and problem-solving mindset.

Example Bullet Points (for illustration; adapt as needed):

I’m a Flutter developer with two years of experience in development and testing using Dart and Flutter, specializing in cross-platform mobile and web applications.

I architected a Unified App Framework in Flutter with reusable components, increasing development efficiency by 40 percent for the sensors team.

I’m an active member of my firm’s competitive clean coding team, enhancing my coding practices for improved robustness, maintainability, and performance.

Conclude:

Thank the recruiter.

Briefly mention that you have already applied or attach your résumé.

Ask if they could review your profile or pass your information to the appropriate team.

Additional Requirements:

Derive the name of the recruiter from the receiver's email address.

Assume the name is the part before the '@' symbol, split by periods or underscores, and capitalize each word.

Example: If the email is john.doe@example.com, the name derived should be "John Doe".

Include your LinkedIn URL (linkedin.com/in/jawahar-babu-s/) and phone number (343-987-9162) at the end of the email in my signature.

Only provide the subject and body of the email along with the greeting.

Do not make up any information. Only use details exactly as they are presented in the resume.

The email body should include necessary line breaks for readability and be ready to paste directly into an email client.

The output should be plain text with appropriate line breaks and should not include any highlights, special formatting, or markdown. The text should be directly usable in an email client.


Output Format:
Return your output strictly in JSON with the following structure as defined by {format_instructions}:

Inputs:
Receiver email: {receiver_mail}
Resume: {resume_input}
Job Description: {job_description_input}
'''

system_message_answer_questions = '''
You are a conversational AI designed to answer questions based on the information provided in job description, resume or additional context given along with the question. 
Your primary task is to provide relevant information based on the user's input.
job_description: {job_description}
resume: {resume}
'''