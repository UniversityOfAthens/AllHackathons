from datetime import datetime,timedelta
from utils import add_row,update_row
import time

# TESTING ALL HACKATHONS API | ENDPOINT: /api/hackathons | METHOD: GET

now = datetime.now().replace(microsecond=0)
next_year = now + timedelta(days=365)
next_year_plus_two_days = next_year + timedelta(days=2)
last_year = now - timedelta(days=365)
last_year_plus_two_days = last_year + timedelta(days=2)

def test_all_hackathons_while_adding_one_hackathon(app,client):
    hackathon1 = {
            "name":"Hackathon1",
            "url":"hack1.com",
        }
    
    with app.app_context():
            from main import db
            db.create_all()
            
    response1 = client.post("/api/hackathons", data=hackathon1)
    assert response1.status_code == 200
    assert response1.json["response"]["success"] == "Successfully added hackathon:Hackathon1!"
    
    #We are making sure that our post requests are valid and successfully reach our backend.
    
    results = client.get("/api/hackathons")
    assert results.status_code == 200
    assert results.json[0]["name"] == "Hackathon1"
    
def test_all_hackathons_while_adding_two_hackathons(app,client):
    hackathon1 = {
            "name":"Hackathon1",
            "url":"hack1.com",
        }
    
    hackathon2 = {
                "name":"Hackathon2",
                "url":"hack2.com",
            }
    
    with app.app_context():
            from main import db
            db.create_all()
            
    response1 = client.post("/api/hackathons", data=hackathon1)
    assert response1.status_code == 200
    assert response1.json["response"]["success"] == "Successfully added hackathon:Hackathon1!"
    
    response2 = client.post("/api/hackathons", data=hackathon2)
    assert response2.status_code == 200
    assert response2.json["response"]["success"] == "Successfully added hackathon:Hackathon2!"
    
    #We are making sure that our post requests are valid and successfully reach our backend.
    
    results = client.get("/api/hackathons")
    assert results.status_code == 200
    assert results.json[0]["name"] == "Hackathon1"
    assert results.json[1]["name"] == "Hackathon2"

def test_all_hackathons_with_wrong_and_right_status_parameter(app,client):
    
    hackathon1 = {
                "name":"Hackathon1",
                "url":"hack1.com",
                "status":"published"
            }
        
    hackathon2 = {
                "name":"Hackathon2",
                "url":"hack2.com",
                "status":"pending"
            }
        
    with app.app_context():
            from main import db
            db.create_all()
            
    response1 = client.post("/api/hackathons", data=hackathon1)
    assert response1.status_code == 200
    assert response1.json["response"]["success"] == "Successfully added hackathon:Hackathon1!"
    
    response2 = client.post("/api/hackathons", data=hackathon2)
    assert response2.status_code == 200
    assert response2.json["response"]["success"] == "Successfully added hackathon:Hackathon2!"
    
    result_test1 = client.get("/api/hackathons?status=published")
    assert result_test1.status_code == 200
    assert result_test1.json[0]["status"] == "published"
    
    result_test2 = client.get("/api/hackathons?status=pending")
    assert result_test2.status_code == 200
    assert result_test2.json[0]["status"] == "pending"
    
    result_test3 = client.get("/api/hackathons?status=something")
    assert result_test3.status_code == 404
    assert result_test3.json["error"] == "Wrong status"
    
