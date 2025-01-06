import os
import sys

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

# Function to build the resume
def build_resume(resume_type, company_name):
    # Define the specific sections for the given resume type
    specific_sections = [
        f"skills_{resume_type}.tex",
        f"experience_{resume_type}.tex"
    ]

    # Create the output directory
    output_dir = os.path.join("..", company_name)
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

    # Create an additional text file in the output directory
    additional_file_path = os.path.join(output_dir, "additional_info.txt")
    with open(additional_file_path, 'w') as file:
        file.write(f"This directory contains the resume for {company_name}.\n")

    print(f"Resume for {resume_type} has been built and saved to {output_file}")
    print(f"Additional information file has been created at {additional_file_path}")

# Main function to handle command line arguments
def main():
    if len(sys.argv) != 3:
        print("Usage: python builder.py <resume_type> <company_name>")
        sys.exit(1)

    resume_type = sys.argv[1]
    company_name = sys.argv[2]
    if resume_type not in valid_resume_types:
        print(f"Invalid resume type: {resume_type}")
        print("Valid resume types are:")
        for valid_type in valid_resume_types:
            print(f" - {valid_type}")
        sys.exit(1)

    build_resume(resume_type, company_name)

if __name__ == "__main__":
    main()