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
    assert response_get1_after.json["name"] == "Hackathon1 Changed" #changed on update
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

def test_update_hackathon_only_url(app,client):
    with app.app_context():
        from main import db
        db.create_all()
    
    add_row(**update_hackathon_dtst1)
    
    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["url"] == "hack1.com" #changes on update
    
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_only_url)
    assert response_patch1.status_code == 200
    assert response_patch1.json["success"] == "Successfully updated hackathon with an id of : 1"
    
    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["name"] == "Hackathon1"
    assert response_get1_after.json["url"] == "hack1.com Changed" #changed on update
    assert response_get1_before.json["description"] == "Full Description"
    assert response_get1_before.json["startDate"] == "2027-01-02T01:03:00"
    assert response_get1_before.json["endDate"] == "2027-02-02T01:03:00"
    assert response_get1_before.json["location"] == "Kavala"
    assert response_get1_before.json["mode"] == "online"
    assert response_get1_before.json["organizer"] == "UoA"
    assert response_get1_before.json["hasPrize"] == True
    assert response_get1_before.json["prizeDetails"] == "500$"
    assert response_get1_before.json["tags"] == "AI,ML,Python"
    assert response_get1_before.json["status"] == "published"

def test_update_hackathon_only_description_location_organizer_tags(app,client):
    with app.app_context():
            from main import db
            db.create_all()
        
    add_row(**update_hackathon_dtst1)
    
    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["description"] == "Full Description"
    assert response_get1_before.json["location"] == "Kavala"
    assert response_get1_before.json["organizer"] == "UoA"
    assert response_get1_before.json["tags"] == "AI,ML,Python"
    
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_description_location_organizer_tags)
    assert response_patch1.status_code == 200
    assert response_patch1.json["success"] == "Successfully updated hackathon with an id of : 1"
    
    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["description"] == "Full Description Changed"
    assert response_get1_after.json["location"] == "Kavala Changed"
    assert response_get1_after.json["organizer"] == "UoA Changed"
    assert response_get1_after.json["tags"] == "AI,ML,Python Changed"
    assert response_get1_before.json["name"] == "Hackathon1"
    assert response_get1_before.json["url"] == "hack1.com"
    assert response_get1_before.json["startDate"] == "2027-01-02T01:03:00"
    assert response_get1_before.json["endDate"] == "2027-02-02T01:03:00"
    assert response_get1_before.json["mode"] == "online"
    assert response_get1_before.json["hasPrize"] == True
    assert response_get1_before.json["prizeDetails"] == "500$"
    assert response_get1_before.json["status"] == "published"

def test_update_hackathon_only_status_correct(app,client):
    
    with app.app_context():
        from main import db
        db.create_all()

    add_row(**update_hackathon_dtst1)

    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["status"] == "published" #changes on update

    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_only_status_correct)
    assert response_patch1.status_code == 200
    assert response_patch1.json["success"] == "Successfully updated hackathon with an id of : 1"

    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_before.json["name"] == "Hackathon1"
    assert response_get1_before.json["description"] == "Full Description"
    assert response_get1_before.json["url"] == "hack1.com"
    assert response_get1_before.json["startDate"] == "2027-01-02T01:03:00"
    assert response_get1_before.json["endDate"] == "2027-02-02T01:03:00"
    assert response_get1_before.json["location"] == "Kavala"
    assert response_get1_after.json["status"] == "draft"
    assert response_get1_before.json["mode"] == "online"
    assert response_get1_before.json["organizer"] == "UoA"
    assert response_get1_before.json["hasPrize"] == True
    assert response_get1_before.json["prizeDetails"] == "500$"
    assert response_get1_before.json["tags"] == "AI,ML,Python"

def test_update_hackathon_only_status_wrong(app,client):
    
    with app.app_context():
        from main import db
        db.create_all()

    add_row(**update_hackathon_dtst1)

    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["status"] == "published" #changes on update

    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_only_status_wrong)
    assert response_patch1.status_code == 400
    assert response_patch1.json["error"] == "Wrong status"

