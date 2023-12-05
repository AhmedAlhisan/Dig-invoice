# Dig Invoice

A website and a financial solution for automating the extraction of information from invoices using OCR technology .

## Description

 The project fully functions to display related information for each department with its complete expenses and budget. The website also provides financial reports and recommendations suitable for providing solutions and financial advice.
## Getting Started

### Dependencies

- Python - Django
- Windows

### Installing

- How to install Dig Invoices:
- create a vrtuale enviroment (VENV)
- clone from GitHub
- pip install (absl-py==2.0.0
aiohttp==3.9.1
aiosignal==1.3.1
annotated-types==0.6.0
anyio==3.7.1
asgiref==3.7.2
astunparse==1.6.3
attrs==23.1.0
cachetools==5.3.2
certifi==2023.11.17
charset-normalizer==3.3.2
colorama==0.4.6
dataclasses-json==0.6.3
distro==1.8.0
Django==4.2.7
filelock==3.13.1
flatbuffers==23.5.26
frozenlist==1.4.0
fsspec==2023.10.0
gast==0.5.4
google-auth==2.23.4
google-auth-oauthlib==1.1.0
google-pasta==0.2.0
greenlet==3.0.1
grpcio==1.59.3
h11==0.14.0
h5py==3.10.0
httpcore==1.0.2
httpx==0.25.2
huggingface-hub==0.19.4
idna==3.6
Jinja2==3.1.2
jsonpatch==1.33
jsonpointer==2.4
keras==2.15.0
langchain==0.0.344
langchain-core==0.0.8
langsmith==0.0.68
libclang==16.0.6
Markdown==3.5.1
MarkupSafe==2.1.3
marshmallow==3.20.1
ml-dtypes==0.2.0
mpmath==1.3.0
multidict==6.0.4
mypy-extensions==1.0.0
networkx==3.2.1
numpy==1.26.2
oauthlib==3.2.2
openai==0.28.0
opt-einsum==3.3.0
packaging==23.2
pandas==2.1.3
pdf2image==1.16.3
Pillow==10.1.0
protobuf==4.23.4
pyasn1==0.5.1
pyasn1-modules==0.3.0
pydantic==2.5.2
pydantic_core==2.14.5
PyMuPDF==1.23.6
PyMuPDFb==1.23.6
PyPDF2==3.0.1
pytesseract==0.3.10
python-dateutil==2.8.2
pytz==2023.3.post1
PyYAML==6.0.1
regex==2023.10.3
requests==2.31.0
requests-oauthlib==1.3.1
rsa==4.9
safetensors==0.4.0
six==1.16.0
sniffio==1.3.0
SQLAlchemy==2.0.23
sqlparse==0.4.4
sympy==1.12
tenacity==8.2.3
tensorboard==2.15.1
tensorboard-data-server==0.7.2
tensorflow==2.15.0
tensorflow-estimator==2.15.0
tensorflow-intel==2.15.0
tensorflow-io-gcs-filesystem==0.31.0
termcolor==2.3.0
tokenizers==0.15.0
torch==2.1.1
tqdm==4.66.1
transformers==4.35.2
typing-inspect==0.9.0
typing_extensions==4.8.0
tzdata==2023.3
urllib3==2.1.0
Werkzeug==3.0.1
wrapt==1.14.1
yarl==1.9.3 )
- alsow you have to install both Tessract Ocr & Poppler in your windows. 

### Executing program

- make migration & migrate for dataBase .
- finnaly , python manage.py runserver

## Usage

- How to use Dig invoices.
- from mnue select Demo and try to upload invoices from nipco , images & pdf are acceptable .
- check if the extracted information meet the original invoice , confirm to save , cancel to go back .
- check the dashboard from mune , first section is provide each department and count of there invoices , and some detailes about type of these invoices.
- second section is provide a pie chart using CHARTjs to calculate spending vs. avialible budget .
- thierd section to visualize the data set for departments spending in each month , and the distribution for departments spending
- last section to Genrate a Financial Recommendations For All Department using OpinAi , and to understand the pattern for each department.   






## Project Status

-  In development.
