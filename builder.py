import os
import sys
import subprocess
import platform
from ai import AIBuilder

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

def build_resume(resume_type, company_name):
    """Build the resume by concatenating LaTeX files."""
    # Define the specific sections for the given resume type
    specific_sections = [
        f"skills_{resume_type}.tex",
        f"experience_{resume_type}.tex"
    ]

    # Create the output directory
    output_dir = os.path.join("..", company_name)
    
    # Clean the output directory if it exists
    if os.path.exists(output_dir):
        for filename in os.listdir(output_dir):
            file_path = os.path.join(output_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)

    # Create the output directory
    os.makedirs(output_dir, exist_ok=True)

    # Output file
    output_file = os.path.join(output_dir, f"resume_{company_name}.tex")
    placeholder_file = os.path.join(output_dir, f"cover_{company_name}.txt")

    # Start the LaTeX document
    resume_content = ""

    # Read and concatenate the contents of each section
    for section in ["design.tex","header.tex", "education.tex"] + specific_sections + ["certifications.tex"]:
        section_path = os.path.join(directory, section)
        if os.path.exists(section_path):
            with open(section_path, 'r') as file:
                resume_content += file.read() + "\n"
        else:
            print(f"Warning: {section_path} does not exist.")

    # End the LaTeX document
    resume_content += "\\end{document}\n"

    # Write the concatenated content to the output file
    with open(output_file, 'w') as file:
        file.write(resume_content)
    # Write the placeholder content to the cover letter placeholder
    with open(placeholder_file, "w") as file:
        file.write("Role: <role>\nCompany: <company>\n\n[Insert cover letter body here]")

    print(f"Resume for {resume_type} has been built and saved to {output_file}")

    # Generate the PDF file from the .tex file
    generate_pdf(output_dir, output_file)

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
    ai_builder = AIBuilder()
    ai_builder.initialize_llm()
    # Read the job description from the placeholder file
    job_description_file = f"../{company_name}/cover_{company_name}.txt"
    if not os.path.exists(job_description_file):
        print(f"Error: {job_description_file} does not exist.")
        sys.exit(1)

    with open(job_description_file, "r") as file:
        job_description = file.read().strip()
    ai_cover = ai_builder.build_cover(job_description, f"../{company_name}/resume_{company_name}.pdf")

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

# Function to print help

def print_help():
    """Print usage instructions."""
    print("Usage:")
    print("  python builder.py create <resume_type> <company_name>  - Create a new resume and generate a PDF")
    print("  python builder.py generate <company_name>              - Generate a PDF from an existing LaTeX file")
    print("  python builder.py help                                 - Show this help message")
    print("\nValid resume types are:")
    for valid_type in valid_resume_types:
        print(f" - {valid_type}")

def main():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    command = sys.argv[1].strip()

    if command == "generate":
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

    elif command == "create":
        if len(sys.argv) != 4:
            print_help()
            sys.exit(1)
        resume_type = sys.argv[2].strip()
        company_name = sys.argv[3].strip()
        if resume_type not in valid_resume_types:
            print(f"Invalid resume type: {resume_type}")
            print_help()
            sys.exit(1)
        build_resume(resume_type, company_name)
    elif command == "help":
        print_help()
    else:
        print("Invalid command.")
        print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
