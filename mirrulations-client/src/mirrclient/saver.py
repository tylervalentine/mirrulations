import os
from json import dumps


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

    def save_json(self, path, data):
        """
        writes the results to disk. used by docket document and comment jobs

        Parameters
        ----------
        data : dict
            the results data to be written to disk
        """
        with open(path, 'w+', encoding='utf8') as file:
            print('Writing results to disk')
            file.write(dumps(data['results']))

    def save_attachment(self, path, data):
        with open(path, "wb") as file:
            file.write(data)
            file.close()
