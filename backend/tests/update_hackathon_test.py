import time
from datetime import datetime
from dataset_tests import *
from utils import add_row,cleanup_db


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
    
def test_update_hackathon_without_id(app,client):
    with app.app_context():
        from main import db
        db.create_all()
    
    add_row(**update_hackathon_dtst1)
    
    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["name"] == "Hackathon1" #changes on update
    
    response_patch1 = client.patch("api/",data=update_hackathon_dtst1_on_updt_only_name) #we update only name
    assert response_patch1.status_code == 400
    assert response_patch1.json["error"] == "id is required"

def test_update_hackathon_with_empty_str_id(app,client):
    with app.app_context():
        from main import db
        db.create_all()
    
    add_row(**update_hackathon_dtst1)
    
    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["name"] == "Hackathon1" #changes on update
    
    response_patch1 = client.patch(f"api/{''}",data=update_hackathon_dtst1_on_updt_only_name) #we update only name
    assert response_patch1.status_code == 400
    assert response_patch1.json["error"] == "id is required"
    
def test_update_hackathon_with_wrong_non_numeric_id(app,client):
    with app.app_context():
        from main import db
        db.create_all()
            
    add_row(**update_hackathon_dtst1)
    
    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["name"] == "Hackathon1" #changes on update
    
    response_patch1 = client.patch("api/abc",data=update_hackathon_dtst1_on_updt_only_name) #we update only name
    assert response_patch1.status_code == 400
    assert response_patch1.json["error"] == "id must be a number"
    
def test_update_hackathon_with_non_existing_id(app,client):
    with app.app_context():
        from main import db
        db.create_all()
            
    add_row(**update_hackathon_dtst1)
    
    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["name"] == "Hackathon1" #changes on update
    
    response_patch1 = client.patch("api/1342",data=update_hackathon_dtst1_on_updt_only_name) #we update only name
    assert response_patch1.status_code == 404
    assert response_patch1.json["error"] == "Hackathon not found"
    
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
    assert response_get1_after.json["url"] == "hack1.com Changed" #changed on update

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

def test_update_hackathon_only_status_draft(app,client):
    
    with app.app_context():
        from main import db
        db.create_all()

    add_row(**update_hackathon_dtst1)

    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["status"] == "published" #changes on update

    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_only_status_draft)
    assert response_patch1.status_code == 200
    assert response_patch1.json["success"] == "Successfully updated hackathon with an id of : 1"

    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["status"] == "draft"
    
def test_update_hackathon_only_status_pending(app,client):
    
    with app.app_context():
        from main import db
        db.create_all()

    add_row(**update_hackathon_dtst1)

    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["status"] == "published" #changes on update

    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_only_status_pending)
    assert response_patch1.status_code == 200
    assert response_patch1.json["success"] == "Successfully updated hackathon with an id of : 1"

    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["status"] == "pending"
    
def test_update_hackathon_only_status_published(app,client):
    
    with app.app_context():
        from main import db
        db.create_all()

    add_row(**update_hackathon_dtst1)

    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["status"] == "published" #changes on update

    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_only_status_published)
    assert response_patch1.status_code == 200
    assert response_patch1.json["success"] == "Successfully updated hackathon with an id of : 1"

    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["status"] == "published"
    
def test_update_hackathon_only_status_needs_changes(app,client):
    
    with app.app_context():
        from main import db
        db.create_all()

    add_row(**update_hackathon_dtst1)

    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["status"] == "published" #changes on update

    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_only_status_needs_changes)
    assert response_patch1.status_code == 200
    assert response_patch1.json["success"] == "Successfully updated hackathon with an id of : 1"

    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["status"] == "needs-changes"
    
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
    
    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["status"] == "published" #must not change on update

def test_update_hackathon_only_mode_hybrid(app,client):
    with app.app_context():
        from main import db
        db.create_all()
    
    add_row(**update_hackathon_dtst1)
    
    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["mode"] == "online" #changes on update
    
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_only_mode_hybrid)
    assert response_patch1.status_code == 200
    assert response_patch1.json["success"] == "Successfully updated hackathon with an id of : 1"
    
    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["mode"] == "hybrid"
    
def test_update_hackathon_only_mode_in_person(app,client):
    with app.app_context():
        from main import db
        db.create_all()
    
    add_row(**update_hackathon_dtst1)
    
    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["mode"] == "online" #changes on update
    
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_only_mode_in_person)
    assert response_patch1.status_code == 200
    assert response_patch1.json["success"] == "Successfully updated hackathon with an id of : 1"
    
    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["mode"] == "in_person"
    
