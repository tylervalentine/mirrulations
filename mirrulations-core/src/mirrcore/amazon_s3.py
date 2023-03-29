import os
from dotenv import load_dotenv
import boto3
import json

class AmazonS3:

    def __init__(self, api_key):
        # Not sure if this is the way to go about this 
        load_dotenv()
        self.access_key = os.getenv("AWS_ACCESS_KEY")
        self.secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.s3_client = self.establish_connection_to_s3()
    
    def establish_connection_to_s3(self):
        s3_client = boto3.client(
                's3', 
                region_name='us-east-1',
                aws_access_key_id=self.access_key, 
                aws_secret_access_key = self.secret_access_key
                )
        return s3_client
    
    def put_text_s3(self, bucket, path, data):
        self.s3_client.put_object(
            Bucket=bucket, 
            Key=path, 
            Body=json.dumps(data)
            )
        return True
    
    def put_binary_s3(self, bucket, path, data):
        self.s3_client.put_object(
            Bucket=bucket, 
            Key=path, 
            Body=data)
        return True 
