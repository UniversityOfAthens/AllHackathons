from datetime import datetime,timedelta
#from backend.conftest import client
from utils import add_row,update_row
import time

# TESTING ALL HACKATHONS API | ENDPOINT: /api/hackathons | METHOD: GET

now = datetime.now()

def make_date_pair(days_from_now: int, duration_days: int = 2):
    start = now + timedelta(days=days_from_now)
    end = start + timedelta(days=duration_days)
    return start.strftime("%Y-%m-%d %H:%M:%S"), end.strftime("%Y-%m-%d %H:%M:%S")


base_payload1 = {
    "name": "HackathonFull1",
    "url": "hackfull1.com",
    "description": "Full payload with all fields",
    "organizer": "TechCorp",
    "status": "published",
    "mode": "online",
    "tags": "AI,ML",
    "startDate": make_date_pair(2200)[0],
    "endDate": make_date_pair(2200)[1],
    "location": "Athens,Greece",
    "hasPrize": "true",
    "prizeDetails": "5000$",
    "interestCount": 120,
}

base_payload2 = {
    "name": "HackathonNoDates",
    "url": "hacknodates.com",
    "description": "Payload without start and end dates",
    "organizer": "DevWorks",
    "status": "pending",
    "mode": "in_person",
    "tags": "Web Development,JavaScript",
    "startDate": None,
    "endDate": None,
    "location": "Thessaloniki,Greece",
    "hasPrize": "false",
    "prizeDetails": None,
    "interestCount": 25,
}

base_payload3 = {
    "name": "HackathonNoPrize",
    "url": "hacknoprize.com",
    "description": "Payload without prize fields",
    "organizer": "BuildIt",
    "status": "draft",
    "mode": "hybrid",
    "tags": "Startup,Design",
    "startDate": make_date_pair(-2200)[0],
    "endDate": make_date_pair(-2200)[1],
    "location": "Patras,Greece",
    "hasPrize": None,
    "prizeDetails": None,
    "interestCount": 47,
}

base_payload4 = {
    "name": "HackathonNoStatus",
    "url": "hacknostatus.com",
    "description": "Payload missing status",
    "organizer": "OpenLabs",
    "status": None,
    "mode": "online",
    "tags": "Data Science,Python",
    "startDate": make_date_pair(-90)[0],
    "endDate": make_date_pair(-90)[1],
    "location": "Ioannina,Greece",
    "hasPrize": "true",
    "prizeDetails": "2500$",
    "interestCount": 89,
}

base_payload5 = {
    "name": "HackathonNoMode",
    "url": "hacknomode.com",
    "description": "Payload missing mode",
    "organizer": "CodeSprint",
    "status": "needs_changes",
    "mode": None,
    "tags": "Blockchain,Security",
    "startDate": make_date_pair(90)[0],
    "endDate": make_date_pair(90)[1],
    "location": "Larisa,Greece",
    "hasPrize": "false",
    "prizeDetails": None,
    "interestCount": 33,
}

base_payload6 = {
    "name": "HackathonNoOrgDesc",
    "url": "hacknoorgdesc.com",
    "description": None,
    "organizer": None,
    "status": "published",
    "mode": "in_person",
    "tags": "Robotics,Engineering",
    "startDate": make_date_pair(-20)[0],
    "endDate": make_date_pair(-20)[1],
    "location": "Volos,Greece",
    "hasPrize": "true",
    "prizeDetails": "3000$",
    "interestCount": 54,
}

base_payload7 = {
    "name": "HackathonMinimal",
    "url": "hackminimal.com",
}

base_payload8 = {
    "name": "HackathonNoLocationTags",
    "url": "hacknolocationtags.com",
    "description": "Payload without location and tags",
    "organizer": "NextGen",
    "status": "pending",
    "mode": "online",
    "tags": None,
    "startDate": make_date_pair(20)[0],
    "endDate": make_date_pair(20)[1],
    "location": None,
    "hasPrize": "false",
    "prizeDetails": None,
    "interestCount": 10,
}

base_payload9 = {
    "name": "HackathonNoLocTagsOrgDesc",
    "url": "hacknolocdescorg.com",
    "description": None,
    "organizer": None,
    "status": "draft",
    "mode": "hybrid",
    "tags": None,
    "startDate": make_date_pair(-10)[0],
    "endDate": make_date_pair(-10)[1],
    "location": None,
    "hasPrize": "true",
    "prizeDetails": "1000$",
    "interestCount": 5,
}