def test_all_hackathons_with_wrong_and_right_upcoming_parameter(app,client):
    
    hackathon1 = {
                "name":"Hackathon1",
                "url":"hack1.com",
                "startDate":last_year,
                "endDate":last_year_plus_two_days
            }
        
    hackathon2 = {
                "name":"Hackathon2",
                "url":"hack2.com",
                "startDate":next_year,
                "endDate":next_year_plus_two_days
            }
        
    with app.app_context():
            from main import db
            db.create_all()
    
    response1 = client.post("/api/hackathons", data=hackathon1)
    assert response1.status_code == 200
    assert response1.json["response"]["success"] == "Successfully added hackathon:Hackathon1!"
    
    response2 = client.post("/api/hackathons", data=hackathon2)
    assert response2.status_code == 200
    assert response2.json["response"]["success"] == "Successfully added hackathon:Hackathon2!"

    result_test1 = client.get("api/hackathons?upcoming=True")
    assert result_test1.status_code == 200
    assert result_test1.json[0]["name"] == "Hackathon2"
    
    result_test2 = client.get("api/hackathons?upcoming=False")
    assert result_test2.status_code == 200
    assert result_test2.json[0]["name"] == "Hackathon1"
    
    result_test3 = client.get("api/hackathons?upcoming=something")
    assert result_test3.status_code == 404
    assert result_test3.json["error"] == "Wrong upcoming" 

def test_all_hackathons_with_wrong_and_right_past_parameter(app,client):
    
    hackathon1 = {
                "name":"Hackathon1",
                "url":"hack1.com",
                "startDate":last_year,
                "endDate":last_year_plus_two_days
            }
        
    hackathon2 = {
                "name":"Hackathon2",
                "url":"hack2.com",
                "startDate":next_year,
                "endDate":next_year_plus_two_days
            }
        
    with app.app_context():
            from main import db
            db.create_all()
    
    response1 = client.post("/api/hackathons", data=hackathon1)
    assert response1.status_code == 200
    assert response1.json["response"]["success"] == "Successfully added hackathon:Hackathon1!"
    
    response2 = client.post("/api/hackathons", data=hackathon2)
    assert response2.status_code == 200
    assert response2.json["response"]["success"] == "Successfully added hackathon:Hackathon2!"

    result_test1 = client.get("api/hackathons?past=True")
    assert result_test1.status_code == 200
    assert result_test1.json[0]["name"] == "Hackathon1"
    
    result_test2 = client.get("api/hackathons?past=False")
    assert result_test2.status_code == 200
    assert result_test2.json[0]["name"] == "Hackathon2"
    
    result_test3 = client.get("api/hackathons?past=something")
    assert result_test3.status_code == 404
    assert result_test3.json["error"] == "Wrong past"

def test_all_hackathons_tags_parameter(app,client):
    
    hackathon1 = {
                "name":"Hackathon1",
                "url":"hack1.com",
                "tags":"Web Development"
            }

    hackathon2 = {
                "name":"Hackathon2",
                "url":"hack2.com",
                "tags":"Cybersecurity"
            }
    
    with app.app_context():
        from main import db
        db.create_all()
    
    response1 = client.post("/api/hackathons", data=hackathon1)
    assert response1.status_code == 200
    assert response1.json["response"]["success"] == "Successfully added hackathon:Hackathon1!"

    response2 = client.post("/api/hackathons", data=hackathon2)
    assert response2.status_code == 200
    assert response2.json["response"]["success"] == "Successfully added hackathon:Hackathon2!"

    result_test1 = client.get("/api/hackathons?tags=Web Development")
    assert result_test1.status_code == 200
    assert result_test1.json[0]["name"] == "Hackathon1"
    assert result_test1.json[0]["tags"] == "Web Development"

    result_test2 = client.get("/api/hackathons?tags=Cybersecurity")
    assert result_test2.status_code == 200
    assert result_test2.json[0]["name"] == "Hackathon2"
    assert result_test2.json[0]["tags"] == "Cybersecurity"
    
    result_test3 = client.get("api/hackathons?tags=something")
    assert result_test3.status_code == 200
    assert result_test3.json == []
    
