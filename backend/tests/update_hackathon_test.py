import time
from datetime import datetime
from dataset_tests import *
from utils import add_row


def test_update_hackathon_with_normal_parameter_values(app,client):
    
    with app.app_context():
        from main import db
        db.create_all()
        
    add_row(**update_hackathon_dtst1)
    
    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["name"] == "Hackathon1"
    assert response_get1_before.json["description"] == "Full Description"
    assert response_get1_before.json["url"] == "hack1.com"
    assert response_get1_before.json["startDate"] == "2027-01-02T01:03:00"
    assert response_get1_before.json["endDate"] == "2027-02-02T01:03:00"
    assert response_get1_before.json["location"] == "Kavala"
    assert response_get1_before.json["mode"] == "online"
    assert response_get1_before.json["organizer"] == "UoA"
    assert response_get1_before.json["hasPrize"] == True
    assert response_get1_before.json["prizeDetails"] == "500$"
    assert response_get1_before.json["tags"] == "AI,ML,Python"
    assert response_get1_before.json["status"] == "published"
    
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt)
    assert response_patch1.status_code == 200
    assert response_patch1.json["success"] == "Successfully updated hackathon with an id of : 1"
    
    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["name"] == "Hackathon1 Changed"
    assert response_get1_after.json["description"] == "Full Description Changed"
    assert response_get1_after.json["url"] == "hack1.com Changed"
    assert response_get1_after.json["startDate"] == "2027-01-02T01:03:00"
    assert response_get1_after.json["endDate"] == "2027-02-02T01:03:00"
    assert response_get1_after.json["location"] == "Kavala Changed"
    assert response_get1_after.json["mode"] == "hybrid"
    assert response_get1_after.json["organizer"] == "UoA"
    assert response_get1_after.json["hasPrize"] == False
    assert response_get1_after.json["prizeDetails"] == None
    assert response_get1_after.json["tags"] == "AI,ML,Python Changed"
    assert response_get1_after.json["status"] == "published"
    assert response_get1_after.json["interestCount"] == 15
    
    
def test_update_hackathon_only_name(app,client):
    with app.app_context():
        from main import db
        db.create_all()
    
    add_row(**update_hackathon_dtst1)
    
    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["name"] == "Hackathon1" #changes on update
    
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_only_name)
    assert response_patch1.status_code == 200
    assert response_patch1.json["success"] == "Successfully updated hackathon with an id of : 1"
    
    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["name"] == "Hackathon1 Changed"

def test_update_hackathon_only_url(app,client):
    with app.app_context():
        from main import db
        db.create_all()
    
    add_row(**update_hackathon_dtst1)
    
    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["name"] == "Hackathon1" #changes on update
    
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_only_url)
    assert response_patch1.status_code == 200
    assert response_patch1.json["success"] == "Successfully updated hackathon with an id of : 1"
    
    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["url"] == "hack1.com Changed"

# def test_update_hackathon_only_description_location_organizer_tags(app,client):
#     pass

# def test_update_hackathon_only_status(app,client):
#     pass

# def test_update_hackathon_only_mode(app,client):
#     pass

# def test_update_hackathon_only_hasPrize(app,client):
#     pass

# def test_update_hackathon_only_startDate_and_endDate(app,client):
#     pass

# def test_update_hackathon_only_name_and_url(app,client):
#     pass