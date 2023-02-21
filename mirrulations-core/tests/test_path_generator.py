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

def test_get_docket_path(generator):
    json = generate_json(id="VETS-2005-0001", type="dockets", agencyId = "VETS")
    expected_path = "data/VETS/VETS-2005-0001/text-VETS-2005-0001/dockets/VETS-2005-0001.json"
    assert expected_path == generator.get_path(json)


def test_get_docket_path_from_FRDOC_docket(generator):
    json = generate_json(id="VETS_FRDOC_0001", type="dockets", agencyId = "VETS")
    expected_path = "data/VETS/FRDOCS/VETS_FRDOC_0001/text-VETS_FRDOC_0001/dockets/VETS_FRDOC_0001.json"
    assert expected_path == generator.get_path(json)

def test_get_document_path(generator):
    json = generate_json(id = "VETS-2005-0001-0001", type="documents", agencyId="VETS")
    expected_path = "data/VETS/VETS-2005-0001/text-VETS-2005-0001/documents/VETS-2005-0001-0001.json"
    assert expected_path == generator.get_document_text_path(json)

def test_get_document_path_from_FRDOC_document(generator):
    json = generate_json(id="VETS_FRDOC_0001-0001", type="documents", agencyId = "VETS")
    expected_path = "data/VETS/FRDOCS/VETS_FRDOC_0001/text-VETS_FRDOC_0001/documents/VETS_FRDOC_0001-0001.json"
    assert expected_path == generator.get_document_text_path(json)

def test_get_comment_path(generator):
    json = generate_json(id = "USTR-2015-0010-0002", type = "comments", agencyId="USTR")
    expected_path = "data/USTR/USTR-2015-0010/text-USTR-2015-0010/comments/USTR-2015-0010-0002.json"
    assert expected_path == generator.get_comment_text_path(json)

# def test_get_docket_path_EPA(generator):
#     job = {
#         "data": {
#             "id": "EPA-HQ-OPP-2011-0939",
#             "type": "dockets"
#         }  
#     } 
#     expected_path = "data/EPA/2011/EPA-HQ-OPP-2011-0939/text-EPA-HQ-OPP-2011-0939/dockets/"
#     assert expected_path == generator.get_docket_path(job)

# def test_get_docket_path_EPA(generator):
#     job = {
#         "data": {
#             "id": "EPA-R08-OAR-2005-UT-0003",
#             "type": "dockets"
#         }  
#     } 
#     expected_path = "data/EPA/2011/EPA-R08-OAR-2005-UT-0003/text-EPA-R08-OAR-2005-UT-0003/dockets/"
#     assert expected_path == generator.get_docket_path(job)

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
