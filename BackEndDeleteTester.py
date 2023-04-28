import requests
import json

url='https://c5plwiyi3e.execute-api.us-east-1.amazonaws.com/Beta/fileUpload'

raw_data='{"Bucket": "tanvirmahdad1","key": "s2.txt"}'

response=requests.post(url, data=raw_data)

body=json.loads(response.content)

#print(body['presigned_url']['fields'])

demoURL=body['presigned_url']['url']
demoField=body['presigned_url']['fields']

print(body)


fin=open('/Users/tanvirmahdad/summer2020/cloudComputing/projects/s2.txt','rb')
files={'file': fin}

try:

    r=requests.post(demoURL,data=demoField,files=files)
    print(r.content)

finally:
    fin.close()



