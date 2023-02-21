from mirrcore.path_generator import PathGenerator
from pytest import fixture
import pytest
import json

@fixture(name='generator')
def path_generator():
    return PathGenerator()

def generate_json(id=str, type=str, agencyId=str) -> dict:
    # returns a json in the form that regulations.gov api stores data
    return {"data":{
        "id": id,
        "type": type, 
        "attributes": {
                    "agencyId":agencyId
                }
        }}


def test_get_comment_path_full_json(generator):
    json_file = '{"data": {"attributes": {"address1": null, "address2": null, "agencyId": "USTR", "category": null, "city": "Washington", "comment": "See attached. ", "commentOn": "0900006481bce624", "commentOnDocumentId": "USTR-2015-0010-0001", "country": "United States", "displayProperties": null, "docAbstract": null, "docketId": "USTR-2015-0010", "documentType": "Public Submission", "duplicateComments": 0, "email": null, "fax": null, "field1": null, "field2": null, "fileFormats": null, "firstName": "Stephanie", "govAgency": null, "govAgencyType": null, "lastName": "Henry", "legacyId": null, "modifyDate": "2015-09-30T20:57:34Z", "objectId": "0900006481c7f7ad", "openForComment": false, "organization": "US-China Business Council", "originalDocumentId": null, "pageCount": 0, "phone": null, "postedDate": "2015-09-30T04:00:00Z", "postmarkDate": null, "reasonWithdrawn": null, "receiveDate": "2015-09-18T04:00:00Z", "restrictReason": null, "restrictReasonType": null, "stateProvinceRegion": "DC", "submitterRep": null, "submitterRepAddress": null, "submitterRepCityState": null, "subtype": null, "title": "US China Business Council", "trackingNbr": "1jz-8l73-5qbv", "withdrawn": false, "zip": null}, "id": "USTR-2015-0010-0002", "links": {"self": "https://api.regulations.gov/v4/comments/USTR-2015-0010-0002"}, "relationships": {"attachments": {"links": {"related": "https://api.regulations.gov/v4/comments/USTR-2015-0010-0002/attachments", "self": "https://api.regulations.gov/v4/comments/USTR-2015-0010-0002/relationships/attachments"}}}, "type": "comments"}}'
    json_file = json.loads(json_file)
    expected_path = "data/USTR/USTR-2015-0010/text-USTR-2015-0010/comments"
    assert expected_path == generator.get_path(json_file)

def test_get_document_path_full_json(generator):
    json_file = '{"data": {"attributes": {"additionalRins": null, "address1": null, "address2": null, "agencyId": "USTR", "allowLateComments": false, "authorDate": null, "authors": null, "category": null, "cfrPart": null, "city": null, "comment": null, "commentEndDate": null, "commentStartDate": null, "country": null, "displayProperties": null, "docAbstract": null, "docketId": "USTR-2015-0010", "documentType": "Supporting & Related Material", "effectiveDate": null, "email": null, "exhibitLocation": null, "exhibitType": null, "fax": null, "field1": null, "field2": null, "fileFormats": null, "firstName": null, "frDocNum": null, "frVolNum": null, "govAgency": null, "govAgencyType": null, "implementationDate": null, "lastName": null, "legacyId": null, "media": null, "modifyDate": "2015-10-09T15:59:17Z", "objectId": "0900006481cb1d8f", "ombApproval": null, "openForComment": false, "organization": null, "originalDocumentId": null, "pageCount": 0, "paperLength": 0, "paperWidth": 0, "phone": null, "postedDate": "2015-10-05T00:00:00Z", "postmarkDate": null, "reasonWithdrawn": "Upddate to agenda", "receiveDate": null, "regWriterInstruction": null, "restrictReason": null, "restrictReasonType": null, "sourceCitation": null, "startEndPage": null, "stateProvinceRegion": null, "subject": null, "submitterRep": null, "submitterRepAddress": null, "submitterRepCityState": null, "subtype": null, "title": "China Public Hearing Agenda", "topics": null, "trackingNbr": null, "withdrawn": true, "zip": null}, "id": "USTR-2015-0010-0015", "links": {"self": "https://api.regulations.gov/v4/documents/USTR-2015-0010-0015"}, "relationships": {"attachments": {"links": {"related": "https://api.regulations.gov/v4/documents/USTR-2015-0010-0015/attachments", "self": "https://api.regulations.gov/v4/documents/USTR-2015-0010-0015/relationships/attachments"}}}, "type": "documents"}}'
    json_file = json.loads(json_file)
    expected_path = "data/USTR/USTR-2015-0010/text-USTR-2015-0010/documents"
    assert expected_path == generator.get_path(json_file)

