"""
    Authors: 
        - Vash C. Puno
        - Mark Allen G. Bobadilla
    Date: November 2024
    Github: 
        - aint-vscp
        - mgachiee
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os, json, csv, requests, io
import models
from openai import AzureOpenAI
import markdown
import pdfkit
from pdfkit.configuration import Configuration
from datetime import datetime
import base64

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": f"http://<localhost>:5000"}}) # set the allowed origins

PDF_SAVE_PATH = os.path.join(os.getcwd(), 'generated_pdf')  # set the path to save the generated PDF files
os.makedirs(PDF_SAVE_PATH, exist_ok=True)  # create the directory if it doesn't exist

load_dotenv() # load environment variables

# for generating loan statements
def generate_pdf(response_text, output_path):
    """
    For generating Loan Statements in PDF file format based on the given response text 
    and save it to the output path.

    Args:
    - response_text (str): The model's response text to be converted to PDF.
    - output_path (str): The path to save the generated PDF file.

    Returns:
    - file_url (str): The URL to download the generated PDF file.

    Prints:
    - Status message for the PDF generation process.
    
    """

    # convert the response text to HTML content
    html_content = markdown.markdown(response_text)
    header_img_path = "C:/Users/Mark/Desktop/BizAI-Development/src/assets/BizAI-Logo.png"

    with open(header_img_path, "rb") as img_file:
        base64_img = base64.b64encode(img_file.read()).decode('utf-8')
    
    header_image_url = f"data:image/png;base64,{base64_img}"
    html_template = f"""
        <!DOCTYPE html><!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Loan Plan Statement</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
            }}
            header {{
                display: flex;
                justify-content: center;
                align-items: center;
                width: 1000px;
                height: 4.5rem;
                max-height: 4.5rem;
                background-color: #500000;
            }}
            header img {{
                width: 150px;
                height: auto;
            }}
        </style>
        </head>
        <body>
            <header>
                <img src="{header_image_url}" alt="BizAI Logo">
            </header>
            {html_content}
        </body>
        </html>
    """

    wkhtmltopdf_path = r"C:\\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"  # set the path to wkhtmltopdf
    config = Configuration(wkhtmltopdf=wkhtmltopdf_path)

    # check if the output directory exists, if not create it
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # generate the PDF file
    try:
        pdfkit.from_string(html_template, output_path, configuration=config)
        print(f"PDF file generated successfully at: {output_path}")
        pdf_filename = os.path.basename(output_path)
        file_url = f'http://<localhost>:5000/download-pdf/{pdf_filename}'
        return file_url
    except Exception as e:
        # return an error message if the PDF generation fails
        print(f"Error generating PDF: {e}")
    

# load Azure Blob Storage URL
loan_blob_url = os.getenv('LOAN_BLOB_URL')

# route for downloading the generated PDF file
@app.route('/download-pdf/<path:filename>')
def download_pdf(filename):
    return send_from_directory(PDF_SAVE_PATH, filename, as_attachment=True)

# route for general prompts
@app.route('/generate', methods=['POST'])
def generate():
    # initialize variables
    prompt = ''
    history = []
    customer_id = request.get_json().get('customer_id', None)

    # check if attachment is provided
    attachment = request.files.get('attachment')

    # set the prompt and history based on the request type
    if attachment is not None:
        # handle multipart/form-data
        prompt = request.form.get('prompt')
        history = json.loads(request.form.get('history', '[]'))
    else:
        # handle json
        data = request.get_json()
        prompt = data.get('prompt', '')
        history = data.get('history', [])

    # check if prompt is provided
    if prompt is None:
        return jsonify({"error": "Prompt is required"}), 400
    
    response_text = "" # initialize response text

    if attachment is None:
        # declare and initialize variables
        fetched_data = None
        response_obj = None
        
        # check if prompt is related to business health check
        if prompt == 'User: Yes, proceed with business health check.':
            # get data from Azure Blob Storage
            fetched_data = get_account_statement(customer_id)
            # store the response object
            response_obj = fetched_data[0]
        # if not related to business health check, directly use llama
        else:
            # using Llama API
            response_text = models.meta_llama(prompt, os.getenv('LLAMA_API_KEY'), history)
        
        # convert the response object to JSON
        contents_data = json.dumps(response_obj, indent=2)

        # check if response object is not None
        if response_obj is not None:
            try:
                # generate an insight for business health check
                # using Llama API
                response_text = models.meta_llama("Generate an insight for business health check based on the following data:\n" + contents_data, os.getenv('LLAMA_API_KEY'), history)
                return jsonify({'response': response_text})
            except Exception as e:
                return jsonify({"error": str(e)}), 500
    
    # check if attachment is provided
    if attachment is not None:
        # using Llama and Gemini API

        # extract text/values from the image
        extracted_text = models.gemini(
            'Extract the values from this image. And make sure it is formattable by markdown.',
            attachment,
            os.getenv("GEMINI_API_KEY"),
            history
        )

        # generate an insight based on the extracted text
        response_text = models.meta_llama(
            f"{prompt} {extracted_text}",
            os.getenv("LLAMA_API_KEY"),
            history
        )

    # return the response text to the frontend
    return jsonify({'response': response_text})

# load necessary env variables for Azure Cognitive Search and OpenAI
endpoint = os.getenv("ENDPOINT_URL")
deployment = os.getenv("DEPLOYMENT_NAME")
search_endpoint = os.getenv("SEARCH_ENDPOINT")
search_key = os.getenv("SEARCH_KEY")
subscription_key = os.getenv("SUBSCRIPTION_KEY")

# Check if all keys are loaded successfully
if (endpoint and deployment and search_endpoint and search_key and subscription_key) is not None:
  print('Loaded Azure keys successfully')

# Initialize Azure OpenAI client with key-based authentication
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2024-05-01-preview",
)

# Query Azure Cognitive Search
def search_azure(query, history):
    search_url = f"{search_endpoint}indexes/nifty-heart-plj5d75ssw/docs/search?api-version=2021-04-30-Preview"
    headers = {
        "Content-Type": "application/json",
        "api-key": search_key,
    }
    search_payload = {
        "search": query + "\n" + "\n".join(history), #include history in the search query
        "top": 10,
        "queryType": "simple"
    }

    try:
        response = requests.post(search_url, headers=headers, json=search_payload)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"Error querying Azure Search: {e}")
        return {"error": str(e)}, 500  # Return a 500 error with the error message


@app.route('/bpi', methods=['POST'])
def generate_azure():
    # get the prompt and file from the request
    prompt = request.get_json().get('query', None)
    file = request.files.get('attachment')
    history = [] # Initialize history

    # check if history is provided
    history = json.loads(request.form.get('history', '[]'))
    response_obj = None

    # integrating Azure Blob Storage with Azure Cognitive Search
    if prompt == 'User: Yes, proceed with business health check.':
        # using Azure Blob Storage
        customer_id = request.get_json().get('customer_id', None)
        fetched_data = get_account_statement(customer_id)
        response_obj = fetched_data[0]

        if hasattr(response_obj, 'get_json'):
            try:
                contents_data = json.dumps(response_obj.get_json(), indent=2)
            except Exception as e:
                print(f"Error fetching data from blob storage: {e}")
                contents_data = response_obj.data.decode('utf-8')
        else:
            contents_data = response_obj
        
        contents_data_str = json.dumps(contents_data) if isinstance(contents_data, dict) else str(contents_data)

        # print(f"Fetching data from blob storage: {contents_data}")
        query = f"Generate an insight for business health check based on the following data:\n{contents_data_str}"

    elif prompt == "User: Yes, proceed with loaning application.":
        customer_id = request.get_json().get('customer_id', None)
        fetched_data = get_account_statement(customer_id)
        response_obj = fetched_data[0]
        contents_data = json.dumps(response_obj, indent=2)
        print(f"Fetching data from blob storage: {contents_data}")
        query = f"Create a content for the PDF file based on the previous chats, get the details of generated tailored loan plan and follow this format {models.pdf_formatting} and get the firstname and lastname from this data:\n{contents_data}"

    # Check if the file and prompt are provided
    elif file and prompt:
      # using Gemini API and Azure Cognitive Search   
      azure_extracted_text = models.gemini(prompt + ' extract the values from the image and generate an insight that is related to bank services.', file, os.getenv('GEMINI_API_KEY'))
      query = azure_extracted_text
    
    # if the file is not provided, use the prompt as the query
    else:
      # using Azure Cognitive Search  
      data = request.get_json()
      query = data.get('query')
    
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400 # Return a 400 error if the query is not provided

    # Search for relevant information
    search_results = search_azure(query, history)
    if isinstance(search_results, tuple):  # Check if an error was returned
        return jsonify({"error": search_results[0]["error"]}), search_results[1]

    # Extract content from search results
    search_texts = "\n".join([doc.get("content", "No content available.") for doc in search_results.get("value", [])])
    
    # Create chat prompt for Azure OpenAI
    chat_prompt = [
        {
            "role": "system",
            "content": models.prompt_engineering
        },
        {
            "role": "user",
            "content": query
        },
        {
            "role": "system",
            "content": f"Relevant information from Azure Search:\n{search_texts or 'No relevant information found.'}"
        }
    ]

    # Generate a response using Azure OpenAI
    try:
        completion = client.chat.completions.create(
            model=deployment,
            messages=chat_prompt,
            max_tokens=800,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
        )
        # Access the content using dot notation
        response_text = completion.choices[0].message.content if completion.choices else "No response generated."
    except Exception as e:
        print(f"Error generating completion: {e}")
        return jsonify({"error": f"Failed to generate completion: {str(e)}"}), 500

    if prompt == "User: Yes, proceed with loaning application.":
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_pdf_path = os.path.join(os.getcwd(), "generated_pdf", f"loan_application_{current_time}_{customer_id}.pdf")
        file_url = generate_pdf(response_text, output_pdf_path)
        return jsonify({"response": response_text, "file_url": file_url})
    
    return jsonify({"response": response_text})

# load necessary env variables for Azure Blob Storage
business_statements = os.getenv('ACC_STATEMENT_BLOB_URL')

def get_account_statement(customer_id):
    # customer_id = request.args.get('customer_id')
    
    print(f"\n\nCustomer ID: {customer_id}\n\n")
    if not customer_id:
        return jsonify({"error": "customer_id is required"}), 400
    
    try:
        response = requests.get(business_statements)
        
        if response.status_code == 200:
            csv_file = io.StringIO(response.content.decode('utf-8'))
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            
            statements_data = [row for row in csv_reader if row['CUSTOMER_ID'] == customer_id]
            
            if statements_data:
                return statements_data
            else:
                return jsonify({"message": "No ADB data found for the given customer_id"}), 404
        
        else:
            return jsonify({"error": "Failed to retrieve the file"}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# currently not working
# def get_loan_by_customer(customer_id):
#     # customer_id = request.args.get('customer_id')
    
#     if not customer_id:
#         return jsonify({"error": "customer_id is required"}), 400
    
#     try:
#         # Fetch the CSV file from Azure Blob Storage
#         response = requests.get(loan_blob_url)
        
#         # Check if the request was successful
#         if response.status_code == 200:
#             csv_file = io.StringIO(response.content.decode('utf-8'))
#             csv_reader = csv.DictReader(csv_file, delimiter=',')  # Changed to comma
            
#             # Filter rows by customer_id
#             loans_data = [row for row in csv_reader if row['CUSTOMER_ID'] == customer_id]
            
#             if loans_data:
#                 return jsonify(loans_data)
#             else:
#                 return jsonify({"message": "No loans found for the given customer_id"}), 404
        
#         else:
#             return jsonify({"error": "Failed to retrieve the file"}), response.status_code

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)