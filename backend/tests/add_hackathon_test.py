from datetime import datetime

# TESTING ADD HACKATHON API | ENDPOINT: /api/hackathons | METHOD: POST

def test_add_hackathon_response_body_and_status(app,client):
    """
    normal hackathon addition, only name and url values filled.
    """
    with app.app_context():
        from main import db
        db.create_all()
        
    response = client.post("/api/hackathons", data={
        "name":"Ioannis",
        "url":"https://ioannis.com"
        })
    assert response.status_code == 200  
    assert response.json["response"]["success"] == "Successfully added hackathon:Ioannis!"

def test_add_hackathon_response_body_and_status_when_name_is_none(app, client):
    """
    name is None
    """
    with app.app_context():
        from main import db
        db.create_all()
        
    response = client.post("/api/hackathons", data={
        "name":None,
        "url":"https://ioannis.com"
        })
    assert response.status_code == 400
    assert response.json["error"]["Missing Fields"] == "name and url are required."
    

def test_add_hackathon_response_body_and_status_when_name_and_url_is_none(app, client):
    
    """
    name and url are both None
    """
    
    with app.app_context():
        from main import db
        db.create_all()
        
    response = client.post("/api/hackathons", data={
        "name":None,
        "url":None
        })
    assert response.status_code == 400
    assert response.json["error"]["Missing Fields"] == "name and url are required."

def test_add_hackathon_response_and_status_code_dataset1(app, client):
    
    """
    dataset1: has normal values for all fields
    """
    
    dataset1 = {
        "name":"Nikos",
        "description": "Hackathon Description",
        "url":"nikos.com",
        "status": "draft",
        "mode": "hybrid",
        "location":"Drama, Greece",
        "startDate":"2027-03-02 13:00:00",
        "endDate" : "2027-03-04 18:00:00",
        "organizer": "Bybit",
        "hasPrize":"true",
        "prizeDetails":"1200$"
    }
    
    with app.app_context():
        from main import db
        db.create_all()
        
    response = client.post("/api/hackathons", data=dataset1)
    assert response.status_code == 200
    assert response.json["response"]["success"] == "Successfully added hackathon:Nikos!"

def test_add_hackathon_response_and_status_code_dataset2(app, client):
    
    """
    dataset2: has status None, mode normal, hasPrize False for all fields
    """
    
    dataset2 = {
        "name":"Lefteris",
        "description": "Hackathon Description",
        "url":"nikos.com",
        "status": None,
        "mode": "hybrid",
        "location":"Drama, Greece",
        "startDate":"2027-03-02 13:00:00",
        "endDate" : "2027-03-04 18:00:00",
        "organizer": "Bybit",
        "hasPrize":"False",
        "prizeDetails":"1200$"
    }
    
    with app.app_context():
        from main import db
        db.create_all()
        
    response = client.post("/api/hackathons", data=dataset2)
    assert response.status_code == 200
    assert response.json["response"]["success"] == "Successfully added hackathon:Lefteris!"


def test_add_hackathon_response_and_status_code_dataset3(app, client):
    
    """
    dataset3: has wrong status everything else normal
    """
    
    dataset3 = {
        "name":"Nikos",
        "description": "Hackathon Description",
        "url":"nikos.com",
        "status": "nope",
        "mode": None,
        "location":"Drama, Greece",
        "startDate":"2027-03-02 13:00:00",
        "endDate" : "2027-03-04 18:00:00",
        "organizer": "Bybit",
        "hasPrize":"False",
        "prizeDetails":"1200$"
    }
    
    with app.app_context():
        from main import db
        db.create_all()
        
    response = client.post("/api/hackathons", data=dataset3)
    assert response.status_code == 400
    assert response.json["error"]["error"] == "Wrong status"

