import requests
import json

url='https://jdj3xxcrk9.execute-api.us-east-1.amazonaws.com/default/folderUpload'

raw_data='{"Bucket": "tanvirmahdad1","key": "testFolder"}'

response=requests.post(url, data=raw_data)

body=json.loads(response.content)

#print(body['presigned_url']['fields'])

demoURL = body['presigned_url']

print(body)


fin=open('/Users/tanvirmahdad/summer2020/cloudComputing/projects/s2.txt','rb')
files={'file': fin}
data = {'dir':'testFolder', 'submit':'Submit'}

try:
    #print("Test")
    r=requests.post(demoURL,data=data)
    print(r.content)

finally:
    fin.close()



