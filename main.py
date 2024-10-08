from app import *
from flask import Flask

# Initialize Flask app
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "Hello, World!"

@app.route('/generate-SAA-receipt-pdf', methods=['POST'])
def return_pdf():
    return generate_receipts()

if __name__ == '__main__':
    # Ensure the app listens on 0.0.0.0 inside Docker
    app.run(host='0.0.0.0', port=5000)
