import os
import re

class PathGenerator:

    def __init__(self):
        self.path = "data"

    def get_path(self, json):
        try: 
            type = json["data"]["type"]
        except KeyError:
            print("JSON did not have 'type' key")
            raise KeyError

        if type == "dockets":
            return self.get_docket_path(json)

        elif type == "documents":
            return self.get_document_text_path(json)

        elif type == "comments": 
            return self.get_comment_text_path(json)

    def get_docket_path(self, json): 
        try: 
            id, agencyId = json["data"]["id"], json["data"]["attributes"]["agencyId"]
        except KeyError:
            print("Could not find necessary keys in json")
            raise KeyError
        if "FRDOC" in id:
            return f'data/{agencyId}/{id}/text-{id}/dockets/{id}.json'
        return f'data/{agencyId}/{id}/text-{id}/dockets/{id}.json'


    def get_document_text_path(self, json):
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
            return f'data/{agencyId}/{docket_id}/text-{docket_id}/documents/{id}.json'
        
        
        if re.match("([A-Z]{2,}-[1-2][0-9]{3,}-[0-9]{4,})-[0-9]{4,}", id):
            docket_id = str(re.match("([A-Z]{2,}-[1-2][0-9]{3,}-[0-9]{4,})-[0-9]{4,}", id).groups()[0])
            # agency, year, docket_num = id.split('-')[:3]
            # docket_id = "-".join([agency, year, docket_num])
            return f'data/{agencyId}/{docket_id}/text-{docket_id}/documents/{id}.json'
        
        else: 
            # data/EPA/EPA-HQ-OPP-2011-0939/text-EPA-HQ-OPP-2011-0939/documents/EPA-HQ-OPP-2011-0939-0001.json
            # Cases where id is not of standard form of AGENCYID-<YEAR>-<DocketID>-<DocumentIDorCommentID>
            split_id = id.split('-') # list of id_segments
            docket_id = '-'.join(split_id[:-1])
            return f'data/{agencyId}/{docket_id}/text-{docket_id}/documents/{id}.json'
                
            


    def get_comment_text_path(self, json):
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
            return f'data/{agencyId}/{docket_id}/text-{docket_id}/comments/{id}.json'
        
        
        if re.match("([A-Z]{2,}-[1-2][0-9]{3,}-[0-9]{4,})-[0-9]{4,}", id):
            docket_id = str(re.match("([A-Z]{2,}-[1-2][0-9]{3,}-[0-9]{4,})-[0-9]{4,}", id).groups()[0])
            # agency, year, docket_num = id.split('-')[:3]
            # docket_id = "-".join([agency, year, docket_num])
            return f'data/{agencyId}/{docket_id}/text-{docket_id}/comments/{id}.json'
        
        else: 
            # data/EPA/EPA-HQ-OPP-2011-0939/text-EPA-HQ-OPP-2011-0939/documents/EPA-HQ-OPP-2011-0939-0002.json
            # Cases where id is not of standard form of AGENCYID-<YEAR>-<DocketID>-<DocumentIDorCommentID>
            split_id = id.split('-') # list of id_segments
            docket_id = '-'.join(split_id[:-1])
            return f'data/{agencyId}/{docket_id}/text-{docket_id}/comments/{id}.json'