def test_update_hackathon_only_mode_correct(app,client):
    with app.app_context():
        from main import db
        db.create_all()
    
    add_row(**update_hackathon_dtst1)
    
    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["mode"] == "online" #changes on update
    
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_only_mode_correct)
    assert response_patch1.status_code == 200
    assert response_patch1.json["success"] == "Successfully updated hackathon with an id of : 1"
    
    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_before.json["name"] == "Hackathon1"
    assert response_get1_before.json["description"] == "Full Description"
    assert response_get1_before.json["url"] == "hack1.com"
    assert response_get1_before.json["startDate"] == "2027-01-02T01:03:00"
    assert response_get1_before.json["endDate"] == "2027-02-02T01:03:00"
    assert response_get1_before.json["location"] == "Kavala"
    assert response_get1_before.json["organizer"] == "UoA"
    assert response_get1_before.json["hasPrize"] == True
    assert response_get1_before.json["prizeDetails"] == "500$"
    assert response_get1_before.json["tags"] == "AI,ML,Python"
    assert response_get1_before.json["status"] == "published"
    assert response_get1_after.json["mode"] == "hybrid"
    
def test_update_hackathon_only_mode_wrong(app,client):
    
    with app.app_context():
        from main import db
        db.create_all()

    add_row(**update_hackathon_dtst1)

    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["mode"] == "online" #changes on update

    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_only_mode_wrong)
    assert response_patch1.status_code == 400
    assert response_patch1.json["error"] == "Wrong mode"

def test_update_hackathon_only_hasPrize_and_prizeDetails_correct(app,client):
    
    with app.app_context():
        from main import db
        db.create_all()
    
    add_row(**update_hackathon_dtst1)
    
    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["hasPrize"] == True #changes on update
    assert response_get1_before.json["prizeDetails"] == "500$" #changes on update
    
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_only_hasPrize_and_prizeDetails_correct)
    assert response_patch1.status_code == 200
    assert response_patch1.json["success"] == "Successfully updated hackathon with an id of : 1"
    
    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["name"] == "Hackathon1"
    assert response_get1_after.json["description"] == "Full Description"
    assert response_get1_after.json["url"] == "hack1.com"
    assert response_get1_after.json["startDate"] == "2027-01-02T01:03:00"
    assert response_get1_after.json["endDate"] == "2027-02-02T01:03:00"
    assert response_get1_after.json["location"] == "Kavala"
    assert response_get1_after.json["organizer"] == "UoA"
    assert response_get1_after.json["hasPrize"] == False #changes on update
    assert response_get1_after.json["prizeDetails"] == None #changes on update
    assert response_get1_after.json["tags"] == "AI,ML,Python"
    assert response_get1_after.json["status"] == "published"
    assert response_get1_after.json["mode"] == "online"

def test_update_hackathon_only_hasPrize_correct_bool_and_prizeDetails_wrong(app,client):
    with app.app_context():
        from main import db
        db.create_all()
    
    add_row(**update_hackathon_dtst1)
    
    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["hasPrize"] == True #changes on update
    assert response_get1_before.json["prizeDetails"] == "500$" #changes on update
    
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_only_hasPrize_correct_bool_and_prizeDetails_wrong)
    assert response_patch1.status_code == 200
    assert response_patch1.json["success"] == "Successfully updated hackathon with an id of : 1"
    
    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["name"] == "Hackathon1"
    assert response_get1_after.json["description"] == "Full Description"
    assert response_get1_after.json["url"] == "hack1.com"
    assert response_get1_after.json["startDate"] == "2027-01-02T01:03:00"
    assert response_get1_after.json["endDate"] == "2027-02-02T01:03:00"
    assert response_get1_after.json["location"] == "Kavala"
    assert response_get1_after.json["organizer"] == "UoA"
    assert response_get1_after.json["hasPrize"] == False #changes on update
    assert response_get1_after.json["prizeDetails"] == None #even though our dataset has prizeDetails set to 123 our backend will make it None since hasPrize is set to False
    assert response_get1_after.json["tags"] == "AI,ML,Python"
    assert response_get1_after.json["status"] == "published"
    assert response_get1_after.json["mode"] == "online"

def test_update_hackathon_only_hasPrize_correct_str_and_prizeDetails_correct(app,client):
    with app.app_context():
        from main import db
        db.create_all()
    
    add_row(**update_hackathon_dtst1)
    
    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["hasPrize"] == True #changes on update
    assert response_get1_before.json["prizeDetails"] == "500$" #changes on update
    
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_only_hasPrize_correct_str_and_prizeDetails_correct)
    assert response_patch1.status_code == 200
    assert response_patch1.json["success"] == "Successfully updated hackathon with an id of : 1"
    
    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["name"] == "Hackathon1"
    assert response_get1_after.json["description"] == "Full Description"
    assert response_get1_after.json["url"] == "hack1.com"
    assert response_get1_after.json["startDate"] == "2027-01-02T01:03:00"
    assert response_get1_after.json["endDate"] == "2027-02-02T01:03:00"
    assert response_get1_after.json["location"] == "Kavala"
    assert response_get1_after.json["organizer"] == "UoA"
    assert response_get1_after.json["hasPrize"] == False #changes on update
    assert response_get1_after.json["prizeDetails"] == None 
    assert response_get1_after.json["tags"] == "AI,ML,Python"
    assert response_get1_after.json["status"] == "published"
    assert response_get1_after.json["mode"] == "online"

