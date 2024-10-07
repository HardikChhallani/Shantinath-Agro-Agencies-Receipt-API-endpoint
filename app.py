from application import *
from flask import Flask, request, send_file
import pdfkit
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "Hello, World!"

@app.route('/generate-SAA-receipt-pdf', methods=['GET'])
def return_pdf():
    return generate_receipts()

if __name__ == '__main__':
    app.run(debug=True)
