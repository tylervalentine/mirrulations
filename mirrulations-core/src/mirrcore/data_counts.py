import requests
from mirrcore.regulations_api import RegulationsAPI


class DataCounts:
    """
    This class provides an interface to get the total number
    of docket, document, and comment entries on Regulations.gov.

    """

    def __init__(self, api_key):

        self.url = "https://api.regulations.gov/v4"
        self.api_key = api_key
        self.regulations_api = RegulationsAPI(api_key)

    def get_counts(self):
        """
        Get current counts from Regulations.gov.
        Uses 3 API calls each time it is called.
        @return: list of counts for docket, document, and comments
        """
        dockets = self._get_dockets_count()
        documents = self._get_documents_count()
        comments = self._get_comments_count()

        for data in [dockets, documents, comments]:
            if not isinstance(data, int) or data < 0:
                raise DataNotFoundException("Invalid data")

        return [dockets, documents, comments]

    def _get_dockets_count(self):
        """
        Get the number of docket entries on Regulations.gov
        @return integer count of docket entries
        """
        response = self.__make_api_call("dockets")
        return self.__get_total_elements(response)

    def _get_documents_count(self):
        """
        Get the number of document entries on Regulations.gov
        @return integer count of document entries
        """
        response = self.__make_api_call("documents")
        return self.__get_total_elements(response)

    def _get_comments_count(self):
        """
        Get the number of comment entries on Regulations.gov
        @return integer count of comment entries
        """
        response = self.__make_api_call("comments")
        return self.__get_total_elements(response)

    def __get_total_elements(self, response):
        """
        Get the total number of elements from the response
        @param response: json response from Regulations.gov
        @return integer count of elements
        """
        try:
            return response['meta']['totalElements']
        except KeyError as exc:
            raise DataNotFoundException("Improper JSON structure") from exc

    def __make_api_call(self, endpoint):
        """
        Make an API call to Regulations.gov
        @param endpoint: string "dockets", "documents", or "comments"
        @return json response from Regulations.gov
        """
        try:
            response = self.regulations_api.download(f'{self.url}/{endpoint}')
        except requests.exceptions.RequestException as exc:
            raise DataNotFoundException from exc
        return response


class DataNotFoundException(Exception):
    """
    Generalized exception raised when data is not what
    is expected from Regulations.gov
    """