def test_update_hackathon_only_hasPrize_correct_str_and_prizeDetails_wrong(app,client):
    with app.app_context():
        from main import db
        db.create_all()
    
    add_row(**update_hackathon_dtst1)
    
    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["hasPrize"] == True #changes on update
    assert response_get1_before.json["prizeDetails"] == "500$" #changes on update
    
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_only_hasPrize_correct_str_and_prizeDetails_wrong)
    assert response_patch1.status_code == 200
    assert response_patch1.json["success"] == "Successfully updated hackathon with an id of : 1"
    
    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["name"] == "Hackathon1"
    assert response_get1_after.json["description"] == "Full Description"
    assert response_get1_after.json["url"] == "hack1.com"
    assert response_get1_after.json["startDate"] == "2027-01-02T01:03:00"
    assert response_get1_after.json["endDate"] == "2027-02-02T01:03:00"
    assert response_get1_after.json["location"] == "Kavala"
    assert response_get1_after.json["organizer"] == "UoA"
    assert response_get1_after.json["hasPrize"] == False #changes on update while being a str our backend makes sure it passes as bool value
    assert response_get1_after.json["prizeDetails"] == None #even though our dataset has prizeDetails set to 123 our backend will make it None since hasPrize is set to False
    assert response_get1_after.json["tags"] == "AI,ML,Python"
    assert response_get1_after.json["status"] == "published"
    assert response_get1_after.json["mode"] == "online"

def test_update_hackathon_only_hasPrize_none_and_prizeDetails_correct(app,client):
    with app.app_context():
        from main import db
        db.create_all()
    
    add_row(**update_hackathon_dtst1)
    
    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["hasPrize"] == True #changes on update
    assert response_get1_before.json["prizeDetails"] == "500$" #changes on update
    
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_only_hasPrize_none_and_prizeDetails_correct)
    assert response_patch1.status_code == 200
    assert response_patch1.json["success"] == "Successfully updated hackathon with an id of : 1"
    
    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["name"] == "Hackathon1"
    assert response_get1_after.json["description"] == "Full Description"
    assert response_get1_after.json["url"] == "hack1.com"
    assert response_get1_after.json["startDate"] == "2027-01-02T01:03:00"
    assert response_get1_after.json["endDate"] == "2027-02-02T01:03:00"
    assert response_get1_after.json["location"] == "Kavala"
    assert response_get1_after.json["organizer"] == "UoA"
    assert response_get1_after.json["hasPrize"] == True #does not change on update since its value in the dataset is None
    assert response_get1_after.json["prizeDetails"] == "123" #changes on update
    assert response_get1_after.json["tags"] == "AI,ML,Python"
    assert response_get1_after.json["status"] == "published"
    assert response_get1_after.json["mode"] == "online"
    
def test_update_hackathon_only_hasPrize_wrong_str_and_prizeDetails_correct(app,client):
    
    with app.app_context():
        from main import db
        db.create_all()
    
    add_row(**update_hackathon_dtst1)
    
    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["hasPrize"] == True #changes on update
    assert response_get1_before.json["prizeDetails"] == "500$" #changes on update
    
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_only_hasPrize_wrong_str_and_prizeDetails)
    assert response_patch1.status_code == 400
    assert response_patch1.json["error"] == "Wrong hasPrize"
    
    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["hasPrize"] == True #must not change on update
    assert response_get1_after.json["prizeDetails"] == "500$" #must not change on update

