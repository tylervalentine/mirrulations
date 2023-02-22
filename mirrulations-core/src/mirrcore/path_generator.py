import re

class PathGenerator:

    '''
    Returns the agency, docket id, and item id from a loaded json object.
    '''
    def get_attributes(self, json_data, is_docket=False):
        try: 
            item_id, agencyId = json_data["data"]["id"], json_data["data"]["attributes"]["agencyId"]
            if is_docket:
                docket_id = item_id
            else:
                docket_id = json_data['data']['attributes']['docketId']
        except KeyError:
            # if a key cannot be found
            print("Could not find necessary keys in json")
            docket_id = None
            raise KeyError
        return agencyId, docket_id, item_id


    def get_docket_json_path(self, json): 
        agencyId, docket_id, item_id = self.get_attributes(json, True)
        return f'data/{agencyId}/{item_id}/text-{item_id}/docket/'

    
    def get_document_json_path(self, json):

        agencyId, docket_id, item_id = self.get_attributes(json)
        if docket_id is not None:
            return f'data/{agencyId}/{docket_id}/text-{docket_id}/documents/'
        
        else: 
            # Case where we do not have a docketId so we must parse the item_id
            split_id = item_id.split('-') # list of id_segments
            docket_id = '-'.join(split_id[:-1])
            return f'data/{agencyId}/{docket_id}/text-{docket_id}/documents/'

    def get_comment_json_path(self, json):

        agencyId, docket_id, item_id = self.get_attributes(json)
        if docket_id is not None:
            return f'data/{agencyId}/{docket_id}/text-{docket_id}/comments/'
        
        else: 
            # Case where we do not have a docketId so we must parse the item_id
            split_id = item_id.split('-') # list of id_segments
            docket_id = '-'.join(split_id[:-1])
            return f'data/{agencyId}/{docket_id}/text-{docket_id}/comments/'


    # def get_comment_extracted_text_path(self, json_data, file_name, extraction_method):
    #     agency, docket_id, item_id = extract_data(json_data)
    #     return self._path + f'/data/{agency}/text-{docket_id}/comments_extracted_text/{extraction_method}/{file_name}'

    # def get_document_extracted_text_path(self, json_data, file_name, extraction_method):
    #     agency, docket_id, item_id = extract_data(json_data)
    #     return self._path + f'/data/{agency}/text-{docket_id}/documents_extracted_text/{extraction_method}/{file_name}'


    # def get_document_attachment_path(self, json_data, file_name):
    #     agency, docket_id, item_id = extract_data(json_data)
    #     return self._path + f'/data/{agency}/binary-{docket_id}/documents_attachments/{file_name}'


    # def get_comment_attachment_path(self, json_data, file_name):
    #     agency, docket_id, item_id = extract_data(json_data)
    #     return self._path + f'/data/{agency}/binary-{docket_id}/comments_attachments/{file_name}'
