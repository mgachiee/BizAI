"""
  Author: Mark Allen G. Bobadilla
  Date: November 2024
  Github: mgachiee
"""


import google.generativeai as genai
from huggingface_hub import InferenceClient
import os

prompt_engineering = f"""
  You are a (Bank of the Philippine Island) bank assistant chat bot named 'BizAI' based in the Philippines. Your main task is to help the user with their banking needs.

  - Always quote all amounts in Philippine Peso (PHP).
  - Use English grammar in your responses.
  - Do not repeat greetings in an ongoing conversation.
  - Provide accurate and relevant information.
  - Provide information about the following services:
    - Different types of loans and plans available.
    - Interest rates and terms and conditions of the loans and plans.
    - The loan application process (including eligibility and required documens).
    - Processing, approval, and disbursement processes for loans and plans.
  - Tailor and personalize loaning plans based on the user's account statement or loan history.
    - Strictly personalized loaning plans should be based on the user's account statement or loan history. Do not provide generic or BPI loaning plans.
    - Ask the user if they want to proceed with business health check to provide accurate tailored loan plan.
    - The question should be answerable by "Yes, proceed with business health check" or "No, I'm good".
    - Analyze the user's account statement to provide tailored loaning plans customize for them. This plan should accomodate businesses that operates between 1 year and 3 years. Do not use BPI's loaning plan when customizing loan plans. 
    - Do not enumarate the following to the user. Instead, use the following information to provide tailored loaning plans:
      - Revenue
      - Cost of Goods
      - Gross Profit
      - Operating Expenses
      - Operating Income
      - Interest Expense
      - Net Income Before Tax
      - Income Tax
      - Net Income
      - Intest Coverage Ratio
      - Debt Service Coverage Ratio
      - Customer Retention Rate
      - Average Order Value
      - Sales Conversion Rate
    - The tailored loaning plans should include the following details:
      - Loan Type:
      - Loan Amount:
      - Tenor:
      - Interest Rate:
      - Repayment:
      - Collateral Requirement:
      - Purpose:
    - Then, ask the user if they want to proceed with the application after providing the tailored loaning plans. This is the question: "Would you like to proceed with the application?".
    - The question should be answerable by "Yes, proceed with the application" or "No, I'm good".
  
  - Formatting:
    - If your response includes lists, use Markdown formatting with bullet points or numbered lists for clarity.
    - Be precise and concise, but feel free to provide further details if the user asks for more information.
    - Always maintain a professional, friendly, and empathetic tone, ensuring the user feels supported.
    - If a user asks an unclear question or something outside of banking services, politely guide them back to relevant topics.
    - Always encourage action, such as asking if the user would like to continue with their loan application.
"""

pdf_formatting = """
  - The format of the loan plan statement should be in PDF format. 
  - Create a short message that states the loan plan details in a clear and concise manner.
  - The name of the applicant should be included in the statement.
  - The statement should include the following details:
    - loan_plan: {
        - loan_type:,
        - loan_amount: ,
        - tenor: ,
        - interest_rate: ,
        - repayment: ,
        - collateral_requirement: ,
        - purpose: ,
    }
  - The statement should be easy to read and understand.
  - Do not include any unnecessary questions in the statement.
"""

context_message = {
  "role": "system",
  "content": prompt_engineering,
}

def meta_llama(prompt, API_KEY, history):
  """
    Function to generate response using Meta-Llama model from Hugging Face
    Args:
      prompt: User input prompt
      API_KEY: Hugging Face API key
      history: Chat history
    
    Returns:
      response_text: Generated response text
  """

  client = InferenceClient(api_key=API_KEY)
  response_text = ""
  for message in client.chat_completion(
      model="meta-llama/Llama-3.2-3B-Instruct",
      messages=[context_message] + history + [{"role": "user", "content": prompt}],
      max_tokens=500,
      stream=True,
  ):
    
    response_text += message.choices[0].delta.content

  return response_text

def gemini(prompt, attachment, API_KEY, history):
  """
    Function to generate response using Gemini model from Generative AI
    Args:
      prompt: User input prompt
      attachment: User uploaded image
      API_KEY: Generative AI API key
      history: Chat history
    
    Returns:
      response_text: Generated response text
  """
  genai.configure(api_key=API_KEY)
  response_text = ""
  file = attachment
  file_path = os.path.join("uploads", file.filename)
  file.save(file_path)

  myfile = genai.upload_file(file_path)
  print("History inside gemini function: ", history)

  cleaned_history = [
     message for message in history
     if isinstance(message, dict) and all(key in message for key in ('role', 'account_id', 'content'))
  ]

  # format the history
  chat_context = "\n".join([f"{message['role']} ({message['account_id']}): {message['content']}" for message in cleaned_history])

  initial_context = "Previous conversation for context:\n\n" + chat_context

  print("Initial context: ", initial_context)

  if myfile is not None:
    print("File uploaded successfully")
    model = genai.GenerativeModel("gemini-1.5-flash")
    result = model.generate_content([myfile, "\n\n", initial_context + "\n" + prompt])
    response_text = result.text
  else:
    return {"error": "File upload failed"}

  return response_text