def test_update_hackathon_only_mode_online(app,client):
    with app.app_context():
        from main import db
        db.create_all()
    
    add_row(**update_hackathon_dtst1)
    
    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["mode"] == "online" #changes on update
    
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_only_mode_online)
    assert response_patch1.status_code == 200
    assert response_patch1.json["success"] == "Successfully updated hackathon with an id of : 1"
    
    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["mode"] == "online"
    
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
    
    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["mode"] == "online" #must not change on update
    

#________________testing1 with: hasPrize_true_and_prizeDetails_none _____________________________
def test_update_hackathon1_only_hasPrize_false_and_prizeDetails_none(app,client):
    with app.app_context():
        from main import db
        db.create_all()
    
    add_row(**update_hackathon_dtst1_hasPrize_true_and_prizeDetails_none)
    
    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["hasPrize"] == True #changes on update
    assert response_get1_before.json["prizeDetails"] == None #changes on update
    
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_hasPrize_false_and_prizeDetails_none)
    assert response_patch1.status_code == 200
    assert response_patch1.json["success"] == "Successfully updated hackathon with an id of : 1"
    
    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["hasPrize"] == False #changes on update
    assert response_get1_after.json["prizeDetails"] == None #changes on update

def test_update_hackathon1_only_hasPrize_false_and_prizeDetails_contain_value(app,client):
    with app.app_context():
        from main import db
        db.create_all()
    
    add_row(**update_hackathon_dtst1_hasPrize_true_and_prizeDetails_none)
    
    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["hasPrize"] == True #changes on update
    assert response_get1_before.json["prizeDetails"] == None #changes on update
    
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_hasPrize_false_and_prizeDetails_contain_value)
    assert response_patch1.status_code == 400
    assert response_patch1.json["error"] == "prizeDetails cannot contain any value when hasPrize is False"
    
    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["hasPrize"] == True #must not change on update
    assert response_get1_after.json["prizeDetails"] == None #muts not change on update
    
def test_update_hackathon1_only_hasPrize_none_and_prizeDetails_contain_value(app,client):
    with app.app_context():
        from main import db
        db.create_all()
    
    add_row(**update_hackathon_dtst1_hasPrize_true_and_prizeDetails_none)
    
    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["hasPrize"] == True #changes on update
    assert response_get1_before.json["prizeDetails"] == None #changes on update
    
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_hasPrize_none_and_prizeDetails_contain_value)
    assert response_patch1.status_code == 200
    assert response_patch1.json["success"] == "Successfully updated hackathon with an id of : 1"
    
    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["hasPrize"] == True #changes on update
    assert response_get1_after.json["prizeDetails"] == "1500$" #changes on update
#____________________________________________________________________________________

#________________testing2 with: hasPrize_false_and_prizeDetails_none _____________________________
    
def test_update_hackathon2_only_hasPrize_none_and_prizeDetails_contain_value(app,client):
    with app.app_context():
        from main import db
        db.create_all()
    
    add_row(**update_hackathon_dtst1_hasPrize_false_prizeDetails_none)
    
    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["hasPrize"] == False #changes on update
    assert response_get1_before.json["prizeDetails"] == None #changes on update
    
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_hasPrize_none_prizeDetails_contain_value)
    assert response_patch1.status_code == 400
    assert response_patch1.json["error"] == "prizeDetails cannot contain any value when hasPrize is False"
    
    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["hasPrize"] == False #changes on update
    assert response_get1_after.json["prizeDetails"] == None #changes on update    

def test_update_hackathon2_only_hasPrize_false_and_prizeDetails_contain_value(app,client):
    with app.app_context():
        from main import db
        db.create_all()
    
    add_row(**update_hackathon_dtst1_hasPrize_false_prizeDetails_none)
    
    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["hasPrize"] == False #changes on update
    assert response_get1_before.json["prizeDetails"] == None #changes on update
    
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_hasPrize_false_prizeDetails_contain_value)
    assert response_patch1.status_code == 400
    assert response_patch1.json["error"] == "prizeDetails cannot contain any value when hasPrize is False"
    
    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["hasPrize"] == False #changes on update
    assert response_get1_after.json["prizeDetails"] == None #changes on update    

def test_update_hackathon2_only_hasPrize_true_and_prizeDetails_none(app,client):
    with app.app_context():
        from main import db
        db.create_all()
    
    add_row(**update_hackathon_dtst1_hasPrize_false_prizeDetails_none)
    
    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["hasPrize"] == False #changes on update
    assert response_get1_before.json["prizeDetails"] == None #changes on update
    
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_hasPrize_true_prizeDetails_none)
    assert response_patch1.status_code == 200
    assert response_patch1.json["success"] == "Successfully updated hackathon with an id of : 1"
    
    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["hasPrize"] == True #changes on update
    assert response_get1_after.json["prizeDetails"] == None #changes on update    

