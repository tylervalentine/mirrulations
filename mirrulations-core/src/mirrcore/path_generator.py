import os


class PathGenerator:

    def __init__(self):
        self.path = "data"

    def get_path(self, json):
        try: 
            type = json["data"]["type"]
        except KeyError:
            print("JSON did not have 'type' key")

        if type == "dockets":
            return self.get_docket_path(json)

        elif type == "documents":
            return self.get_document_text_path(json)
        elif type == "comments":
            #TODO implement comment pathing
            return 0

    def get_docket_path(self, json): 
        try: 
            id, type, agencyId = json["data"]["id"], json["data"]["type"], json["data"]["attributes"]["agencyId"]
        except KeyError:
            print("Could not find necessary keys")
        if "FRDOC" in id:
            return f'data/{agencyId}/FRDOCS/{id}/text-{id}/{type}/{id}.json'
        return f'data/{agencyId}/{id}/text-{id}/dockets/{id}.json'


    def get_document_text_path(self, json):
        try: 
            id, type, agencyId = json["data"]["id"], json["data"]["type"], json["data"]["attributes"]["agencyId"]
        except KeyError:
            print("Could not find necessary keys")
        if "FRDOC" in id:
            agency, FRDOC, rest_of_id = id.split("_")
            docket_id, document_id = rest_of_id.split("-")
            docket_id = '_'.join([agency, FRDOC, docket_id])
            return f'data/{agencyId}/FRDOCS/{docket_id}/text-{docket_id}/documents/{id}.json'
        agency, year, docket_num, document_id = id.split('-')
        docket_id = "-".join([agency, year, docket_num])
        type_folder = "text-" + docket_id

        return f'data/{agencyId}/{docket_id}/{type_folder}/documents/{id}.json'


    def get_comment_text_path(self, json):
        try: 
            id, type, agencyId = json["data"]["id"], json["data"]["type"], json["data"]["attributes"]["agencyId"]
        except KeyError:
            print("Could not find necessary keys")
        if "FRDOC" in id:
            agency, FRDOC, rest_of_id = id.split("_")
            docket_id, comment_id = rest_of_id.split("-")[0]
            docket_id = '_'.join([agency, FRDOC, docket_id])
            return f'data/{agencyId}/FRDOCS/{docket_id}/text-{docket_id}/comments/{id}.json'
        agency, year, docket_num, document_id = id.split('-')
        docket_id = "-".join([agency, year, docket_num])
        type_folder = "text-" + docket_id

        return f'data/{agency}/{docket_id}/{type_folder}/comments/{id}.json'

