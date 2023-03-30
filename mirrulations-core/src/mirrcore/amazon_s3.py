import os
from dotenv import load_dotenv
import boto3
import json


class AmazonS3:

    def __init__(self, bucket_name):
        # Not sure if this is the way to go about this
        load_dotenv()
        self.access_key = os.getenv("AWS_ACCESS_KEY")
        self.secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.s3_client = boto3.client(
                's3',
                region_name='us-east-1',
                # aws_access_key_id=self.access_key,
                # aws_secret_access_key=self.secret_access_key
                )
        self.bucket_name = bucket_name

    def get_s3_client(self):
        return self.s3_client

    def put_text_s3(self, path, data):
        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=path,
            Body=json.dumps(data)
            )

    def put_binary_s3(self, path, data):
        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=path,
            Body=data)
