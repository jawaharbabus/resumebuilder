import os
import sys
import subprocess
import platform
from ai import AIBuilder
from gsheets import GSheets
import warnings
warnings.filterwarnings("ignore")
import json
from mail import Mailer
import concurrent.futures
import requests
import json

# Define the order of the common sections
common_sections = [
    "design.tex",
    "header.tex",
    "education.tex",
    "certifications.tex"
]

# Directory containing the LaTeX files
directory = "tex"

# List of valid resume types
valid_resume_types = {"backend", "frontend", "fullstack", "javascript", "python", "java", "general", "ai", "test"}

def build_common_resume():
   for resume_type in valid_resume_types:
        build_resume(resume_type, resume_type, common=True)

def generate_pdf(output_dir, tex_file):
    """Generate PDF from .tex file and clean up auxiliary files."""
    if platform.system() == "Linux" or platform.system() == "Windows":
        subprocess.run(["pdflatex", "-output-directory", output_dir, tex_file], check=True)
    else:
        print("PDF generation is not supported on this platform.")
        return

    # Clean up the directory by removing all files except .tex and .pdf
    for filename in os.listdir(output_dir):
        if not (filename.endswith(".tex") or filename.endswith(".pdf") or filename.endswith(".txt")):
            os.remove(os.path.join(output_dir, filename))

def build_resume(resume_type, company_name, common = False):
    
    """Build the resume by concatenating LaTeX files."""
    specific_sections = [
        f"skills_{resume_type}.tex",
        f"experience_{resume_type}.tex"
    ]
    job_description_file = f"../job_description_placeholder.txt"
    # Create the output directory
    if not common:
        output_dir = os.path.join("..", company_name)
        # clean up the directory
        if os.path.exists(output_dir):
            for filename in os.listdir(output_dir):
                file_path = os.path.join(output_dir, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)
        if not os.path.exists(job_description_file):
            print(f"Error: {job_description_file} does not exist.")
            sys.exit(1)
        with open(job_description_file, "r") as file:
            job_description = file.read().strip()

    else:
        output_dir = os.path.join("..", "common")

    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"resume_{company_name}.tex")

 
    resume_content = "" 

    # extract jobrole and skills
    ai_results = tuple()
    section_path = os.path.join(directory, specific_sections[0])
    if os.path.exists(section_path):
        with open(section_path, 'r') as file:
            if "skills" in section_path:
                if not common:
                    ai_results = build_skills_using_ai(job_description, file.read(), f"../common/resume_{resume_type}.pdf")
                    # print(ai_results)
    else:
        print(f"Warning: {specific_sections[0]} does not exist.")
    role = ai_results[0]
    # Read and concatenate the contents of each section
    for section in ["design.tex","header.tex", "education.tex"] + specific_sections + ["certifications.tex"]:
        section_path = os.path.join(directory, section)
        if os.path.exists(section_path):
            with open(section_path, 'r') as file:
                if "header.tex" in section_path:
                    resume_content += file.read().replace("<<job_role>>", role)
                elif "skills" in section_path:
                    if not common:
                        resume_content += ai_results[1] + "\n"
                else:
                    resume_content += file.read() + "\n"
        else:
            print(f"Warning: {section_path} does not exist.")

    resume_content += "\\end{document}\n"

    # Write the concatenated content to the output file
    with open(output_file, 'w') as file:
        file.write(resume_content)

    print(f"Resume for {resume_type} has been built and saved to {output_file}")

    # Generate the PDF file from the .tex file
    generate_pdf(output_dir, output_file)
    GSheets().get_values([company_name, role, resume_type])


def generate_from_existing(company_name):
    """Generate PDF from an existing LaTeX file and clean up."""
    output_dir = os.path.join("..", company_name)
    tex_file = os.path.join(output_dir, f"resume_{company_name}.tex")

    if not os.path.exists(tex_file):
        print(f"Error: {tex_file} does not exist.")
        sys.exit(1)

    # Generate the PDF file from the .tex file
    generate_pdf(output_dir, tex_file)

