import os
import json
from json import dumps, load
import boto3
import botocore

class Saver:
    """
    A class which takes the content of an attachment (pdf, doc, etc.), and
    saves it to a given path.
    ...
    Methods
    -------
    save(content = response, path = string)
        Takes the content (pdf, doc, etc.) and saves the attachment to a
        given path
    """

    def make_path(self, path):
        try:
            os.makedirs(f'/data{path}')
        except FileExistsError:
            print(f'Directory already exists in root: /data{path}')

    def save_to_disk(self, path, data):
        with open(path, 'x', encoding='utf8') as file:
            print('Writing results to disk')
            file.write(dumps(data))

    def save_json(self, path, data):
        """
        writes the results to disk. used by docket document and comment jobs

        Parameters
        ----------
        data : dict
            the results data to be written to disk
        """
        data = data['results']
        if os.path.exists(path) is False:
            self.save_to_disk(path, data)
        else:
            self.check_for_duplicates(path, data, 1)

    def save_duplicate_json(self, path, data, i):
        path_without_file_type = path.strip(".json")
        path = f'{path_without_file_type}({i}).json'
        if os.path.exists(path) is False:
            print(f'JSON is different than duplicate: Labeling ({i})')
            self.save_to_disk(path, data)
        else:
            self.check_for_duplicates(path, data, i + 1)

    def save_attachment(self, path, data):
        with open(path, "wb") as file:
            file.write(data)
            file.close()

    def open_json_file(self, path):
        with open(path, encoding='utf8') as file:
            saved_data = load(file)
        return saved_data

    def is_duplicate(self, existing, new):
        if existing == new:
            print('Data is a duplicate, skipping this download')
            return True
        return False

    def check_for_duplicates(self, path, data, i):
        if self.is_duplicate(self.open_json_file(path), data) is False:
            self.save_duplicate_json(path, data, i)

    def establish_s3_connection(self):
        """
        Checks if a valid connection could be made to s3
        """
        try:
            session = boto3.Session(profile_name="profile_name")
            s3_client = session.client("s3")
            return s3_client
        except Exception:
            return False
        

    def save_to_s3(self, path, data):
        s3_client = self.establish_s3_connection()
        try:
            s3_client.put_object(Bucket="test-mirrulations", Key=f'{path}', Body=json.dumps(data))
            print("SUCCESS: Wrote results to S3")

        except botocore.exceptions.ClientError:
            print("FAILURE: Writing to S3")