base_payload10 = {
    "name": "HackathonNoLocTagsOrg",
    "url": "hacknolocorg.com",
    "description": "Payload without location, tags, and organizer",
    "organizer": None,
    "status": "published",
    "mode": "online",
    "tags": None,
    "startDate": make_date_pair(120)[0],
    "endDate": make_date_pair(120)[1],
    "location": None,
    "hasPrize": "false",
    "prizeDetails": None,
    "interestCount": 75,
}

base_payloads = [
    base_payload1,
    base_payload2,
    base_payload3,
    base_payload4,
    base_payload5,
    base_payload6,
    base_payload7,
    base_payload8,
    base_payload9,
    base_payload10,
]

def get_payload_for_post(payload):
    return {key: value for key, value in payload.items() if value is not None}


def assert_post_success(client, payload):
    response = client.post("/api/hackathons", data=get_payload_for_post(payload))
    assert response.status_code == 200
    assert response.json["success"] == f"Successfully added hackathon:{payload['name']}!"
    return response

def post_all_base_payloads(client,contains_specific_payloads: bool = False,specific_payloads: list = None):
    #in case we want to test a no results value
    if contains_specific_payloads:
        for payload in specific_payloads:
            assert_post_success(client, payload)
    else:
        for payload in base_payloads:
            assert_post_success(client, payload)

