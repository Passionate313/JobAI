import json
import requests
from starlette import status

from src.config import API_LAYER_KEY, EDEN_AI_API_KEY
from src.resume.utils import map_parsed_result_to_resume


# Uses API Layer resume parser service
def parse_resume_by_api_layer(resume_name: str):
    url = 'https://api.apilayer.com/resume_parser/upload'
    headers = {
        'Content-Type': 'application/octet-stream',
        'apikey': API_LAYER_KEY
    }
    data = open(f"files/{resume_name}", 'rb', encoding='utf-8').read()

    response = requests.post(url, headers=headers, data=data)

    return response


# Uses Eden AI resume parser service
def parse_resume_by_eden_ai(resume_name: str):
    headers = {"Authorization": f"Bearer {EDEN_AI_API_KEY}"}

    url = "https://api.edenai.run/v2/ocr/resume_parser"
    data = {"providers": "affinda"}
    files = {'file': open(f"files/{resume_name}", 'rb')}

    response = requests.post(url, data=data, files=files, headers=headers)

    if response.status_code != status.HTTP_200_OK:
        return response.status_code, response.text
    else:
        result = json.loads(response.text)
        data = map_parsed_result_to_resume(result["affinda"]["extracted_data"])
        return status.HTTP_200_OK, data