def test_add_hackathon_response_and_status_code_dataset4(app, client):
    
    """
    dataset4: has wrong mode everything else normal
    """
    
    dataset4 = {
        "name":"Nikos",
        "description": "Hackathon Description",
        "url":"nikos.com",
        "status": None,
        "mode": "nope",
        "location":"Drama, Greece",
        "startDate":"2027-03-02 13:00:00",
        "endDate" : "2027-03-04 18:00:00",
        "organizer": "Bybit",
        "hasPrize":"False",
        "prizeDetails":"1200$"
    }
    
    with app.app_context():
        from main import db
        db.create_all()
        
    response = client.post("/api/hackathons", data=dataset4)
    assert response.status_code == 400
    assert response.json["error"]["error"] == "Wrong mode"
    
def test_add_hackathon_response_and_status_code_dataset5(app, client):
    
    """
    dataset3: has wrong mode everything else normal
    """
    
    dataset5 = {
        "name":"Nikos",
        "description": "Hackathon Description",
        "url":"nikos.com",
        "status": None,
        "mode": None,
        "location":"Drama, Greece",
        "startDate":"2027-03-02 13:00:00",
        "endDate" : "2027-03-04 18:00:00",
        "organizer": "Bybit",
        "hasPrize":"falsy", # hasPrize gets applied a .lower() func
        "prizeDetails":"1200$"
    }
    
    with app.app_context():
        from main import db
        db.create_all()
        
    response = client.post("/api/hackathons", data=dataset5)
    assert response.status_code == 400
    assert response.json["error"]["error"] == "Wrong hasPrize"

def test_add_hackathon_status_code_dataset6(app, client):
    
    """
    dataset6: has wrong startDate everything else normal
    """
    
    dataset6 = {
        "name":"Nikos",
        "description": "Hackathon Description",
        "url":"nikos.com",
        "status": None,
        "mode": None,
        "location":"Drama, Greece",
        "startDate":"1234567",
        "endDate" : "2027-03-04 18:00:00",
        "organizer": "Bybit",
        "hasPrize":None,
        "prizeDetails":"1200$"
    }
    
    with app.app_context():
        from main import db
        db.create_all()
        
    response = client.post("/api/hackathons", data=dataset6)
    assert response.status_code == 400
    assert response.json["error"]["error"] == "Wrong date format"


def test_add_hackathon_response_and_status_code_dataset7(app, client):
    
    """
    dataset7: has wrong status,wrong mode everything else normal
    """
    
    dataset7 = {
        "name":"Nikos",
        "description": "Hackathon Description",
        "url":"nikos.com",
        "status": "nope",
        "mode": "nope",
        "location":"Drama, Greece",
        "startDate":"2027-03-02 13:00:00",
        "endDate" : "2027-03-04 18:00:00",
        "organizer": "Bybit",
        "hasPrize":"False",
        "prizeDetails":"1200$"
    }
    
    with app.app_context():
        from main import db
        db.create_all()
        
    response = client.post("/api/hackathons", data=dataset7)
    assert response.status_code == 400
    assert response.json["error"]["error"] == "Wrong status" #'Wrong mode' wont be printed yet since it is validated after status in validate_parameters() func

def test_add_hackathon_response_and_status_code_dataset8(app, client):
    
    """
    dataset8: has wrong status,wrong hasPrize everything else normal
    """
    
    dataset8 = {
        "name":"Nikos",
        "description": "Hackathon Description",
        "url":"nikos.com",
        "status": "nope",
        "mode": None,
        "location":"Drama, Greece",
        "startDate":"2027-03-02 13:00:00",
        "endDate" : "2027-03-04 18:00:00",
        "organizer": "Bybit",
        "hasPrize":"bruuh",
        "prizeDetails":"1200$"
    }
    
    with app.app_context():
        from main import db
        db.create_all()
        
    response = client.post("/api/hackathons", data=dataset8)
    assert response.status_code == 400
    assert response.json["error"]["error"] == "Wrong status"

def test_add_hackathon_response_and_status_code_dataset9(app, client):
    
    """
    dataset9: has wrong endDate everything else normal
    """
    
    dataset9 = {
        "name":"Nikos",
        "description": "Hackathon Description",
        "url":"nikos.com",
        "status": "nope",
        "mode": None,
        "location":"Drama, Greece",
        "startDate":"2027-03-04 18:00:00",
        "endDate" : "wrong-format",
        "organizer": "Bybit",
        "hasPrize":"bruuh",
        "prizeDetails":"1200$"
    }
    
    with app.app_context():
        from main import db
        db.create_all()
        
    response = client.post("/api/hackathons", data=dataset9)
    assert response.status_code == 400
    assert response.json["error"]["error"] == "Wrong date format"

