import os
import json
from dotenv import load_dotenv
import boto3
import sys


class AmazonS3:

    def __init__(self):
        self.get_credentials()
        self.access_key = None
        self.secret_access_key = None
        self.s3_client = self.get_S3_client()
        

    def get_S3_client(self):
        if self.get_credentials() is False:
            print("No credentials provided, Unable to connect to S3")
        try:
            return boto3.client(
                    's3',
                    region_name='us-east-1',
                    aws_access_key_id=self.access_key,
                    aws_secret_access_key=self.secret_access_key
                    )
        except:
            print("AWS credentials provided were not valid.")

    def get_credentials(self):
        load_dotenv()
        self.access_key = os.getenv("AWS_ACCESS_KEY")
        self.secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        return (self.access_key is not None and 
                self.secret_access_key is not None)
        

    def put_text_s3(self, bucket_name, path, data):
        return self.s3_client.put_object(
            Bucket=bucket_name,
            Key=path,
            Body=json.dumps(data)
            )

    def put_binary_s3(self, bucket_name, path, data):
        return self.s3_client.put_object(
            Bucket=bucket_name,
            Key=path,
            Body=data)
