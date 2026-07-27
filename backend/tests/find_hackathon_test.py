from dataset_tests import *
from utils import add_row
import time


def test_find_hackathon_with_normal_id_values(app,client):
    
    with app.app_context():
        from main import db
        db.create_all()
            
    add_row(**find_hackathon_dtst1)
    add_row(**find_hackathon_dtst2)
    add_row(**find_hackathon_dtst3)

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
            
    result_test1 = client.get("api/hackathons/5") #wrong id testcase
    assert result_test1.status_code == 404
    assert result_test1.json["error"] == "Wrong id"
    
    result_test2 = client.get("api/hackathons/abc") #wrong id testcase
    assert result_test2.status_code == 404
    assert result_test2.json["error"] == "Wrong id"
    
    result_test3 = client.get("api/hackathons/id=abc") #wrong id testcase
    assert result_test3.status_code == 404
    assert result_test3.json["error"] == "Wrong id"