# Function to build a cover letter
def build_cover_letter(company_name):
    """Build a cover letter by interpolating role and company details."""

    # Read the job description from the placeholder file
    job_description_file = f"../job_description_placeholder.txt"
    if not os.path.exists(job_description_file):
        print(f"Error: {job_description_file} does not exist.")
        sys.exit(1)

    with open(job_description_file, "r") as file:
        job_description = file.read().strip()
    ai_cover = build_cover_using_ai(job_description, f"../{company_name}/resume_{company_name}.pdf")
    # ai_cover = build_cover_using_ai(job_description, f"../common/resume_general.pdf")

    # Create the output directory
    output_dir = os.path.join("..", company_name)
    os.makedirs(output_dir, exist_ok=True)

    # Read the header file
    header_file = os.path.join(directory, "cover_header.tex")
    if not os.path.exists(header_file):
        print(f"Error: {header_file} does not exist.")
        sys.exit(1)

    with open(header_file, "r") as file:
        header_content = file.read()

    # Replace placeholders in the header
    header_content = header_content.replace("{company}", ai_cover["company"]).replace("{role}", ai_cover["role"])

    # Process body content: add spacing before paragraphs
    # body_with_spacing = "\n\n\\vspace{0.5cm}\n".join(ai_cover["body"])
    body_with_spacing = "\n\n\\vspace{0.5cm}".join([paragraph for paragraph in ai_cover["body"] if paragraph.strip()])

    # Footer content
    footer_content = "\n\n\\makeletterclosing\n\\end{document}\n"

    # Finalize cover letter content
    cover_letter_content = header_content + "\n" + body_with_spacing + footer_content

    # Output file
    output_file = os.path.join(output_dir, f"coverletter_{company_name}.tex")

    # Write the content to the .tex file
    with open(output_file, "w") as file:
        file.write(cover_letter_content)

    print(f"Cover letter for {ai_cover["company"]} has been built and saved to {output_file}")
    generate_pdf(output_dir, output_file)
    os.remove(output_file)

# Function to build a follow-up email
def build_follow_up_email(company_name, receiver_email):
    """Build a cover letter by interpolating role and company details."""

    # Read the job description from the placeholder file
    job_description_file = f"../job_description_placeholder.txt"
    follow_up_file = f"../followup_placeholder.json"
    if not os.path.exists(job_description_file):
        print(f"Error: {job_description_file} does not exist.")
        sys.exit(1)

    with open(job_description_file, "r") as file:
        job_description = file.read().strip()
    follow_up_email = build_follow_up_email_using_ai(job_description, receiver_email, f"../{company_name}/resume_{company_name}.pdf")
    print(follow_up_email)
    user_input = input("press y/n to continue: >")
    if user_input == "n":
        with open(follow_up_file, 'w') as json_file:
            json.dump(follow_up_email, json_file, indent=4)
        user_input = input("press enter to continue: >")
        with open(follow_up_file, "r") as file:
            follow_up_email = json.load(file)
    # TODO use mail apis
    Mailer.sender_email(receiver_email, f"../{company_name}/resume_{company_name}.pdf", follow_up_email["subject"], follow_up_email["body"])
        
    


def answer_questions(company_name):
    job_description_file = f"../job_description_placeholder.txt"
    if not os.path.exists(job_description_file):
            print(f"Error: {job_description_file} does not exist.")
            sys.exit(1)
    with open(job_description_file, "r") as file:
        job_description = file.read().strip()
    ai_builder = AIBuilder()
    ai_builder.initialize_llm()
    ai_builder.answer_questions(job_description, f"../{company_name}/resume_{company_name}.pdf")
    

# helper to build skills using AI
def build_skills_using_ai(job_description, skill_section, resume_path):
    ai_builder = AIBuilder()
    ai_builder.initialize_llm()
    return ai_builder.build_resume(job_description, skill_section, resume_path)

# helper to build cover letter using AI
def build_cover_using_ai(job_description, resume_path):
    ai_builder = AIBuilder()
    ai_builder.initialize_llm()
    return ai_builder.build_cover(job_description, resume_path)

# helper to build cover letter using AI
def build_follow_up_email_using_ai(job_description, receiver_mail, resume_path):
    ai_builder = AIBuilder()
    ai_builder.initialize_llm()
    return ai_builder.draft_follow_up_email(job_description, receiver_mail, resume_path)
