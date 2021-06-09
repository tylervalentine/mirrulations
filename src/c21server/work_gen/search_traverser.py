
class SearchIterator:

    def __init__(self, api, endpoint, last_modified_date):
        self.api = api
        self.url = f'https://api.regulations.gov/v4/{endpoint}'
        self.next_page = 1
        self.params = {
            'sort': 'lastModifiedDate',
            'page[size]': 250,
            'filter[lastModifiedDate][ge]': last_modified_date
        }
        self.iteration_done = False

    def __iter__(self):
        return self

    def __next__(self):
        if self.iteration_done:
            raise StopIteration

        self.params['page[number]'] = self.next_page
        self.next_page += 1

        result = self.api.download(self.url, self.params)
        self.iteration_done = self.check_if_done(result)

        return result

    def check_if_done(self, result):
        if result['meta']['pageNumber'] != result['meta']['totalPages']:
            return False

        if result['meta']['totalElements'] <= 5000:
            self.iteration_done = True
            return True

        # Reset for the next search
        self.next_page = 1
        # Dates in data have T between date and time and Z at end
        # Dates in query have a space between and nothing at the end
        last_date = result['data'][-1]['attributes']['lastModifiedDate']\
            .replace('T', ' ').replace('Z', '')
        self.params['filter[lastModifiedDate][ge]'] = last_date

        return False