def test_update_hackathon2_only_hasPrize_true_and_prizeDetails_contain_value(app,client):
    with app.app_context():
        from main import db
        db.create_all()
    
    add_row(**update_hackathon_dtst1_hasPrize_false_prizeDetails_none)
    
    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["hasPrize"] == False #changes on update
    assert response_get1_before.json["prizeDetails"] == None #changes on update
    
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_hasPrize_true_prizeDetails_contain_value)
    assert response_patch1.status_code == 200
    assert response_patch1.json["success"] == "Successfully updated hackathon with an id of : 1"
    
    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["hasPrize"] == True #changes on update
    assert response_get1_after.json["prizeDetails"] == "350$" #changes on update
    
#____________________________________________________________________________________

#________________testing3 with: hasPrize_none_and_prizeDetails_none _____________________________

def test_update_hackathon3_only_hasPrize_true_and_prizeDetails_none(app,client):
    with app.app_context():
        from main import db
        db.create_all()
    
    add_row(**update_hackathon_dtst1_hasPrize_none_prizeDetails_none)
    
    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["hasPrize"] == None #changes on update
    assert response_get1_before.json["prizeDetails"] == None #changes on update
    
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_hasPrize_true_and_prizeDetails_none)
    assert response_patch1.status_code == 200
    assert response_patch1.json["success"] == "Successfully updated hackathon with an id of : 1"
    
    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["hasPrize"] == True #changes on update
    assert response_get1_after.json["prizeDetails"] == None
    
def test_update_hackathon3_only_hasPrize_true_and_prizeDetails_contain_value(app,client):
    with app.app_context():
        from main import db
        db.create_all()
    
    add_row(**update_hackathon_dtst1_hasPrize_none_prizeDetails_none)
    
    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["hasPrize"] == None #changes on update
    assert response_get1_before.json["prizeDetails"] == None #changes on update
    
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_hasPrize_true_and_prizeDetails_contain_value)
    assert response_patch1.status_code == 200
    assert response_patch1.json["success"] == "Successfully updated hackathon with an id of : 1"
    
    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["hasPrize"] == True #changes on update
    assert response_get1_after.json["prizeDetails"] == "500$" #changes on update
    
def test_update_hackathon3_only_hasPrize_false_and_prizeDetails_none(app,client):
    with app.app_context():
        from main import db
        db.create_all()
    
    add_row(**update_hackathon_dtst1_hasPrize_none_prizeDetails_none)
    
    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["hasPrize"] == None #changes on update
    assert response_get1_before.json["prizeDetails"] == None #changes on update
    
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_hasPrize_false_and_prizeDetails_none)
    assert response_patch1.status_code == 200
    assert response_patch1.json["success"] == "Successfully updated hackathon with an id of : 1"
    
    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["hasPrize"] == False #changes on update
    assert response_get1_after.json["prizeDetails"] == None #changes on update
    
def test_update_hackathon3_only_hasPrize_false_and_prizeDetails_contain_value(app,client):
    with app.app_context():
        from main import db
        db.create_all()
    
    add_row(**update_hackathon_dtst1_hasPrize_none_prizeDetails_none)
    
    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["hasPrize"] == None #changes on update
    assert response_get1_before.json["prizeDetails"] == None #changes on update
    
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_hasPrize_false_and_prizeDetails_contain_value)
    assert response_patch1.status_code == 400
    assert response_patch1.json["error"] == "prizeDetails cannot contain any value when hasPrize is False"
    
    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["hasPrize"] == None #changes on update
    assert response_get1_after.json["prizeDetails"] == None #changes on update

