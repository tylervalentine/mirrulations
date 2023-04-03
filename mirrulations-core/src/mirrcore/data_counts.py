import requests

class DataStats:

    DOCS = "https://api.regulations.gov/v4/documents"
    DOCKETS = "https://api.regulations.gov/v4/dockets"
    COMMENTS = "https://api.regulations.gov/v4/comments"

    def __init__(self, url, key):
        
        self.url = url
        self.key = key

    def get_stats(self):
        self.docs = get_documents_count()
        self.dockets = get_dockets_count()
        self.comments = get_comments_count()

    def get_documents_count():
        response = requests.get(DOCS, params={"api_key": self.key})
        print(get_total_elements(response))

    def get_dockets_count():
        response = requests.get(DOCKETS, params={"api_key": self.key})
        print(get_total_elements(response))

    def get_comments_count():
        response = requests.get(COMMENTS, params={"api_key": self.key})
        print(get_total_elements(response))

    def get_total_elements(response):
        return response.json()['meta']['totalElements']
