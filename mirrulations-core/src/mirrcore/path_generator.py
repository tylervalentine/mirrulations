
'''
Returns the agency, docket id, and item id from a loaded json object.
'''
def extract_data(json_data, is_docket_json=False):
    agency_id = json_data['data']['attributes']['agencyId']
    if is_docket_json:
        docket_id = None
    else:
        docket_id = json_data['data']['attributes']['docketId']
    item_id = json_data['data']['id']

    if is_docket_json:
        # in this case item_id is the docket id
        return agency_id, item_id, None
    else:
        return agency_id, docket_id, item_id


class PathGenerator:
    def __init__(self, path):
        self._path = path

    def get_docket_path(self, json_data): 
        agency, docket_id, _ = extract_data(json_data, is_docket_json=True)
        return self._path + f'/data/{agency}/text-{docket_id}/docket/{docket_id}.json'

    def get_document_path(self, json_data):
        agency, docket_id, item_id = extract_data(json_data)
        return self._path + f'/data/{agency}/text-{docket_id}/documents/{item_id}.json'

    def get_comment_path(self, json_data):
        agency, docket_id, item_id = extract_data(json_data)
        return self._path + f'/data/{agency}/text-{docket_id}/comments/{item_id}.json'

    def get_document_extracted_text_path(self, json_data, file_name, extraction_method):
        agency, docket_id, item_id = extract_data(json_data)
        return self._path + f'/data/{agency}/text-{docket_id}/documents_extracted_text/{extraction_method}/{file_name}'

    def get_comment_extracted_text_path(self, json_data, file_name, extraction_method):
        agency, docket_id, item_id = extract_data(json_data)
        return self._path + f'/data/{agency}/text-{docket_id}/comments_extracted_text/{extraction_method}/{file_name}'

    def get_document_attachment_path(self, json_data, file_name):
        agency, docket_id, item_id = extract_data(json_data)
        return self._path + f'/data/{agency}/binary-{docket_id}/documents_attachments/{file_name}'

    def get_comment_attachment_path(self, json_data, file_name):
        agency, docket_id, item_id = extract_data(json_data)
        return self._path + f'/data/{agency}/binary-{docket_id}/comments_attachments/{file_name}'
