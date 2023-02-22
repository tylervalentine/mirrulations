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
            print("Could not find necessary keys in json")
            raise KeyError

        return agencyId, docket_id, item_id


    def get_docket_json_path(self, json): 
        agencyId, docket_id, item_id = self.get_attributes(json)
        if "FRDOC" in item_id:
            item_id = f'{agencyId}_FRDOC_0001'

        return f'data/{agencyId}/{item_id}/text-{item_id}/docket/'

    
    def get_document_json_path(self, json):

        agencyId, docket_id, item_id = self.get_attributes(json)

        if "FRDOC" in item_id:
            # FRDOC document cases
            agency, FRDOC, rest_of_id = item_id.split("_")
            docket_id= rest_of_id.split("-")[0]
            docket_id = '_'.join([agency, FRDOC, docket_id])
            return f'data/{agencyId}/{docket_id}/text-{docket_id}/documents/'
        
        
        if re.match("([A-Z]{2,}-[1-2][0-9]{3,}-[0-9]{4,})-[0-9]{4,}", item_id):
            docket_id = str(re.match("([A-Z]{2,}-[1-2][0-9]{3,}-[0-9]{4,})-[0-9]{4,}", item_id).groups()[0])
            # agency, year, docket_num = id.split('-')[:3]
            # docket_id = "-".join([agency, year, docket_num])
            return f'data/{agencyId}/{docket_id}/text-{docket_id}/documents/'
        
        else: 
            # data/EPA/EPA-HQ-OPP-2011-0939/text-EPA-HQ-OPP-2011-0939/documents/EPA-HQ-OPP-2011-0939-0001.json
            # Cases where id is not of standard form of AGENCYID-<YEAR>-<DocketID>-<DocumentIDorCommentID>
            split_id = item_id.split('-') # list of id_segments
            docket_id = '-'.join(split_id[:-1])
            return f'data/{agencyId}/{docket_id}/text-{docket_id}/documents/'


    def get_comment_json_path(self, json):

        agencyId, docket_id, item_id = self.get_attributes(json)

        if "FRDOC" in item_id:
            # FRDOC comment cases
            agency, FRDOC, rest_of_id = item_id.split("_")
            docket_id= rest_of_id.split("-")[0]
            docket_id = '_'.join([agency, FRDOC, docket_id])
            return f'data/{agencyId}/{docket_id}/text-{docket_id}/comments/'
        
        
        if re.match("([A-Z]{2,}-[1-2][0-9]{3,}-[0-9]{4,})-[0-9]{4,}", item_id):
            docket_id = str(re.match("([A-Z]{2,}-[1-2][0-9]{3,}-[0-9]{4,})-[0-9]{4,}", item_id).groups()[0])
            # agency, year, docket_num = id.split('-')[:3]
            # docket_id = "-".join([agency, year, docket_num])
            return f'data/{agencyId}/{docket_id}/text-{docket_id}/comments/'
        
        else: 
            # data/EPA/EPA-HQ-OPP-2011-0939/text-EPA-HQ-OPP-2011-0939/documents/EPA-HQ-OPP-2011-0939-0002.json
            # Cases where id is not of standard form of AGENCYID-<YEAR>-<DocketID>-<DocumentIDorCommentID>
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