def test_get_docket_path_full_json(generator):
    json_file = '{"data": {"attributes": {"additionalRins": null, "address1": null, "address2": null, "agencyId": "USTR", "allowLateComments": false, "authorDate": null, "authors": null, "category": null, "cfrPart": null, "city": null, "comment": null, "commentEndDate": "2015-09-24T03:59:59Z", "commentStartDate": "2015-08-10T04:00:00Z", "country": null, "displayProperties": null, "docAbstract": null, "docketId": "USTR-2015-0010", "documentType": "Notice", "effectiveDate": null, "email": null, "exhibitLocation": null, "exhibitType": null, "fax": null, "field1": null, "field2": null, "fileFormats": [{"fileUrl": "https://downloads.regulations.gov/USTR-2015-0010-0001/content.pdf", "format": "pdf", "size": 182010}, {"fileUrl": "https://downloads.regulations.gov/USTR-2015-0010-0001/content.htm", "format": "htm", "size": 9709}], "firstName": null, "frDocNum": "2015-19523", "frVolNum": null, "govAgency": null, "govAgencyType": null, "implementationDate": null, "lastName": null, "legacyId": null, "media": null, "modifyDate": "2015-10-02T01:31:31Z", "objectId": "0900006481bce624", "ombApproval": null, "openForComment": false, "organization": null, "originalDocumentId": "USTR_FRDOC_0001-0346", "pageCount": 0, "paperLength": 0, "paperWidth": 0, "phone": null, "postedDate": "2015-08-10T04:00:00Z", "postmarkDate": null, "reasonWithdrawn": null, "receiveDate": "2015-08-10T04:00:00Z", "regWriterInstruction": null, "restrictReason": null, "restrictReasonType": null, "sourceCitation": null, "startEndPage": "47985 - 47986", "stateProvinceRegion": null, "subject": null, "submitterRep": null, "submitterRepAddress": null, "submitterRepCityState": null, "subtype": null, "title": "Public Hearing: China\'s Compliance with WTO Commitments", "topics": null, "trackingNbr": null, "withdrawn": false, "zip": null}, "id": "USTR-2015-0010-0001", "links": {"self": "https://api.regulations.gov/v4/documents/USTR-2015-0010-0001"}, "relationships": {"attachments": {"links": {"related": "https://api.regulations.gov/v4/documents/USTR-2015-0010-0001/attachments", "self": "https://api.regulations.gov/v4/documents/USTR-2015-0010-0001/relationships/attachments"}}}, "type": "documents"}}'
    json_file = json.loads(json_file)
    expected_path = "data/USTR/USTR-2015-0010/text-USTR-2015-0010/docket"
    assert expected_path == generator.get_path(json_file)

def test_get_docket_path(generator):
    json = generate_json(id="VETS-2005-0001", type="dockets", agencyId = "VETS")
    expected_path = "data/VETS/VETS-2005-0001/text-VETS-2005-0001/dockets/VETS-2005-0001.json"
    assert expected_path == generator.get_path(json)

