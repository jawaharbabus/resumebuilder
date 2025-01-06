import os
import sys
import subprocess
import platform
from time import sleep

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
valid_resume_types = {"backend", "frontend", "fullstack", "javascript", "python", "java", "general"}

def generate_pdf(output_dir, tex_file):
    """Generate PDF from .tex file and clean up auxiliary files."""
    if platform.system() == "Linux":
        subprocess.run(["pdflatex", "-output-directory", output_dir, tex_file], check=True)
    elif platform.system() == "Windows":
        print("PDF generation is not supported on Windows in this script.")
        return

    # Clean up the directory by removing all files except .tex and .pdf
    for filename in os.listdir(output_dir):
        if not (filename.endswith(".tex") or filename.endswith(".pdf")):
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