def test_all_hackathons_q_parameter(app,client):
    
    hackathon1 = {
                    "name":"Hackathon1",
                    "url":"hack1.com",
                    "description": "Another Description",
                    "location": "Kavala",
                    "tags":"Cybersecurity"
                }
    
    hackathon2 = {
                "name":"Hackathon2",
                "url":"hack2.com",
                "description": "Cool Description",
                "location": "Athens,Greece",
                "hasPrize":"true",
                "prizeDetails": "1500$",
                "tags":"AI,ML,Python"
            }
    
    hackathon3 = {
                    "name":"Hackathon3",
                    "url":"hack3.com",
                    "tags":"Cybersecurity",
                    "location":"Crete"
                }
    
    with app.app_context():
            from main import db
            db.create_all()
    
    response1 = client.post("/api/hackathons", data=hackathon1)
    assert response1.status_code == 200
    assert response1.json["response"]["success"] == "Successfully added hackathon:Hackathon1!"

    response2 = client.post("/api/hackathons", data=hackathon2)
    assert response2.status_code == 200
    assert response2.json["response"]["success"] == "Successfully added hackathon:Hackathon2!"
    
    response3 = client.post("/api/hackathons", data=hackathon3)
    assert response3.status_code == 200
    assert response3.json["response"]["success"] == "Successfully added hackathon:Hackathon3!"
    
    result_test1 = client.get("api/hackathons?q=Crete") #q for location test
    result_test2 = client.get("api/hackathons?q=ai") #q for tags test
    result_test3 = client.get("api/hackathons?q=1500") #q for prizeDetails test
    result_test4 = client.get("api/hackathons?q=hack3") #q for url test
    result_test5 = client.get("api/hackathons?q=athens") #q for location test 2
    result_test6 = client.get("api/hackathons?q=cybersecurity") #q for tags test 2 | should give us 2 results
    result_test7 = client.get("api/hackathons?q=cool") #q for description test
    result_test8 = client.get("api/hackathons?q=hackathon1") #q for name test
    
    
    assert result_test1.status_code == 200
    assert result_test1.json[0]["name"] == "Hackathon3"
    assert result_test1.json[0]["tags"] == "Cybersecurity"
    assert result_test1.json[0]["location"] == "Crete"
    assert result_test1.json[0]["url"] == "hack3.com"
    
    assert result_test2.status_code == 200
    assert result_test2.json[0]["name"] == "Hackathon2"
    assert result_test2.json[0]["prizeDetails"] == "1500$"
    assert result_test2.json[0]["location"] == "Athens,Greece"
    assert result_test2.json[0]["description"] == "Cool Description"
    assert result_test2.json[0]["url"] == "hack2.com"
    
    assert result_test3.status_code == 200
    assert result_test3.json[0]["name"] == "Hackathon2"
    assert result_test3.json[0]["prizeDetails"] == "1500$"
    assert result_test3.json[0]["location"] == "Athens,Greece"
    assert result_test3.json[0]["description"] == "Cool Description"
    assert result_test3.json[0]["url"] == "hack2.com"
    
    assert result_test4.status_code == 200
    assert result_test4.json[0]["name"] == "Hackathon3"
    assert result_test4.json[0]["tags"] == "Cybersecurity"
    assert result_test4.json[0]["location"] == "Crete"
    assert result_test4.json[0]["url"] == "hack3.com"
    
    assert result_test5.status_code == 200
    assert result_test5.json[0]["name"] == "Hackathon2"
    assert result_test5.json[0]["prizeDetails"] == "1500$"
    assert result_test5.json[0]["location"] == "Athens,Greece"
    assert result_test5.json[0]["description"] == "Cool Description"
    assert result_test5.json[0]["url"] == "hack2.com"
    
        
    assert result_test6.status_code == 200
    assert result_test6.json[1]["name"] == "Hackathon3"
    assert result_test6.json[1]["tags"] == "Cybersecurity"
    assert result_test6.json[1]["location"] == "Crete"
    assert result_test6.json[1]["url"] == "hack3.com"
    
    assert result_test6.json[0]["name"] == "Hackathon1"
    assert result_test6.json[0]["tags"] == "Cybersecurity"
    assert result_test6.json[0]["location"] == "Kavala"
    assert result_test6.json[0]["description"] == "Another Description"
    assert result_test6.json[0]["url"] == "hack1.com"
    
    assert result_test7.status_code == 200
    assert result_test7.json[0]["name"] == "Hackathon2"
    assert result_test7.json[0]["prizeDetails"] == "1500$"
    assert result_test7.json[0]["location"] == "Athens,Greece"
    assert result_test7.json[0]["description"] == "Cool Description"
    assert result_test7.json[0]["url"] == "hack2.com"
    
    assert result_test8.json[0]["name"] == "Hackathon1"
    assert result_test8.json[0]["tags"] == "Cybersecurity"
    assert result_test8.json[0]["location"] == "Kavala"
    assert result_test8.json[0]["description"] == "Another Description"
    assert result_test8.json[0]["url"] == "hack1.com"
    