#____________________________________________________________________________________

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
    assert response_patch1.status_code == 400
    assert response_patch1.json["error"] == "prizeDetails cannot contain any value when hasPrize is False"
    
    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["hasPrize"] == True #changes on update
    assert response_get1_after.json["prizeDetails"] == "500$" #even though our dataset has prizeDetails set to 123 our backend will make it None since hasPrize is set to False

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
    assert response_get1_after.json["hasPrize"] == False #changes on update
    assert response_get1_after.json["prizeDetails"] == None 

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
    assert response_patch1.status_code == 400
    assert response_patch1.json["error"] == "prizeDetails cannot contain any value when hasPrize is False"
    
    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["hasPrize"] == True #changes on update while being a str our backend makes sure it passes as bool value
    assert response_get1_after.json["prizeDetails"] == "500$" #even though our dataset has prizeDetails set to 123 our backend will make it None since hasPrize is set to False


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
    assert response_get1_after.json["hasPrize"] == True #does not change on update since its value in the dataset is None
    assert response_get1_after.json["prizeDetails"] == "123" #changes on update
    
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
    assert response_get1_after.json["startDate"] == "2028-01-02T01:03:00" #changes on update
    assert response_get1_after.json["endDate"] == "2028-02-02T01:03:00" #chages on update

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
    assert response_get1_after.json["interestCount"] == 0 #must not change after update

def test_update_hackathon_only_interestCount_correct_str(app,client):
    with app.app_context():
        from main import db
        db.create_all()
    
    add_row(**update_hackathon_dtst1)
    
    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["interestCount"] == 0 #changes on update
    
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_only_interestCount_correct_str)
    assert response_patch1.status_code == 200
    assert response_patch1.json["success"] == "Successfully updated hackathon with an id of : 1"
    
    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["interestCount"] == 15
    
def test_update_hackathon_only_interestCount_negative_int(app,client):
    with app.app_context():
        from main import db
        db.create_all()
    
    add_row(**update_hackathon_dtst1)
    
    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["interestCount"] == 0 #changes on update
    
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_only_interestCount_negative_int)
    assert response_patch1.status_code == 400
    assert response_patch1.json["error"] == "Wrong interestCount"

    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["interestCount"] == 0 #changes on update
    
def test_update_hackathon_only_interestCount_large_int(app,client):
    with app.app_context():
        from main import db
        db.create_all()
    
    add_row(**update_hackathon_dtst1)
    
    response_get1_before = client.get("api/hackathons/1")
    assert response_get1_before.status_code == 200
    assert response_get1_before.json["interestCount"] == 0 #changes on update
    
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_only_interestCount_large_int)
    assert response_patch1.status_code == 400
    assert response_patch1.json["error"] == "Wrong interestCount"

    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert response_get1_after.json["interestCount"] == 0 #changes on update

def test_update_hackathon_only_submittedAt_data_provided(app,client):
    
    """
    submittedAt value can NEVER be updated, its value is set only once in the post request
    thats why in last assert test we compare submittedAt (which hasnt changed) with
    before and after from above cause thats the case it should satisfy
    """
    with app.app_context():
        from main import db
        db.create_all()
    
    before = datetime.now().replace(microsecond=0)
    time.sleep(1)
    add_row(**update_hackathon_dtst1)
    time.sleep(1)
    after = datetime.now().replace(microsecond=0)
    
    response_get1_before = client.get("api/hackathons/1")
    submittedAt_value = datetime.fromisoformat(response_get1_before.json["submittedAt"])
    
    #Checking that submittedAt is correctly parsed
    assert response_get1_before.status_code == 200
    assert before <= submittedAt_value <= after
    
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_only_submittedAt_data_provided)
    assert response_patch1.status_code == 200
    assert response_patch1.json["success"] == "Successfully updated hackathon with an id of : 1"
    
    response_get1_after = client.get("api/hackathons/1")
    submittedAt_value_after_patch = datetime.fromisoformat(response_get1_after.json["submittedAt"])
    assert response_get1_after.status_code == 200
    assert before <= submittedAt_value_after_patch <= after
    
def test_update_hackathon_only_submittedAt_contain_value_data_provided(app,client):
    
    """
    submittedAt value can NEVER be updated, its value is set only once in the post request
    thats why in last assert test we compare submittedAt (which hasnt changed) with
    before and after from above cause thats the case it should satisfy, also we in our
    dataset submittedAt contains a value but submittedAt must not be updated At
    """
    with app.app_context():
        from main import db
        db.create_all()
    
    before = datetime.now().replace(microsecond=0)
    time.sleep(1)
    add_row(**update_hackathon_dtst1)
    time.sleep(1)
    after = datetime.now().replace(microsecond=0)
    
    response_get1_before = client.get("api/hackathons/1")
    submittedAt_value = datetime.fromisoformat(response_get1_before.json["submittedAt"])
    
    #Checking that submittedAt is correctly parsed
    assert response_get1_before.status_code == 200
    assert before <= submittedAt_value <= after
    
    #submittedAt in the dataset has a value of -> "submittedAt": "2020-01-02 01:00:00"
    #and it must not be updated
    
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_only_submittedAt_contain_value_data_provided)
    assert response_patch1.status_code == 200
    assert response_patch1.json["success"] == "Successfully updated hackathon with an id of : 1"
    
    response_get1_after = client.get("api/hackathons/1")
    submittedAt_value_after_patch = datetime.fromisoformat(response_get1_after.json["submittedAt"])
    assert response_get1_after.status_code == 200
    assert before <= submittedAt_value_after_patch <= after
    
