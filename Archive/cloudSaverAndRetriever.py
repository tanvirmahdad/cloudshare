
import boto3
from botocore.exceptions import NoCredentialsError
from botocore.exceptions import HTTPClientError


print("Welcome to Amazon S3 Tester")


#Step (a)

f=open("awskeys.txt","r")
lines=f.readlines()
ACCESS_KEY=lines[0].strip()
SECRET_KEY=lines[1].strip()
SESSION_TOKEN=lines[2].strip()
f.close()



#Step (b)

name = raw_input("Enter your name : ")

#step (C)

fwrite = open("name.txt","w+")
fwrite.write(name)
fwrite.close()


# Step (d)

s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY,
                      aws_session_token=SESSION_TOKEN)

try:
    s3.upload_file('name.txt', 'tanvirmahdad1', 'name.txt')
    print("File Upload Successful")
except IOError:
    print("The file was not found")
except NoCredentialsError:
    print("Credentials not available")
except HTTPClientError as e:
    print("Unexpected error: %s" % e)




# Step (e)

s3read = boto3.resource('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY,
                      aws_session_token=SESSION_TOKEN)

obj = s3read.Object('tanvirmahdad1', 'name.txt')
body = obj.get()['Body'].read()
print("The file content is: "+body)


#Step (f)

s3read.Object('tanvirmahdad1', 'name.txt').delete()

print("Uploaded file successfully deleted")






