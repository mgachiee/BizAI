# BizAI: The Future of Loaning Support for MSMEs

Micro, Small, and Medium Enterprises (MSMEs) frequently face difficulties accessing loans due to limited financial history and perceived risk by lenders. This paper proposes a GenAI-powered chatbot to address these challenges by providing tailored insights into loan options, financial planning, and cash flow management. Built on Azure’s AI infrastructure, this chatbot offers interactive assistance for loan eligibility, automated documentation, and personalized advice, aiming to improve loan accessibility and enhance financial literacy. With measurable impacts on loan accessibility, interest rates, and revenue growth, this solution supports MSME growth, thereby contributing to economic development.

## Snapshot of the prototype

![BizAI Snapshot](https://scontent.fmnl34-1.fna.fbcdn.net/v/t39.30808-6/468326696_122117166116576075_3910117658229457964_n.jpg?_nc_cat=106&ccb=1-7&_nc_sid=127cfc&_nc_eui2=AeGQ3_oFmXLngrACj8y0QlvEHwckyQPd6lsfByTJA93qW3uC0cUzBPuia5qrIA23hTjLF_m1drcTBdVC-0zS1PAV&_nc_ohc=79LXZEvmwwcQ7kNvgG8DTdJ&_nc_zt=23&_nc_ht=scontent.fmnl34-1.fna&_nc_gid=ApHaJeESlf_AwE1WpE6wMfW&oh=00_AYD1BiusQiVYHujZrRC4iYyOJ7K0qa94RR8_-8ChBH945w&oe=675038F7)

## Installation and Usage

_Reminder: This is a fast-paced development, and the app will run on a browser. The app's UI only works for mobile phones like the **iPhone XR**, **iPhone 14 Pro Max**, **Samsung Galaxy S20 Ultra**, and other devices with same dimensions as the mentioned devices._

1. Create your project directory.
    
    - ```npm create vite@latest react-project-name```
  
2. Install modules and packages.

   - Click the green button ```Code``` then ```Download ZIP```.
   - ```npm install```
   - ```npm install axios react-markdown remark-gfm```
   - ```pip install Flask flask-cors python-dotenv requests openai markdown pdfkit```
   - For windows click the link: [wkhtmltopdf installer](https://wkhtmltopdf.org/downloads.html) or ```sudo apt-get install wkhtmltopdf```

3. Prepare environment variables.

   ```
    LLAMA_API_KEY="<API_KEY_HERE>"
    GEMINI_API_KEY="<API_KEY_HERE>"
    ENDPOINT_URL="<URL_HERE>"
    DEPLOYMENT_NAME="<MODEL_NAME>"
    SEARCH_ENDPOINT="<SEARCH_ENDPOINT_URL>"
    SEARCH_KEY="<SEARCH_KEY>"
    SUBSCRIPTION_KEY="<SUBSCRIPTION_KEY>"
    LOAN_BLOB_URL="<BLOB_STORAGE_URL_FOR_DUMMY_DATA>"
    ACC_STATEMENT_BLOB_URL="<BLOB_STORAGE_URL_FOR_DUMMY_DATA>"
   ```

4. Run locally.

   - **project-name/src** ```npm run dev```
   - **project-name/src/backend/main.py** file ```python main.py```

## Privacy and License

This prototype does not collect any personal data from the users. However, during the use of this app, certain user interactions (e.g., inputs for test prompts, account information, etc.) may be temporarily stored for demonstration purposes only. No real banking data or sensitive information is collected, stored, or processed.

- __User Inputs:__ Any input provided by users, such as dummy account details or transaction information, is only used within the app session and is not stored long-term or shared with any third-party services.
- __Security:__ Since this is a prototype, security measures such as encryption or secure transaction processing are not implemented. This app is intended solely for demonstration and educational purposes.

Feel free to check its [LICENSE](https://github.com/mgachiee/BizAI/blob/main/LICENSE) under [MIT License](https://choosealicense.com/licenses/mit/).

## Acknowledgements

We would like to express our gratitude to the following individuals, libraries, and resources for their contributions and support during the development of this prototype bank app:

### Libraries and Tools:

- Flask – A lightweight web framework for Python used to build this app.
- React – A JavaScript library for building user interfaces that was used in the frontend of this app.
- OpenAI – Used for generating AI-driven responses and interactions within the app.
- Python-dotenv – A Python library for managing environment variables used to configure the app securely.
- PDFKit – A tool for generating PDF reports and documents in the app.

### Services and Platforms
- Azure Services – Used for cloud hosting, AI models, and other services essential for the app’s backend, such as Azure OpenAI and Azure Cognitive Services.
- Hugging Face – Used for natural language processing models and AI-powered features within the app.

### Resources
- Flaticon – Used for providing high-quality, customizable icons to enhance the user interface.

### Special Thanks:

- BizAI Team:  For conceptualizing and developing the prototype bank app.
- Mentor: We were so hooked on the event that we forgot to ask his name. But thank you for sharing your expertise and ideas for our solution.

### BizAI Team:

<div style="display: flex;  gap: 10px; flex-direction: column;">
    <div style = "display: flex; align-items: center; gap: 10px;">
        <a href="https://github.com/Jaushi" target="_blank">
            <img src="https://avatars.githubusercontent.com/u/144474840" alt="Jaushi Github Icon" style="border-radius: 50%; width: 40px; height: 40px;">
        </a>
        <p>Researcher | Pitcher:</br> <a href="https://www.linkedin.com/in/joshuapagallaman/" target="_blank">Joshua Allan Pagallaman</a></p>
    </div>
    <div style = "display: flex;align-items: center; gap: 10px;">
        <a href="https://github.com/aint-vscp" target="_blank">
            <img src="https://avatars.githubusercontent.com/u/136457226" alt="aint-vscp Github Icon" style="border-radius: 50%; width: 40px; height: 40px;">
        </a>
        <p>System Architect | Backend Developer:</br> <a href="https://www.linkedin.com/in/vash-puno/" target="_blank">Vash Puno</a></p>
    </div>
    <div style = "display: flex;align-items: center; gap: 10px;">
        <a href="https://github.com/mgachiee" target="_blank">
            <img src="https://avatars.githubusercontent.com/u/119985091" alt="mgachiee Github Icon" style="border-radius: 50%; width: 40px; height: 40px;">
        </a>
        <p>Frontend | Backend Developer:</br> <a href="https://www.linkedin.com/in/markallenbobadilla/" target="_blank">Mark Allen Bobadilla</a></p>
    </div>
    <div style = "display: flex;align-items: center; gap: 10px;">
        <a href="https://www.linkedin.com/in/christinejoie/" target="_blank">
            <img src="https://media.licdn.com/dms/image/v2/D5603AQFI30K8u9fRsw/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1721997056083?e=1738195200&v=beta&t=xQvle4K8ZlR1NgNrK3ndHarazSiyVVOO9KWxmgqyoMM" alt="Christine LinkedIn Photo" style="border-radius: 50%; width: 40px; height: 40px;">
        </a>
        <p>UI/UX Designer:</br> <a href="https://www.linkedin.com/in/christinejoie/" target="_blank">Christine Joie Calapati</a></p>
    </div>
</div>
