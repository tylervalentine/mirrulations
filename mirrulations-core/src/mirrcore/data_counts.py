import requests

class DataCounts:

    def __init__(self, api_key):
        
        self.url = "https://api.regulations.gov/v4"
        self.api_key = api_key

    def get_counts(self):
        """ 
        Get current counts from Regulations.gov
        @return: list of counts for docket, document, and comments
        """
        dockets = self._get_dockets_count()
        documents = self._get_documents_count()
        comments = self._get_comments_count()
        return [dockets, documents, comments]


    def _get_dockets_count(self):
        """
        Get the number of docket entries on Regulations.gov
        @return integer count of docket entries
        """
        response = requests.get(f'{self.url}/{"dockets"}', params={"api_key": self.api_key})
        return(self.__get_total_elements(response))


    def _get_documents_count(self):
        """
        Get the number of document entries on Regulations.gov
        @return integer count of document entries
        """
        response = requests.get(f'{self.url}/{"documents"}', params={"api_key": self.api_key})
        return(self.__get_total_elements(response))


    def _get_comments_count(self):
        """
        Get the number of comment entries on Regulations.gov
        @return integer count of comment entries
        """
        response = requests.get(f'{self.url}/{"comments"}', params={"api_key": self.api_key})
        return(self.__get_total_elements(response))


    def __get_total_elements(response):
        return response.json()['meta']['totalElements']
