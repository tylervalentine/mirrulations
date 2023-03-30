import boto3
from moto import mock_s3
# import pytest
# from botocore.exceptions import ClientError
# from mirrclient.saver import Saver
from mirrcore.amazon_s3 import AmazonS3
# import os


@staticmethod
def create_mock_mirrulations_bucket():
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="test-mirrulations1")
    return conn


@mock_s3
def test_put_text_to_bucket():
    conn = create_mock_mirrulations_bucket()
    s3_bucket = AmazonS3(bucket_name="test-mirrulations1")
    test_data = {
        "data": "test"
    }
    test_path = "data/test"
    response = s3_bucket.put_text_s3(test_path, test_data)
    body = conn.Object("test-mirrulations1", "data/test").get()["Body"] \
                                                         .read() \
                                                         .decode("utf-8")
    assert body == '{"data": "test"}'
    assert response["ResponseMetadata"]['HTTPStatusCode'] == 200


@mock_s3
def test_put_binary_to_bucket():
    conn = create_mock_mirrulations_bucket()
    s3_bucket = AmazonS3(bucket_name="test-mirrulations1")
    test_binary_path = "/Users/jack11wagner/Courses/334/mirrulations/" + \
                       "mirrulations-core/tests/test-mirrulations-pdf.pdf"
    test_path = "data/test"
    response = s3_bucket.put_binary_s3(test_path, test_binary_path)
    body = conn.Object("test-mirrulations1", "data/test").get()["Body"] \
                                                         .read() \
                                                         .decode("utf-8")
    assert response['ResponseMetadata']['HTTPStatusCode'] == 200
    assert body == "/Users/jack11wagner/Courses/334/mirrulations/" + \
                   "mirrulations-core/tests/test-mirrulations-pdf.pdf"