def test_add_hackathon_response_and_status_code_dataset10(app, client):
    
    """
    dataset10: tests updatedAt parameter
    """
    
    dataset10 = {
        "name":"Nikos",
        "description": "Hackathon Description",
        "url":"nikos.com",
        "status": None,
        "mode": None,
        "location":"Drama, Greece",
        "startDate":"2027-03-04 18:00:00",
        "endDate" : "2027-03-08 18:00:00",
        "organizer": "Bybit",
        "hasPrize":"False",
        "prizeDetails":None
    }
    
    with app.app_context():
        from main import db
        db.create_all()
    
    before = datetime.now().replace(microsecond=0)
    response1 = client.post("/api/hackathons", data=dataset10)
    after = datetime.now().replace(microsecond=0)
    
    assert response1.status_code == 200
    assert response1.json["response"]["success"] == "Successfully added hackathon:Nikos!"
    
    response2 = client.get("/api/hackathons/1")
    updatedAt_value = datetime.fromisoformat(response2.json["updatedAt"])
    submittedAt_value = datetime.fromisoformat(response2.json["submittedAt"])
    
    assert response2.status_code == 200
    assert response2.json["name"] == "Nikos"
    assert before <= updatedAt_value <= after
    assert before <= submittedAt_value <= after


def test_add_hackathon_response_and_status_code_dataset11(app, client):
    
    """
    dataset11: tests if updatedAt parameter is current even if user tries to set one himself
    """
    
    dataset11 = {
        "name":"Nikos",
        "description": "Hackathon Description",
        "url":"nikos.com",
        "status": None,
        "mode": None,
        "location":"Drama, Greece",
        "startDate":"2027-03-04 18:00:00",
        "endDate" : "2027-03-08 18:00:00",
        "organizer": "Bybit",
        "hasPrize":"False",
        "prizeDetails":None,
        "updatedAt": "2023-03-08 12:00:00",
        "submittedAt": "2023-03-08 12:00:00"
    }
    
    with app.app_context():
        from main import db
        db.create_all()
    
    before = datetime.now().replace(microsecond=0)
    response1 = client.post("/api/hackathons", data=dataset11)
    after = datetime.now().replace(microsecond=0)
    
    assert response1.status_code == 200
    assert response1.json["response"]["success"] == "Successfully added hackathon:Nikos!"
    
    response2 = client.get("/api/hackathons/1")
    updatedAt_value = datetime.fromisoformat(response2.json["updatedAt"])
    submittedAt_value = datetime.fromisoformat(response2.json["submittedAt"])
    
    assert response2.status_code == 200
    assert response2.json["name"] == "Nikos"
    assert before <= updatedAt_value <= after
    assert before <= submittedAt_value <= after

def test_add_hackathon_response_and_status_code_dataset12(app, client):
    
    """
    dataset3: tests if prizeDetails remains None even if user tries to pass a value
              in prizeDetails when hasPrize is already False
    """
    
    dataset5 = {
        "name":"Nikos",
        "description": "Hackathon Description",
        "url":"nikos.com",
        "status": None,
        "mode": None,
        "location":"Drama, Greece",
        "startDate":"2027-03-02 13:00:00",
        "endDate" : "2027-03-04 18:00:00",
        "organizer": "Bybit",
        "hasPrize":"False", # hasPrize gets applied a .lower() func
        "prizeDetails":"1200$"
    }
    
    with app.app_context():
        from main import db
        db.create_all()
        
    response1 = client.post("/api/hackathons", data=dataset5)
    response2 = client.get("/api/hackathons/1")
    assert response1.status_code == 200
    assert response1.json["response"]["success"] == "Successfully added hackathon:Nikos!"
    assert response2.status_code == 200
    assert response2.json["prizeDetails"] == None