def test_get_hackathons_no_params_returns_all(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons")
    assert results.status_code == 200
    assert len(results.json) == len(base_payloads)

    returned_names = sorted(item["name"] for item in results.json)
    returned_urls = sorted(item["url"] for item in results.json)
    expected_names = sorted(payload["name"] for payload in base_payloads)
    expected_urls = sorted(payload["url"] for payload in base_payloads)

    assert returned_names == expected_names
    assert returned_urls == expected_urls


def test_get_hackathons_status_wrong_value(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?status=invalid")
    assert results.status_code == 400
    assert results.json["error"] == "Wrong status"


def test_get_hackathons_status_is_draft_uppercase_value(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    for value in ["Draft", "DRAFT", "DRafT"]:
        results = client.get(f"/api/hackathons?status={value}")
        assert results.status_code == 200

        returned_names = [item["name"] for item in results.json]
        returned_urls = [item["url"] for item in results.json]
        assert sorted(returned_names) == sorted(["HackathonNoPrize", "HackathonNoLocTagsOrgDesc"])
        assert sorted(returned_urls) == sorted(["hacknoprize.com", "hacknolocdescorg.com"])

def test_get_hackathons_status_is_pending_uppercase_value(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    for value in ["Pending", "PENDING", "PeNdInG"]:
        results = client.get(f"/api/hackathons?status={value}")
        assert results.status_code == 200

        returned_names = [item["name"] for item in results.json]
        returned_urls = [item["url"] for item in results.json]
        assert sorted(returned_names) == sorted(["HackathonNoDates", "HackathonNoLocationTags"])
        assert sorted(returned_urls) == sorted(["hacknodates.com", "hacknolocationtags.com"])


def test_get_hackathons_status_is_published_uppercase_value(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    for value in ["Published", "PUBLISHED", "PuBlIsHeD"]:
        results = client.get(f"/api/hackathons?status={value}")
        assert results.status_code == 200

        returned_names = [item["name"] for item in results.json]
        returned_urls = [item["url"] for item in results.json]
        assert sorted(returned_names) == sorted(["HackathonFull1", "HackathonNoOrgDesc", "HackathonNoLocTagsOrg"])
        assert sorted(returned_urls) == sorted(["hackfull1.com", "hacknoorgdesc.com", "hacknolocorg.com"])


def test_get_hackathons_status_is_needs_changes_uppercase_value(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    for value in ["Needs_changes", "NEEDS_CHANGES", "NeEdS_cHaNgEs"]:
        results = client.get(f"/api/hackathons?status={value}")
        assert results.status_code == 200

        returned_names = [item["name"] for item in results.json]
        returned_urls = [item["url"] for item in results.json]
        assert sorted(returned_names) == sorted(["HackathonNoMode"])
        assert sorted(returned_urls) == sorted(["hacknomode.com"])


def test_get_hackathons_status_wrong_parameter_and_correct_value(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?stat=draft")
    assert results.status_code == 200
    assert len(results.json) == len(base_payloads)


def test_get_hackathons_status_wrong_parameter_and_wrong_value(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?stat=invalid")
    assert results.status_code == 200
    assert len(results.json) == len(base_payloads)


def test_get_hackathons_status_empty_string(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?status=")
    assert results.status_code == 200
    assert len(results.json) == len(base_payloads)


def test_get_hackathons_status_draft(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?status=draft")
    assert results.status_code == 200
    returned_names = [item["name"] for item in results.json]
    returned_urls = [item["url"] for item in results.json]
    assert sorted(returned_names) == sorted(["HackathonNoPrize", "HackathonNoLocTagsOrgDesc"])
    assert sorted(returned_urls) == sorted(["hacknoprize.com", "hacknolocdescorg.com"])


def test_get_hackathons_status_pending(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?status=pending")
    assert results.status_code == 200
    returned_names = [item["name"] for item in results.json]
    returned_urls = [item["url"] for item in results.json]
    assert sorted(returned_names) == sorted(["HackathonNoDates", "HackathonNoLocationTags"])
    assert sorted(returned_urls) == sorted(["hacknodates.com", "hacknolocationtags.com"])


def test_get_hackathons_status_published(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?status=published")
    assert results.status_code == 200
    returned_names = [item["name"] for item in results.json]
    returned_urls = [item["url"] for item in results.json]
    assert sorted(returned_names) == sorted(["HackathonFull1", "HackathonNoOrgDesc", "HackathonNoLocTagsOrg"])
    assert sorted(returned_urls) == sorted(["hackfull1.com", "hacknoorgdesc.com", "hacknolocorg.com"])


def test_get_hackathons_status_needs_changes(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?status=needs_changes")
    assert results.status_code == 200
    returned_names = [item["name"] for item in results.json]
    returned_urls = [item["url"] for item in results.json]
    print(type(returned_urls))
    assert sorted(returned_names) == sorted(["HackathonNoMode"])
    assert sorted(returned_urls) == sorted(["hacknomode.com"])
    
def test_get_hackathons_status_no_matches(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payloads_not_matching_status = [
        base_payload1,
        base_payload2,
        base_payload4,
        base_payload5,
        base_payload6,
        base_payload8,
        base_payload10,
    ]
    post_all_base_payloads(client, contains_specific_payloads=True, specific_payloads=payloads_not_matching_status)

    results = client.get("/api/hackathons?status=draft")
    assert results.status_code == 200
    assert results.json == []
    
def test_get_hackathons_status_duplicate_param(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?status=draft&status=published")
    assert results.status_code == 200

    returned_names = sorted(item["name"] for item in results.json)
    returned_urls = sorted(item["url"] for item in results.json)
    assert returned_names == sorted(["HackathonNoPrize", "HackathonNoLocTagsOrgDesc"])
    assert returned_urls == sorted(["hacknoprize.com", "hacknolocdescorg.com"])


## upcoming param tests

def test_get_hackathons_upcoming_true(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?upcoming=true")
    assert results.status_code == 200

    returned_names = [item["name"] for item in results.json]
    returned_urls = [item["url"] for item in results.json]
    assert sorted(returned_names) == sorted(["HackathonNoMode", "HackathonNoLocationTags", "HackathonNoLocTagsOrg", "HackathonFull1"])
    assert sorted(returned_urls) == sorted(["hacknomode.com", "hacknolocationtags.com", "hacknolocorg.com", "hackfull1.com"])


def test_get_hackathons_upcoming_false(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?upcoming=false")
    assert results.status_code == 200

    returned_names = [item["name"] for item in results.json]
    returned_urls = [item["url"] for item in results.json]
    assert sorted(returned_names) == sorted(["HackathonNoPrize", "HackathonNoStatus", "HackathonNoOrgDesc", "HackathonNoLocTagsOrgDesc"])
    assert sorted(returned_urls) == sorted(["hacknoprize.com", "hacknostatus.com", "hacknoorgdesc.com", "hacknolocdescorg.com"])


def test_get_hackathons_upcoming_wrong_value(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?upcoming=invalid")
    assert results.status_code == 400
    assert results.json["error"] == "Wrong upcoming"


def test_get_hackathons_upcoming_uppercase_true(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    for value in ["TRUE", "TruE", "True"]:
        results = client.get(f"/api/hackathons?upcoming={value}")
        assert results.status_code == 200
        returned_names = [item["name"] for item in results.json]
        returned_urls = [item["url"] for item in results.json]
        assert sorted(returned_names) == sorted(["HackathonNoMode", "HackathonNoLocationTags", "HackathonNoLocTagsOrg", "HackathonFull1"])
        assert sorted(returned_urls) == sorted(["hacknomode.com", "hacknolocationtags.com", "hacknolocorg.com", "hackfull1.com"])

def test_get_hackathons_upcoming_uppercase_false(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    for value in ["FALSE", "FalsE", "False"]:
        results = client.get(f"/api/hackathons?upcoming={value}")
        assert results.status_code == 200

        returned_names = ["HackathonNoPrize", "HackathonNoStatus", "HackathonNoOrgDesc", "HackathonNoLocTagsOrgDesc"]
        returned_urls = ["hacknoprize.com", "hacknostatus.com", "hacknoorgdesc.com", "hacknolocdescorg.com"]

        assert sorted(item["name"] for item in results.json) == sorted(returned_names)
        assert sorted(item["url"] for item in results.json) == sorted(returned_urls)

def test_get_hackathons_upcoming_empty_string(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?upcoming=")
    assert results.status_code == 200
    assert len(results.json) == len(base_payloads)


## upcoming param tests

def test_get_hackathons_past_true(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?past=true")
    assert results.status_code == 200

    returned_names = [item["name"] for item in results.json]
    returned_urls = [item["url"] for item in results.json]
    assert sorted(returned_names) == sorted(["HackathonNoPrize", "HackathonNoStatus", "HackathonNoOrgDesc", "HackathonNoLocTagsOrgDesc"])
    assert sorted(returned_urls) == sorted(["hacknoprize.com", "hacknostatus.com", "hacknoorgdesc.com", "hacknolocdescorg.com"])


def test_get_hackathons_past_false(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?past=false")
    assert results.status_code == 200

    returned_names = [item["name"] for item in results.json]
    returned_urls = [item["url"] for item in results.json]
    assert sorted(returned_names) == sorted(["HackathonNoMode", "HackathonNoLocationTags", "HackathonNoLocTagsOrg", "HackathonFull1"])
    assert sorted(returned_urls) == sorted(["hacknomode.com", "hacknolocationtags.com", "hacknolocorg.com", "hackfull1.com"])


def test_get_hackathons_past_wrong_value(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?past=invalid")
    assert results.status_code == 400
    assert results.json["error"] == "Wrong past"


def test_get_hackathons_past_uppercase_true(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    for value in ["TRUE", "TruE", "True"]:
        results = client.get(f"/api/hackathons?past={value}")
        assert results.status_code == 200
        returned_names = [item["name"] for item in results.json]
        returned_urls = [item["url"] for item in results.json]
        assert sorted(returned_names) == sorted(["HackathonNoPrize", "HackathonNoStatus", "HackathonNoOrgDesc", "HackathonNoLocTagsOrgDesc"])
        assert sorted(returned_urls) == sorted(["hacknoprize.com", "hacknostatus.com", "hacknoorgdesc.com", "hacknolocdescorg.com"])
    
def test_get_hackathons_past_uppercase_false(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    for value in ["FALSE", "FalsE", "False"]:
        results = client.get(f"/api/hackathons?past={value}")
        assert results.status_code == 200
        returned_names = [item["name"] for item in results.json]
        returned_urls = [item["url"] for item in results.json]
        assert sorted(returned_names) == sorted(["HackathonNoMode", "HackathonNoLocationTags", "HackathonNoLocTagsOrg", "HackathonFull1"])
        assert sorted(returned_urls) == sorted(["hacknomode.com", "hacknolocationtags.com", "hacknolocorg.com", "hackfull1.com"])

def test_get_hackathons_past_empty_string(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?past=")
    assert results.status_code == 200
    assert len(results.json) == len(base_payloads)