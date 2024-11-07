import requests 
import json
def get_text(responses):
    text = ""
    for response in responses.decode('utf-8', 'ignore').split("\n")[:-1]:
        try:
            nresponse = json.loads(response)
            text += nresponse.get('response', '')
        except json.JSONDecodeError as e:
            print("Error parsing JSON:", response, e)
    return text
        

url = "http://localhost:11434/api/generate"
headers = {'Content-Type': 'application/json'}
data = {'model': 'phi3', 'prompt': 'Why is the sky blue?', 'streaming': "False"}
response = requests.post(url, headers=headers, data=json.dumps(data))
if response.status_code == 200:
    print("Response:", get_text(response.content))
else:
    print("Error Occurred:", response.text)
