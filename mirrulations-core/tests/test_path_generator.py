from mirrcore.path_generator import PathGenerator

def test_get_docket_path():
    job = {
        "data": {
            "id": "VETS-2005-0001",
            "type": "dockets"
        }  
    } 
    actual_path = "data/VETS/2005/VETS-2005-0001/text-VETS-2005-0001/docket/"
    assert actual_path == PathGenerator().get_docket_path(job)


def test_get_docket_path_from_FRDOC_docket():
    job = {
        "data":{
            "id": "VETS_FRDOC_0001", 
            "type": "dockets"
        }
    }
    expected_path = "data/VETS/FRDOCS/VETS_FRDOC_0001/text-VETS_FRDOC_0001/docket/"
    assert expected_path == PathGenerator().get_docket_path(job)


def test_get_document_path_from_FRDOC_document():
    job = {
        "data":{
            "id": "VETS_FRDOC_0001-0001", 
            "type": "documents"
        }
    }
    expected_path = "data/VETS/FRDOCS/VETS_FRDOC_0001/text-VETS_FRDOC_0001/documents/"
    assert expected_path == PathGenerator().get_document_text_path(job)

def test_get_document_path():
    job = {
        "data": {
            "id": "USTR-2015-0010-0001",
            "type": "documents"
        }  
    } 
    actual_path = "data/USTR/2015/USTR-2015-0010/text-USTR-2015-0010/documents/"
    assert actual_path == PathGenerator().get_document_text_path(job)

def test_get_comment_path():
    job = {
        "data": {
            "id": "USTR-2015-0010-0002",
            "type": "comments"
        }  
    } 
    actual_path = "data/USTR/2015/USTR-2015-0010/text-USTR-2015-0010/comments/"
    assert actual_path == PathGenerator().get_comment_text_path(job)

