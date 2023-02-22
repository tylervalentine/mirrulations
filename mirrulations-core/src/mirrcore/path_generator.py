import re


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

    def get_docket_json_path(self, json): 
        try: 
            id, agencyId = json["data"]["id"], json["data"]["attributes"]["agencyId"]
        except KeyError:
            print("Could not find necessary keys in json")
            raise KeyError
        if "FRDOC" in id:
            return f'data/{agencyId}/{id}/text-{id}/docket/'
        return f'data/{agencyId}/{id}/text-{id}/docket/'


    def get_document_extracted_text_path(self, json_data, file_name, extraction_method):
        agency, docket_id, item_id = extract_data(json_data)
        return self._path + f'/data/{agency}/text-{docket_id}/documents_extracted_text/{extraction_method}/{file_name}'


    def get_document_json_path(self, json):
        try: 
            id, agencyId = json["data"]["id"], json["data"]["attributes"]["agencyId"]
        except KeyError:
            print("Could not find necessary keys in json")
            raise KeyError

        if "FRDOC" in id:
            # FRDOC document cases
            agency, FRDOC, rest_of_id = id.split("_")
            docket_id= rest_of_id.split("-")[0]
            docket_id = '_'.join([agency, FRDOC, docket_id])
            return f'data/{agencyId}/{docket_id}/text-{docket_id}/documents/'
        
        
        if re.match("([A-Z]{2,}-[1-2][0-9]{3,}-[0-9]{4,})-[0-9]{4,}", id):
            docket_id = str(re.match("([A-Z]{2,}-[1-2][0-9]{3,}-[0-9]{4,})-[0-9]{4,}", id).groups()[0])
            # agency, year, docket_num = id.split('-')[:3]
            # docket_id = "-".join([agency, year, docket_num])
            return f'data/{agencyId}/{docket_id}/text-{docket_id}/documents/'
        
        else: 
            # data/EPA/EPA-HQ-OPP-2011-0939/text-EPA-HQ-OPP-2011-0939/documents/EPA-HQ-OPP-2011-0939-0001.json
            # Cases where id is not of standard form of AGENCYID-<YEAR>-<DocketID>-<DocumentIDorCommentID>
            split_id = id.split('-') # list of id_segments
            docket_id = '-'.join(split_id[:-1])
            return f'data/{agencyId}/{docket_id}/text-{docket_id}/documents/'


    def get_comment_json_path(self, json):
        try: 
            id, agencyId = json["data"]["id"], json["data"]["attributes"]["agencyId"]
        except KeyError:
            print("Could not find necessary keys")
            raise KeyError

        if "FRDOC" in id:
            # FRDOC comment cases
            agency, FRDOC, rest_of_id = id.split("_")
            docket_id= rest_of_id.split("-")[0]
            docket_id = '_'.join([agency, FRDOC, docket_id])
            return f'data/{agencyId}/{docket_id}/text-{docket_id}/comments/'
        
        
        if re.match("([A-Z]{2,}-[1-2][0-9]{3,}-[0-9]{4,})-[0-9]{4,}", id):
            docket_id = str(re.match("([A-Z]{2,}-[1-2][0-9]{3,}-[0-9]{4,})-[0-9]{4,}", id).groups()[0])
            # agency, year, docket_num = id.split('-')[:3]
            # docket_id = "-".join([agency, year, docket_num])
            return f'data/{agencyId}/{docket_id}/text-{docket_id}/comments/'
        
        else: 
            # data/EPA/EPA-HQ-OPP-2011-0939/text-EPA-HQ-OPP-2011-0939/documents/EPA-HQ-OPP-2011-0939-0002.json
            # Cases where id is not of standard form of AGENCYID-<YEAR>-<DocketID>-<DocumentIDorCommentID>
            split_id = id.split('-') # list of id_segments
            docket_id = '-'.join(split_id[:-1])
            return f'data/{agencyId}/{docket_id}/text-{docket_id}/comments/'


    def get_comment_extracted_text_path(self, json_data, file_name, extraction_method):
        agency, docket_id, item_id = extract_data(json_data)
        return self._path + f'/data/{agency}/text-{docket_id}/comments_extracted_text/{extraction_method}/{file_name}'


    def get_document_attachment_path(self, json_data, file_name):
        agency, docket_id, item_id = extract_data(json_data)
        return self._path + f'/data/{agency}/binary-{docket_id}/documents_attachments/{file_name}'


    def get_comment_attachment_path(self, json_data, file_name):
        agency, docket_id, item_id = extract_data(json_data)
        return self._path + f'/data/{agency}/binary-{docket_id}/comments_attachments/{file_name}'
