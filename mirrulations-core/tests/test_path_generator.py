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