def test_all_hackathons_sort_parameter(app,client):
    
    hackathon1 = {
                "name":"Hackathon1",
                "url":"hack1.com",
                "startDate":"2024-06-02 15:00:00",
                "endDate":"2024-06-05 18:00:00"
                }
		
    hackathon2 = {
				"name":"Hackathon2",
				"url":"hack2.com",
                "startDate":"2026-08-03 15:00:00",
                "endDate":"2026-09-07 12:00:00"
			    }
	
    hackathon3 = {
                "name":"Hackathon3",
                "url":"hack3.com",
                "startDate":"2027-10-05 12:00:00",
                "endDate":"2027-10-07 12:00:00"
				}
    
    kwargs1 = {
                    "name": "Ioannis",
                    "description":None,
                    "url": "ioannis.com",
                    "startDate": None,
                    "endDate": None,
                    "location": None,
                    "mode": None,
                    "organizer": "BYBIT",
                    "hasPrize": True,
                    "prizeDetails": "1400$",
                    "tags": "None",
                    "status": None,
                    "submittedAt": None,
                    "updatedAt": None,
                    "interestCount": None,
                }
        
    kwargs2 = {
                "name": "Kostas",
                "description":None,
                "url": "kostas.com",
                "startDate": None,
                "endDate": None,
                "location": None,
                "mode": None,
                "organizer": "BYBIT",
                "hasPrize": True,
                "prizeDetails": "1400$",
                "tags": "None",
                "status": None,
                "submittedAt": None,
                "updatedAt": None,
                "interestCount": None,
            }
    
    kwargs3 = {
                "name": "Nikos",
                "description":None,
                "url": "nikos.com",
                "startDate": None,
                "endDate": None,
                "location": None,
                "mode": None,
                "organizer": "BYBIT",
                "hasPrize": True,
                "prizeDetails": "1400$",
                "tags": "None",
                "status": None,
                "submittedAt": None,
                "updatedAt": None,
                "interestCount": None,
            }
    
    kwargs4 = {
                "name": "Fotis",
                "description":None,
                "url": "fotis.com",
                "startDate": None,
                "endDate": None,
                "location": None,
                "mode": None,
                "organizer": "BYBIT",
                "hasPrize": True,
                "prizeDetails": "1400$",
                "tags": "None",
                "status": None,
                "submittedAt": None,
                "updatedAt": None,
                "interestCount": None,
            }
    
    kwargs5 = {
                "name": "George",
                "description":None,
                "url": "george.com",
                "startDate": None,
                "endDate": None,
                "location": None,
                "mode": None,
                "organizer": "BYBIT",
                "hasPrize": True,
                "prizeDetails": "1400$",
                "tags": "None",
                "status": None,
                "submittedAt": None,
                "updatedAt": None,
                "interestCount": None,
            }
    
    with app.app_context():
        from main import db,Hackathon
        db.create_all()
    
    response1 = client.post("api/hackathons",data=hackathon1)
    assert response1.status_code == 200
    assert response1.json["response"]["success"] == "Successfully added hackathon:Hackathon1!"
    
    response2 = client.post("api/hackathons",data=hackathon2)
    assert response2.status_code == 200
    assert response2.json["response"]["success"] == "Successfully added hackathon:Hackathon2!"
        
    response3 = client.post("api/hackathons",data=hackathon3)
    assert response3.status_code == 200
    assert response3.json["response"]["success"] == "Successfully added hackathon:Hackathon3!"

    with app.app_context():
        from main import db,Hackathon
        hackathon_to_update1 = db.get_or_404(Hackathon,1)
        hackathon_to_update1.interestCount = 4
        
        hackathon_to_update2 = db.get_or_404(Hackathon,2)
        hackathon_to_update2.interestCount = 17

        hackathon_to_update3 = db.get_or_404(Hackathon,3)
        hackathon_to_update3.interestCount = 67
                
        db.session.commit()
            
    result_test1 = client.get("api/hackathons?sort=name")
    assert result_test1.status_code == 200
    assert result_test1.json[0]["name"] == "Hackathon1"
    assert result_test1.json[0]["url"] == "hack1.com"
    assert result_test1.json[1]["name"] == "Hackathon2"
    assert result_test1.json[1]["url"] == "hack2.com"
    assert result_test1.json[2]["name"] == "Hackathon3"
    assert result_test1.json[2]["url"] == "hack3.com"
    
    result_test2 = client.get("api/hackathons?sort=startDate")
    assert result_test2.status_code == 200
    assert result_test1.status_code == 200
    assert result_test1.json[0]["name"] == "Hackathon1"
    assert result_test1.json[0]["url"] == "hack1.com"
    assert result_test1.json[1]["name"] == "Hackathon2"
    assert result_test1.json[1]["url"] == "hack2.com"
    assert result_test1.json[2]["name"] == "Hackathon3"
    assert result_test1.json[2]["url"] == "hack3.com"
    
    result_test3 = client.get("api/hackathons?sort=endDate")
    assert result_test3.status_code == 200
    assert result_test3.json[0]["name"] == "Hackathon1"
    assert result_test3.json[0]["url"] == "hack1.com"
    assert result_test3.json[1]["name"] == "Hackathon2"
    assert result_test3.json[1]["url"] == "hack2.com"
    assert result_test3.json[2]["name"] == "Hackathon3"
    assert result_test3.json[2]["url"] == "hack3.com"
    
    result_test4 = client.get("api/hackathons?sort=interestCount")
    assert result_test4.status_code == 200
    assert result_test4.json[0]["name"] == "Hackathon3"
    assert result_test4.json[0]["url"] == "hack3.com"
    assert result_test4.json[1]["name"] == "Hackathon2"
    assert result_test4.json[1]["url"] == "hack2.com"
    assert result_test4.json[2]["name"] == "Hackathon1"
    assert result_test4.json[2]["url"] == "hack1.com"
    
    result_test5 = client.get("api/hackathons?sort=submittedAt")
    assert result_test5.status_code == 200
    assert result_test5.json[0]["name"] == "Hackathon1"
    assert result_test5.json[0]["url"] == "hack1.com"
    assert result_test5.json[1]["name"] == "Hackathon2"
    assert result_test5.json[1]["url"] == "hack2.com"
    assert result_test5.json[2]["name"] == "Hackathon3"
    assert result_test5.json[2]["url"] == "hack3.com"

    
    update_row(id=1,**kwargs1) #firstly we update hackathon1
    time.sleep(2) #we need to wait at least 2 secs, otherwise updatedAt values have the same updatedAt time 
    update_row(id=3,**kwargs3) 
    time.sleep(2)
    update_row(id=2,**kwargs2) #lastly we update hackathon2 and sort=updatedAt will show this first since it was updated last
    time.sleep(2)
    add_row(**kwargs4)
    time.sleep(2)
    add_row(**kwargs5)
    
    result_test6 = client.get("api/hackathons?sort=updatedAt")
    assert result_test6.status_code == 200
    assert result_test6.json[0]["name"] == "George"
    assert result_test6.json[0]["url"] == "george.com"
    assert result_test6.json[1]["name"] == "Fotis"
    assert result_test6.json[1]["url"] == "fotis.com"
    assert result_test6.json[2]["name"] == "Kostas"
    assert result_test6.json[2]["url"] == "kostas.com"
    assert result_test6.json[3]["name"] == "Nikos"
    assert result_test6.json[3]["url"] == "nikos.com"
    assert result_test6.json[4]["name"] == "Ioannis"
    assert result_test6.json[4]["url"] == "ioannis.com"