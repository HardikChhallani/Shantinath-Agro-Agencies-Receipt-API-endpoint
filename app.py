from flask import Flask, request, send_file
import pdfkit
import os

# Path to wkhtmltopdf
path_to_wkhtmltopdf = '/usr/bin/wkhtmltopdf'
config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

options = {
    'page-size': 'A4',
    'margin-top': '0.25in',
    'margin-right': '0.25in',
    'margin-bottom': '0.25in',
    'margin-left': '0.25in',
    'encoding': "UTF-8",
    'no-outline': None
}

def replace_placeholders(template, data):
    for key, value in data.items():
        placeholder = '{{ ' + key + ' }}'
        if placeholder in template:
            print(f"Replacing {placeholder} with {value}")
            template = template.replace(placeholder, str(value))
        else:
            print(f"No placeholder for {key} in the template.")
    return template

def generate_receipts():
    try:
        data = request.json  # Ensure you are receiving JSON data
        if not data or "SAA_DATA" not in data:
            return {'error': 'No JSON data or SAA_DATA key received'}, 400

        # Get the PDF file name from the JSON data
        pdf_file_name = data.get("pdf_file_name", "receipts.pdf")  # Default to 'receipts.pdf' if not provided

        # Create a list to hold all the formatted HTML content
        combined_html = "<style>@media print {.page-break { page-break-before: always; }}</style>"

        # Iterate over the list of receipts
        for index, item in enumerate(data["SAA_DATA"]):
            # Path to the external HTML file
            html_file = os.path.join(os.getcwd(), 'templates', 'index.html')

            # Ensure the HTML file exists
            if not os.path.exists(html_file):
                return {'error': 'HTML template file not found'}, 404

            # Read the HTML content from the file
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()

            # Replace placeholders in the HTML with data from the JSON request
            html_formatted = replace_placeholders(html_content, item)

            # Append the formatted HTML and a page break
            combined_html +=  html_formatted
            if index < len(data["SAA_DATA"]) - 1:
                combined_html += '<div class="page-break"></div>'

        # Generate PDF from the combined HTML content
        pdf_file_path = pdf_file_name
        pdfkit.from_string(combined_html, pdf_file_path, configuration=config, options=options)

        # Send the combined PDF file as a response
        return send_file(pdf_file_path, as_attachment=True, download_name=pdf_file_name, mimetype='application/pdf')

    except Exception as e:
        return {'error': str(e)}, 400
