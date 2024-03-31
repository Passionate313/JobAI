import pdfkit
from jinja2 import Environment, FileSystemLoader

from src.resume.models import Resume
from src.resume.utils import map_resume_to_builder_pattern, convert_first_page_to_image


def build_resume(id: str, data: Resume, resume_template_id: str = None):
    """Build resume with given resume data and resume template"""

    # Define resume_template_id
    if resume_template_id is None:
        resume_template_id = "64dbb0370a009cc26e1ed49e"

    # map resume to builder pattern
    data = map_resume_to_builder_pattern(data)

    # Define the templates path
    file_loader = FileSystemLoader('src/resume_template/templates')

    # Initialize Jinja2 environment
    env = Environment(loader=file_loader)

    # Load the templates file
    template = env.get_template(f'{resume_template_id}.html')

    # Render the templates with data
    output = template.render(data)

    # Write to a file
    with open(f"files/{id}.html", "w", encoding='utf-8') as fh:
        fh.write(output)
    with open(f"files/{id}-{resume_template_id}.html", "w", encoding='utf-8') as fh:
        fh.write(output)

    # define file paths (make sure to use raw strings or double backslashes)
    html_path = f'files/{id}.html'
    output_path = f'files/{id}.pdf'
    output_path_with_template = f'files/{id}-{resume_template_id}.pdf'

    # Use the function 'from_file' to convert the HTML file to a PDF
    # If you have a css file, use the option 'css'. You can also include multiple css files
    pdfkit.from_file(html_path, output_path)
    pdfkit.from_file(html_path, output_path_with_template)

    # Gets the image of first page of pdf for thumbnail
    convert_first_page_to_image(id)
    convert_first_page_to_image(f"{id}-{resume_template_id}")

    return f"{id}.pdf"