# chat mode
def chat_mode(company_name):
    print(f"\nEntering conversation mode for {company_name}.\n")
    while True:
        print("\nWhat would you like to do? (Type 'exit' to quit)")
        print("1. Create a resume (y/n)")
        response = input("> ").strip().lower()
        if response == 'y':
            print("Enter resume type (common, technical, management):")
            resume_type = input("> ").strip().lower()
            if resume_type == "common":
                build_common_resume()
            elif resume_type in valid_resume_types:
                build_resume(resume_type, company_name)
            else:
                print("Invalid resume type.")
        
        print("2. Generate resume from existing data (y/n)")
        response = input("> ").strip().lower()
        if response == 'y':
            generate_from_existing(company_name)

        print("3. Build cover letter (y/n)")
        response = input("> ").strip().lower()
        if response == 'y':
            build_cover_letter(company_name)

        print("4. Answer Application Questions (y/n)")
        response = input("> ").strip().lower()
        if response == 'y':
            answer_questions(company_name)

        print("4. Follow-up email (y/n)")
        response = input("> ").strip().lower()
        if response == 'y':
            print("Enter receiver's email:")
            receiver_email = input("> ").strip()
            build_follow_up_email(company_name, receiver_email)

        print("5. Exit conversation mode? (y/n)")
        response = input("> ").strip().lower()
        if response == 'y':
            print(f"\nExiting conversation mode for {company_name}.\n")
            break

# Function to print help
def print_help():
    """Print usage instructions."""
    print("Usage:")
    print("  python builder.py create <resume_type> <company_name>  - Create a new resume and generate a PDF")
    print("  python builder.py generate <company_name>              - Generate a PDF from an existing LaTeX file")
    print("  python builder.py cover <company_name>                 - Create a cover letter for the specified company")
    print("  python builder.py followup <company_name>              - Create a follow-up email for the specified company")
    print("  python builder.py create common                        - Create common resumes for all types")
    print("  python builder.py help                                 - Show this help message")
    print("\nValid resume types are:")
    for valid_type in valid_resume_types:
        print(f" - {valid_type}")

def main():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    command = sys.argv[1].strip()

    if command == "chat":
        if len(sys.argv) != 3:
            print_help()
            sys.exit(1)
        company_name = sys.argv[2].strip()
        chat_mode(company_name)

    elif command == "generate":
        if len(sys.argv) != 3:
            print_help()
            sys.exit(1)
        company_name = sys.argv[2].strip()
        generate_from_existing(company_name)

    elif command == "cover":
        if len(sys.argv) != 3:
            print_help()
            sys.exit(1)
        company_name = sys.argv[2].strip()
        build_cover_letter(company_name)

    elif command == "qa":
        if len(sys.argv) != 3:
            print_help()
            sys.exit(1)
        company_name = sys.argv[2].strip()
        answer_questions(company_name)

    elif command == "followup":
        if len(sys.argv) != 4:
            print_help()
            sys.exit(1)
        company_name = sys.argv[2].strip()
        receiver_email = sys.argv[3].strip()
        build_follow_up_email(company_name, receiver_email)

    elif command == "create":
        if len(sys.argv) < 3:
            print_help()
            sys.exit(1)
        resume_type = sys.argv[2].strip()
        if(resume_type == "common"):
            build_common_resume()
            return
        company_name = sys.argv[3].strip()
        if resume_type not in valid_resume_types:
            print(f"Invalid resume type: {resume_type}")
            print_help()
            sys.exit(1)
        build_resume(resume_type, company_name)

    # elif command == "createt":
    #         company_name = sys.argv[3].strip()
    #         resume_type = sys.argv[2].strip()
    #         if resume_type not in valid_resume_types:
    #             print(f"Invalid resume type: {resume_type}")
    #             print_help()
    #             sys.exit(1)
    #         build_resume(resume_type, company_name)
    #         with concurrent.futures.ThreadPoolExecutor() as executor:
    #             future1 = executor.submit(build_resume(resume_type, company_name))
    #             future2 = executor.submit(build_cover_letter(company_name))
    #             return

    elif command == "help":
        print_help()
    else:
        print("Invalid command.")
        print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
