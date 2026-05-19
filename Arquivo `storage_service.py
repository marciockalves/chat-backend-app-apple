import boto3
from botocore.client import Config
import os
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client('s3', config=Config(signature_version='s3v4'), 
                  region_name='us-east-1', 
                  aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), 
                  aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

def generate_presigned_url(bucket_name, object_name, expiration=3600):
    return s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': object_name}, ExpiresIn=expiration)
