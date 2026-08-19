#from dataset_tests import *
from utils import add_row
import time


base_payload1 = {
                "name": "Hackathon1",
                "description":None,
                "url": "hack1.com",
                "startDate": None,
                "endDate": None,
                "location": "Crete",
                "mode": None,
                "organizer": "BYBIT",
                "hasPrize": True,
                "prizeDetails": "1400$",
                "tags": None,
                "status": None,
                "submittedAt": None,
                "updatedAt": None,
                "interestCount": None,
                }

base_payload2 = {
                "name": "Hackathon2",
                "description":None,
                "url": "hack2.com",
                "startDate": None,
                "endDate": None,
                "location": None,
                "mode": None,
                "organizer": "Oracle",
                "hasPrize": False,
                "prizeDetails": None,
                "tags": None,
                "status": "pending",
                "submittedAt": None,
                "updatedAt": None,
                "interestCount": None,
                }

base_payload3 = {
                "name": "Hackathon3",
                "description":None,
                "url": "hack3.com",
                "startDate": "2027-01-02 01:03:00",
                "endDate": "2027-02-02 01:03:00",
                "location": "Kavala",
                "mode": None,
                "organizer": "UoA",
                "hasPrize": True,
                "prizeDetails": "Hundai Car",
                "tags": None,
                "status": "published",
                "submittedAt": None,
                "updatedAt": None,
                "interestCount": None,
                }

def get_payload_for_post(payload):
    return {key: value for key, value in payload.items() if value is not None}

def add_hackathon(client, payload):
    data = get_payload_for_post(payload)
    response = client.post("/api/hackathons", data=data)
    assert response.status_code == 200
    assert response.json["success"] == f"Successfully added hackathon:{payload['name']}!"



def test_find_hackathon_with_normal_id_values(app,client):
    
    with app.app_context():
        from main import db
        db.create_all()
            
    add_hackathon(client,base_payload1)
    add_hackathon(client,base_payload2)
    add_hackathon(client,base_payload3)

    result_test1 = client.get("api/hackathons/1") #dtst1
    assert result_test1.status_code == 200
    assert result_test1.json["name"] == "Hackathon1"
    assert result_test1.json["url"] == "hack1.com"
    assert result_test1.json["location"] == "Crete"
    assert result_test1.json["organizer"] == "BYBIT"
    assert result_test1.json["prizeDetails"] == "1400$"

    result_test2 = client.get("api/hackathons/2") #dtst2
    assert result_test2.status_code == 200
    assert result_test2.json["name"] == "Hackathon2"
    assert result_test2.json["url"] == "hack2.com"
    assert result_test2.json["organizer"] == "Oracle"
    assert result_test2.json["status"] == "pending"
    
    result_test3 = client.get("api/hackathons/3") #dtst3
    assert result_test3.status_code == 200
    assert result_test3.json["name"] == "Hackathon3"
    assert result_test3.json["url"] == "hack3.com"
    assert result_test3.json["location"] == "Kavala"
    assert result_test3.json["organizer"] == "UoA"
    assert result_test3.json["prizeDetails"] == "Hundai Car"
    assert result_test3.json["status"] == "published"
    

def test_find_hackathon_with_wrong_id_values(app,client):
    
    with app.app_context():
        from main import db
        db.create_all()
        

    add_hackathon(client,
base_payload1)
    add_hackathon(client,
base_payload2)
    add_hackathon(client,base_payload3)
            
    result_test1 = client.get("api/hackathons/5") #wrong id testcase
    assert result_test1.status_code == 404
    assert result_test1.json["error"] == "Wrong id"
    
    result_test2 = client.get("api/hackathons/abc") #wrong id testcase
    assert result_test2.status_code == 400
    assert result_test2.json["error"] == "id must be a number"
    
    result_test3 = client.get("api/hackathons/id=abc") #wrong id testcase
    assert result_test3.status_code == 400
    assert result_test3.json["error"] == "id must be a number"