def test_update_hackathon_only_updatedAt_data_provided(app,client):
    
    """
    updatedAt value alone cannot be updated,
    in order to test it we have to update some
    other fields as well (name,url...)
    if we try to patch a request with empty data
    it will throw a 400 No data provided to update error
    """
    
    with app.app_context():
        from main import db
        db.create_all()
    
    before = datetime.now().replace(microsecond=0)
    time.sleep(1)
    add_row(**update_hackathon_dtst1)
    time.sleep(1)
    after = datetime.now().replace(microsecond=0)
    
    response_get1_before = client.get("api/hackathons/1")
    updatedAt_value = datetime.fromisoformat(response_get1_before.json["updatedAt"])
    
    #Checking that submittedAt is correctly parsed
    assert response_get1_before.status_code == 200
    assert before <= updatedAt_value <= after
    
    before_patch = datetime.now().replace(microsecond=0)
    time.sleep(1)
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_only_updatedAt_data_provided)
    time.sleep(1)
    after_patch = datetime.now().replace(microsecond=0)
    
    assert response_patch1.status_code == 200
    assert response_patch1.json["success"] == "Successfully updated hackathon with an id of : 1"
    
    response_get1_after = client.get("api/hackathons/1")
    updatedAt_value_after_patch = datetime.fromisoformat(response_get1_after.json["updatedAt"])
    assert response_get1_after.status_code == 200
    assert before_patch <= updatedAt_value_after_patch <= after_patch
    
def test_update_hackathon_only_updatedAt_contain_value_data_provided(app,client):
    
    """
    updatedAt value alone cannot be updated, from the user in the request
    in order to test it we have to update some other fields as well
    if we try to patch a request with empty data it will throw a
    400 No data provided to update error
    """
    
    with app.app_context():
        from main import db
        db.create_all()
    
    before = datetime.now().replace(microsecond=0)
    time.sleep(1)
    add_row(**update_hackathon_dtst1)
    time.sleep(1)
    after = datetime.now().replace(microsecond=0)
    
    response_get1_before = client.get("api/hackathons/1")
    updatedAt_value = datetime.fromisoformat(response_get1_before.json["updatedAt"])
    
    #Checking that submittedAt is correctly parsed
    assert response_get1_before.status_code == 200
    assert before <= updatedAt_value <= after
    
    before_patch = datetime.now().replace(microsecond=0)
    time.sleep(1)
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_only_updatedAt_data_provided)
    time.sleep(1)
    after_patch = datetime.now().replace(microsecond=0)
    
    assert response_patch1.status_code == 200
    assert response_patch1.json["success"] == "Successfully updated hackathon with an id of : 1"
    
    #updatedAt in the dataset has a value of -> "updatedAt": "2020-02-01 05:00:02
    #and it must not be updated with that value
        
    response_get1_after = client.get("api/hackathons/1")
    updatedAt_value_after_patch = datetime.fromisoformat(response_get1_after.json["updatedAt"])
    assert response_get1_after.status_code == 200
    assert before_patch <= updatedAt_value_after_patch <= after_patch
    
def test_update_hackathon_only_when_data_NOT_provided(app,client):
    
    """
    When not data is being provided in the request and there is nothing
    to update, our backend serves a 400 error No data provided to update
    """
    
    with app.app_context():
        from main import db
        db.create_all()
    
    before = datetime.now().replace(microsecond=0)
    time.sleep(1)
    add_row(**update_hackathon_dtst1)
    time.sleep(1)
    after = datetime.now().replace(microsecond=0)
    
    response_get1_before = client.get("api/hackathons/1")
    submittedAt_value = datetime.fromisoformat(response_get1_before.json["submittedAt"])
    
    #Checking that submittedAt is correctly parsed
    assert response_get1_before.status_code == 200
    assert before <= submittedAt_value <= after
    
    response_patch1 = client.patch("api/1",data=update_hackathon_dtst1_on_updt_only_when_data_NOT_provided)
    assert response_patch1.status_code == 400
    assert response_patch1.json["error"] == "No data provided to update"
    
    response_get1_after = client.get("api/hackathons/1")
    assert response_get1_after.status_code == 200
    assert before <= submittedAt_value <= after