def test_update_hackathon_only_startDate_and_endDate_correct(app,client):
    with app.app_context():
        from main import db
        db.create_all()
    
    add_row(**update_hackathon_dtst1)
    
    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["startDate"] == "2027-01-02T01:03:00" #changes on update
    assert response_get1_before.json["endDate"] == "2027-02-02T01:03:00" #changes on update
    
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_only_startDate_and_endDate_correct)
    assert response_patch1.status_code == 200
    assert response_patch1.json["success"] == "Successfully updated hackathon with an id of : 1"
    
    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["name"] == "Hackathon1"
    assert response_get1_after.json["description"] == "Full Description"
    assert response_get1_after.json["url"] == "hack1.com"
    assert response_get1_after.json["startDate"] == "2028-01-02T01:03:00" #changes on update
    assert response_get1_after.json["endDate"] == "2028-02-02T01:03:00" #chages on update
    assert response_get1_after.json["location"] == "Kavala"
    assert response_get1_after.json["organizer"] == "UoA"
    assert response_get1_after.json["hasPrize"] == True
    assert response_get1_after.json["prizeDetails"] == "500$" 
    assert response_get1_after.json["tags"] == "AI,ML,Python"
    assert response_get1_after.json["status"] == "published"
    assert response_get1_after.json["mode"] == "online"

def test_update_hackathon_only_startDate_wrong_and_endDate_correct(app,client):
    with app.app_context():
        from main import db
        db.create_all()
    
    add_row(**update_hackathon_dtst1)
    
    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["startDate"] == "2027-01-02T01:03:00" 
    assert response_get1_before.json["endDate"] == "2027-02-02T01:03:00" 
    
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_only_startDate_wrong_and_endDate_correct)
    assert response_patch1.status_code == 400
    assert response_patch1.json["error"] == "Wrong date format"
    
    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["startDate"] == "2027-01-02T01:03:00" #must not change on update
    assert response_get1_after.json["endDate"] == "2027-02-02T01:03:00" #must not change on update

def test_update_hackathon_only_startDate_correct_and_endDate_wrong(app,client):
    with app.app_context():
        from main import db
        db.create_all()
    
    add_row(**update_hackathon_dtst1)
    
    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["startDate"] == "2027-01-02T01:03:00" 
    assert response_get1_before.json["endDate"] == "2027-02-02T01:03:00" 
    
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_only_startDate_correct_and_endDate_wrong)
    assert response_patch1.status_code == 400
    assert response_patch1.json["error"] == "Wrong date format"
    
    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["startDate"] == "2027-01-02T01:03:00" #must not change on update
    assert response_get1_after.json["endDate"] == "2027-02-02T01:03:00" #must not change on update
    
def test_update_hackathon_only_startDate_and_endDate_wrong(app,client):
    with app.app_context():
        from main import db
        db.create_all()
    
    add_row(**update_hackathon_dtst1)
    
    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["startDate"] == "2027-01-02T01:03:00" 
    assert response_get1_before.json["endDate"] == "2027-02-02T01:03:00" 
    
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_only_startDate_and_endDate_wrong)
    assert response_patch1.status_code == 400
    assert response_patch1.json["error"] == "Wrong date format"
    
    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["startDate"] == "2027-01-02T01:03:00" #must not change on update
    assert response_get1_after.json["endDate"] == "2027-02-02T01:03:00" #must not change on update

def test_update_hackathon_only_interestCount_correct(app,client):
    with app.app_context():
        from main import db
        db.create_all()
    
    add_row(**update_hackathon_dtst1)
    
    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["interestCount"] == 0 #changes on update
    
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_only_interestCount_correct)
    assert response_patch1.status_code == 200
    assert response_patch1.json["success"] == "Successfully updated hackathon with an id of : 1"
    
    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["name"] == "Hackathon1"
    assert response_get1_after.json["description"] == "Full Description"
    assert response_get1_after.json["url"] == "hack1.com"
    assert response_get1_after.json["startDate"] == "2027-01-02T01:03:00" #changes on update
    assert response_get1_after.json["endDate"] == "2027-02-02T01:03:00" #chages on update
    assert response_get1_after.json["location"] == "Kavala"
    assert response_get1_after.json["organizer"] == "UoA"
    assert response_get1_after.json["hasPrize"] == True
    assert response_get1_after.json["prizeDetails"] == "500$" 
    assert response_get1_after.json["tags"] == "AI,ML,Python"
    assert response_get1_after.json["status"] == "published"
    assert response_get1_after.json["mode"] == "online"
    assert response_get1_after.json["interestCount"] == 15
    
def test_update_hackathon_only_interestCount_wrong_str(app,client):
    with app.app_context():
        from main import db
        db.create_all()
    
    add_row(**update_hackathon_dtst1)
    
    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["interestCount"] == 0 #changes on update
    
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_only_interestCount_wrong_str)
    assert response_patch1.status_code == 400
    assert response_patch1.json["error"] == "Wrong interestCount"
    
    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["interestCount"] == 0