def test_get_docket_path_from_FRDOC_docket(generator):
    json = generate_json(id="VETS_FRDOC_0001", type="dockets", agencyId = "VETS")
    expected_path = "data/VETS/VETS_FRDOC_0001/text-VETS_FRDOC_0001/dockets/VETS_FRDOC_0001.json"
    assert expected_path == generator.get_path(json)

def test_get_document_path(generator):
    json = generate_json(id = "VETS-2005-0001-0001", type="documents", agencyId="VETS")
    expected_path = "data/VETS/VETS-2005-0001/text-VETS-2005-0001/documents/VETS-2005-0001-0001.json"
    assert expected_path == generator.get_path(json)

def test_get_document_path_from_FRDOC_document(generator):
    json = generate_json(id="VETS_FRDOC_0001-0001", type="documents", agencyId = "VETS")
    expected_path = "data/VETS/VETS_FRDOC_0001/text-VETS_FRDOC_0001/documents/VETS_FRDOC_0001-0001.json"
    assert expected_path == generator.get_path(json)

def test_get_comment_path(generator):
    json = generate_json(id = "USTR-2015-0010-0002", type = "comments", agencyId="USTR")
    expected_path = "data/USTR/USTR-2015-0010/text-USTR-2015-0010/comments/USTR-2015-0010-0002.json"
    assert expected_path == generator.get_path(json)

def test_get_docket_path_EPA_with_unconvential_agencyId(generator):
    json = generate_json(id = "EPA-HQ-OPP-2011-0939", type="dockets", agencyId="EPA")
    expected_path = "data/EPA/EPA-HQ-OPP-2011-0939/text-EPA-HQ-OPP-2011-0939/dockets/EPA-HQ-OPP-2011-0939.json"
    assert expected_path == generator.get_path(json)

def test_get_document_path_EPA_with_unconvential_agencyId(generator):
    json = generate_json(id = "EPA-HQ-OPP-2011-0939-0001", type="documents", agencyId="EPA")
    expected_path = "data/EPA/EPA-HQ-OPP-2011-0939/text-EPA-HQ-OPP-2011-0939/documents/EPA-HQ-OPP-2011-0939-0001.json"
    assert expected_path == generator.get_path(json)

def test_get_docket_path_with_numbers_in_agencyId(generator):
    json = generate_json(id = "EPA-R08-OAR-2005-UT-0003", type="dockets", agencyId="EPA")
    expected_path = "data/EPA/EPA-R08-OAR-2005-UT-0003/text-EPA-R08-OAR-2005-UT-0003/dockets/EPA-R08-OAR-2005-UT-0003.json"
    assert expected_path == generator.get_path(json)


def test_get_comment_path(generator):
    json = generate_json(id = "USTR-2015-0010-0002", type = "comments", agencyId="USTR")
    expected_path = "data/USTR/USTR-2015-0010/text-USTR-2015-0010/comments/USTR-2015-0010-0002.json"
    assert expected_path == generator.get_path(json)

def test_get_docket_path_with_missing_type_key(generator):
    json = {"data":{
        "id": "VETS-2005-0001", 
        "attributes": {
                    "agencyId":"VETS"
                }
        }}
    with pytest.raises(KeyError):
        generator.get_path(json)

def test_get_docket_path_with_missing_id_key(generator):
    json = {"data":{
        "type":"dockets",
        "attributes": {
                    "agencyId":"VETS"
                }
        }}
    with pytest.raises(KeyError):
        generator.get_path(json)

def test_get_document_path_with_missing_id_key(generator):
    json = {"data":{
        "type":"documents",
        "attributes": {
                    "agencyId":"VETS"
                }
        }}
    with pytest.raises(KeyError):
        generator.get_path(json)

def test_get_comment_path_with_missing_id_key(generator):
    json = {"data":{
        "type":"comments",
        "attributes": {
                    "agencyId":"VETS"
                }
        }}
    with pytest.raises(KeyError):
        generator.get_path(json)
