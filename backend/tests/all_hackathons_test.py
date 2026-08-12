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
    "tags": "web",
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

    expected_names = []
    expected_urls = []
    for payload in base_payloads:
        expected_names.append(payload["name"])
        expected_urls.append(payload["url"])

    assert sorted(item["name"] for item in results.json) == sorted(expected_names)
    assert sorted(item["url"] for item in results.json) == sorted(expected_urls)


def test_get_hackathons_status_wrong_parameter_and_wrong_value(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?stat=invalid")
    assert results.status_code == 200
    assert len(results.json) == len(base_payloads)

    expected_names = []
    expected_urls = []
    for payload in base_payloads:
        expected_names.append(payload["name"])
        expected_urls.append(payload["url"])

    assert sorted(item["name"] for item in results.json) == sorted(expected_names)
    assert sorted(item["url"] for item in results.json) == sorted(expected_urls)


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


def test_get_hackathons_upcoming_wrong_parameter_and_correct_value(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?upco=true")
    assert results.status_code == 200
    assert len(results.json) == len(base_payloads)

    expected_names = []
    expected_urls = []
    for payload in base_payloads:
        expected_names.append(payload["name"])
        expected_urls.append(payload["url"])

    assert sorted(item["name"] for item in results.json) == sorted(expected_names)
    assert sorted(item["url"] for item in results.json) == sorted(expected_urls)


def test_get_hackathons_upcoming_wrong_parameter_and_wrong_value(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?upco=invalid")
    assert results.status_code == 200
    assert len(results.json) == len(base_payloads)

    expected_names = []
    expected_urls = []
    for payload in base_payloads:
        expected_names.append(payload["name"])
        expected_urls.append(payload["url"])

    assert sorted(item["name"] for item in results.json) == sorted(expected_names)
    assert sorted(item["url"] for item in results.json) == sorted(expected_urls)


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

def test_get_hackathons_upcoming_true_without_startDate_and_endDate(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client,contains_specific_payloads=True,specific_payloads=[base_payload2,base_payload7])

    results = client.get("/api/hackathons?upcoming=true")
    assert results.status_code == 200
    assert results.json == []
    
def test_get_hackathons_upcoming_false_without_startDate_and_endDate(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client,contains_specific_payloads=True,specific_payloads=[base_payload2,base_payload7])

    results = client.get("/api/hackathons?upcoming=false")
    assert results.status_code == 200
    assert results.json == []
    
## past param tests

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


def test_get_hackathons_past_wrong_parameter_and_correct_value(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?ps=true")
    assert results.status_code == 200
    assert len(results.json) == len(base_payloads)

    expected_names = []
    expected_urls = []
    for payload in base_payloads:
        expected_names.append(payload["name"])
        expected_urls.append(payload["url"])

    assert sorted(item["name"] for item in results.json) == sorted(expected_names)
    assert sorted(item["url"] for item in results.json) == sorted(expected_urls)


def test_get_hackathons_past_wrong_parameter_and_wrong_value(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?ps=invalid")
    assert results.status_code == 200
    assert len(results.json) == len(base_payloads)

    expected_names = []
    expected_urls = []
    for payload in base_payloads:
        expected_names.append(payload["name"])
        expected_urls.append(payload["url"])

    assert sorted(item["name"] for item in results.json) == sorted(expected_names)
    assert sorted(item["url"] for item in results.json) == sorted(expected_urls)


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

def test_get_hackathons_past_true_without_startDate_and_endDate(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client,contains_specific_payloads=True,specific_payloads=[base_payload2,base_payload7])

    results = client.get("/api/hackathons?past=true")
    assert results.status_code == 200
    assert results.json == []
    
def test_get_hackathons_past_false_without_startDate_and_endDate(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client,contains_specific_payloads=True,specific_payloads=[base_payload2,base_payload7])

    results = client.get("/api/hackathons?past=false")
    assert results.status_code == 200
    assert results.json == []



## tags param tests

def test_get_hackathons_tags_matches_multiple_tags(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?tags=python security")
    assert results.status_code == 200
    returned_names = [item["name"] for item in results.json]
    returned_urls = [item["url"] for item in results.json]
    assert sorted(returned_names) == sorted(["HackathonNoStatus", "HackathonNoMode"])
    assert sorted(returned_urls) == sorted(["hacknostatus.com", "hacknomode.com"])


def test_get_hackathons_tags_case_insensitive(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    for value in ["python", "PYTHON", "PyThOn"]:
        results = client.get(f"/api/hackathons?tags={value}")
        assert results.status_code == 200
        returned_names = [item["name"] for item in results.json]
        returned_urls = [item["url"] for item in results.json]
        assert sorted(returned_names) == sorted(["HackathonNoStatus"])
        assert sorted(returned_urls) == sorted(["hacknostatus.com"])


def test_get_hackathons_tags_no_matches(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?tags=NonExistentTag")
    assert results.status_code == 200
    assert results.json == []


def test_get_hackathons_tags_wrong_parameter_wrong_value(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?tag=invalid")
    assert results.status_code == 200
    assert len(results.json) == len(base_payloads)

    expected_names = [payload["name"] for payload in base_payloads]
    expected_urls = [payload["url"] for payload in base_payloads]
    assert sorted(item["name"] for item in results.json) == sorted(expected_names)
    assert sorted(item["url"] for item in results.json) == sorted(expected_urls)


def test_get_hackathons_tags_wrong_parameter_correct_value(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?tag=python")
    assert results.status_code == 200
    assert len(results.json) == len(base_payloads)

    expected_names = [payload["name"] for payload in base_payloads]
    expected_urls = [payload["url"] for payload in base_payloads]
    assert sorted(item["name"] for item in results.json) == sorted(expected_names)
    assert sorted(item["url"] for item in results.json) == sorted(expected_urls)


def test_get_hackathons_tags_empty_string(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?tags=")
    assert results.status_code == 200
    assert len(results.json) == len(base_payloads)


def test_get_hackathons_tags_with_last_value_search(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    for value in ["python", "pyth", "pYth"]:
        results = client.get(f"/api/hackathons?tags={value}")
        assert results.status_code == 200
        returned_names = [item["name"] for item in results.json]
        returned_urls = [item["url"] for item in results.json]
        assert sorted(returned_names) == sorted(["HackathonNoStatus"])
        assert sorted(returned_urls) == sorted(["hacknostatus.com"])


def test_get_hackathons_tags_partial_match_first_value(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?tags=data")
    assert results.status_code == 200
    returned_names = [item["name"] for item in results.json]
    returned_urls = [item["url"] for item in results.json]
    assert sorted(returned_names) == sorted(["HackathonNoStatus"])
    assert sorted(returned_urls) == sorted(["hacknostatus.com"])


def test_get_hackathons_tags_multi_word_tag(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?tags=web development")
    assert results.status_code == 200
    returned_names = [item["name"] for item in results.json]
    returned_urls = [item["url"] for item in results.json]
    assert sorted(returned_names) == sorted(["HackathonNoDates", "HackathonNoLocationTags"])
    assert sorted(returned_urls) == sorted(["hacknodates.com", "hacknolocationtags.com"])
    
def test_get_hackathons_tags_multi_word_tag_reversed(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?tags=development web")
    assert results.status_code == 200
    returned_names = [item["name"] for item in results.json]
    returned_urls = [item["url"] for item in results.json]
    assert sorted(returned_names) == sorted(["HackathonNoDates", "HackathonNoLocationTags"])
    assert sorted(returned_urls) == sorted(["hacknodates.com", "hacknolocationtags.com"])


def test_get_hackathons_tags_comma_separated_query(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?tags=ai,ml")
    assert results.status_code == 200
    returned_names = [item["name"] for item in results.json]
    returned_urls = [item["url"] for item in results.json]
    assert sorted(returned_names) == sorted(["HackathonFull1", "HackathonNoMode"])
    assert sorted(returned_urls) == sorted(["hackfull1.com", "hacknomode.com"])


def test_get_hackathons_tags_duplicate_param(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?tags=AI&tags=Python")
    assert results.status_code == 200
    returned_names = [item["name"] for item in results.json]
    returned_urls = [item["url"] for item in results.json]
    assert sorted(returned_names) == sorted(["HackathonFull1", "HackathonNoMode"])
    assert sorted(returned_urls) == sorted(["hackfull1.com", "hacknomode.com"])


## q param tests

def test_get_hackathons_q_matches_name(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?q=HackathonMinimal")
    assert results.status_code == 200
    returned_names = [item["name"] for item in results.json]
    returned_urls = [item["url"] for item in results.json]
    assert sorted(returned_names) == ["HackathonMinimal"]
    assert sorted(returned_urls) == ["hackminimal.com"]


def test_get_hackathons_q_matches_description(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?q=dates")
    assert results.status_code == 200
    returned_names = [item["name"] for item in results.json]
    returned_urls = [item["url"] for item in results.json]
    assert sorted(returned_names) == ["HackathonNoDates"]
    assert sorted(returned_urls) == ["hacknodates.com"]


def test_get_hackathons_q_matches_url(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?q=hackfull1")
    assert results.status_code == 200
    returned_names = [item["name"] for item in results.json]
    returned_urls = [item["url"] for item in results.json]
    assert sorted(returned_names) == ["HackathonFull1"]
    assert sorted(returned_urls) == ["hackfull1.com"]


def test_get_hackathons_q_matches_location(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?q=Athens")
    assert results.status_code == 200
    returned_names = [item["name"] for item in results.json]
    returned_urls = [item["url"] for item in results.json]
    assert sorted(returned_names) == ["HackathonFull1"]
    assert sorted(returned_urls) == ["hackfull1.com"]


def test_get_hackathons_q_matches_organizer(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?q=TechCorp")
    assert results.status_code == 200
    returned_names = [item["name"] for item in results.json]
    returned_urls = [item["url"] for item in results.json]
    assert sorted(returned_names) == ["HackathonFull1"]
    assert sorted(returned_urls) == ["hackfull1.com"]


def test_get_hackathons_q_matches_prizeDetails(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?q=2500")
    assert results.status_code == 200
    returned_names = [item["name"] for item in results.json]
    returned_urls = [item["url"] for item in results.json]
    assert sorted(returned_names) == ["HackathonNoStatus"]
    assert sorted(returned_urls) == ["hacknostatus.com"]


def test_get_hackathons_q_matches_tags(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?q=Blockchain")
    assert results.status_code == 200
    returned_names = [item["name"] for item in results.json]
    returned_urls = [item["url"] for item in results.json]
    assert sorted(returned_names) == ["HackathonNoMode"]
    assert sorted(returned_urls) == ["hacknomode.com"]


def test_get_hackathons_q_no_matches(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?q=qwertyuiopxyz")
    assert results.status_code == 200
    assert results.json == []


def test_get_hackathons_q_case_insesitive(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    for value in ["python", "PYTHON", "PyThOn"]:
        results = client.get(f"/api/hackathons?q={value}")
        assert results.status_code == 200
        returned_names = [item["name"] for item in results.json]
        returned_urls = [item["url"] for item in results.json]
        assert sorted(returned_names) == sorted(["HackathonNoStatus"])
        assert sorted(returned_urls) == sorted(["hacknostatus.com"])


def test_get_hackathons_q_wildcard_symbols_injected(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)
	# "_" underscore is evaluating as true due to tokenization fix in the future
    symbol_combos = ["!!!", "%%%", "^^^", "~~~", "***",
                     "()", "[]", "{}", "@@@", ";;;", ":::"]

    for symbols in symbol_combos:
        results = client.get(f"/api/hackathons?q={symbols}")
        assert results.status_code == 400
        assert results.json["error"] == "Wrong q"


def test_get_hackathons_q_empty_string(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?q=")
    assert results.status_code == 200
    assert len(results.json) == len(base_payloads)


def test_get_hackathons_q_and_operator_works(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    #both tokens exist in the payloads but each one belongs to a different hackathon
    #so the AND operator returns nothing
    results = client.get("/api/hackathons?q=TechCorp Blockchain")
    assert results.status_code == 200
    assert results.json == []


def test_get_hackathons_q_all_tokens_same_row(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    #both tokens exist in the same hackathon so the AND operator returns it
    results = client.get("/api/hackathons?q=Athens TechCorp")
    assert results.status_code == 200
    returned_names = [item["name"] for item in results.json]
    returned_urls = [item["url"] for item in results.json]
    assert sorted(returned_names) == sorted(["HackathonFull1"])
    assert sorted(returned_urls) == sorted(["hackfull1.com"])


def test_get_hackathons_q_duplicate_parameter(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    #only the first q value is used by the endpoint
    results = client.get("/api/hackathons?q=python&q=blockchain")
    assert results.status_code == 200
    returned_names = [item["name"] for item in results.json]
    returned_urls = [item["url"] for item in results.json]
    assert sorted(returned_names) == sorted(["HackathonNoStatus"])
    assert sorted(returned_urls) == sorted(["hacknostatus.com"])


def test_get_hackathons_q_wrong_parameter(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?query=python")
    assert results.status_code == 200
    assert len(results.json) == len(base_payloads)

    expected_names = [payload["name"] for payload in base_payloads]
    expected_urls = [payload["url"] for payload in base_payloads]
    assert sorted(item["name"] for item in results.json) == sorted(expected_names)
    assert sorted(item["url"] for item in results.json) == sorted(expected_urls)


# def test_get_hackathons_q_very_large_str(app, client):
#     #TODO: prevent very large values - will be fixed later
#     with app.app_context():
#         from main import db
#         db.create_all()
#
#     post_all_base_payloads(client)
#
#     results = client.get("/api/hackathons?q=" + "a" * 100000)
#     assert results.status_code == 200
#     assert results.json == []


# def test_get_hackathons_q_very_large_int(app, client):
#     #TODO: prevent very large values - will be fixed later
#     with app.app_context():
#         from main import db
#         db.create_all()
#
#     post_all_base_payloads(client)
#
#     results = client.get("/api/hackathons?q=" + "1" * 100000)
#     assert results.status_code == 200
#     assert results.json == []


## sort param tests

def test_get_hackathons_sort_name(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?sort=name")
    assert results.status_code == 200

    expected_names = ["HackathonFull1", "HackathonMinimal", "HackathonNoDates", "HackathonNoLocTagsOrg",
                      "HackathonNoLocTagsOrgDesc", "HackathonNoLocationTags", "HackathonNoMode", "HackathonNoOrgDesc",
                      "HackathonNoPrize", "HackathonNoStatus"]
    expected_urls = ["hackfull1.com", "hackminimal.com", "hacknodates.com", "hacknolocorg.com",
                     "hacknolocdescorg.com", "hacknolocationtags.com", "hacknomode.com", "hacknoorgdesc.com",
                     "hacknoprize.com", "hacknostatus.com"]

    assert [item["name"] for item in results.json] == expected_names
    assert [item["url"] for item in results.json] == expected_urls


def test_get_hackathons_sort_startDate(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?sort=startDate")
    assert results.status_code == 200

    expected_names = ["HackathonNoDates", "HackathonMinimal", "HackathonNoPrize", "HackathonNoStatus",
                      "HackathonNoOrgDesc", "HackathonNoLocTagsOrgDesc", "HackathonNoLocationTags",
                      "HackathonNoMode", "HackathonNoLocTagsOrg", "HackathonFull1"]
    expected_urls = ["hacknodates.com", "hackminimal.com", "hacknoprize.com", "hacknostatus.com",
                     "hacknoorgdesc.com", "hacknolocdescorg.com", "hacknolocationtags.com",
                     "hacknomode.com", "hacknolocorg.com", "hackfull1.com"]

    assert [item["name"] for item in results.json] == expected_names
    assert [item["url"] for item in results.json] == expected_urls


def test_get_hackathons_sort_endDate(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?sort=endDate")
    assert results.status_code == 200

    expected_names = ["HackathonNoDates", "HackathonMinimal", "HackathonNoPrize", "HackathonNoStatus",
                      "HackathonNoOrgDesc", "HackathonNoLocTagsOrgDesc", "HackathonNoLocationTags",
                      "HackathonNoMode", "HackathonNoLocTagsOrg", "HackathonFull1"]
    expected_urls = ["hacknodates.com", "hackminimal.com", "hacknoprize.com", "hacknostatus.com",
                     "hacknoorgdesc.com", "hacknolocdescorg.com", "hacknolocationtags.com",
                     "hacknomode.com", "hacknolocorg.com", "hackfull1.com"]

    assert [item["name"] for item in results.json] == expected_names
    assert [item["url"] for item in results.json] == expected_urls


def test_get_hackathons_sort_submittedAt(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?sort=submittedAt")
    assert results.status_code == 200

    expected_names = ["HackathonFull1", "HackathonNoDates", "HackathonNoPrize", "HackathonNoStatus",
                      "HackathonNoMode", "HackathonNoOrgDesc", "HackathonMinimal", "HackathonNoLocationTags",
                      "HackathonNoLocTagsOrgDesc", "HackathonNoLocTagsOrg"]
    expected_urls = ["hackfull1.com", "hacknodates.com", "hacknoprize.com", "hacknostatus.com",
                     "hacknomode.com", "hacknoorgdesc.com", "hackminimal.com", "hacknolocationtags.com",
                     "hacknolocdescorg.com", "hacknolocorg.com"]

    assert [item["name"] for item in results.json] == expected_names
    assert [item["url"] for item in results.json] == expected_urls


def test_get_hackathons_sort_updatedAt(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?sort=updatedAt")
    assert results.status_code == 200

    expected_names = ["HackathonNoLocTagsOrg", "HackathonNoLocTagsOrgDesc", "HackathonNoLocationTags",
                      "HackathonMinimal", "HackathonNoOrgDesc", "HackathonNoMode", "HackathonNoStatus",
                      "HackathonNoPrize", "HackathonNoDates", "HackathonFull1"]
    expected_urls = ["hacknolocorg.com", "hacknolocdescorg.com", "hacknolocationtags.com",
                     "hackminimal.com", "hacknoorgdesc.com", "hacknomode.com", "hacknostatus.com",
                     "hacknoprize.com", "hacknodates.com", "hackfull1.com"]

    assert [item["name"] for item in results.json] == expected_names
    assert [item["url"] for item in results.json] == expected_urls


def test_get_hackathons_sort_interestCount(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    #interestCount is always set to 0 when a hackathon is added, so give each row a distinct value
    interest_counts = {1: 120, 2: 25, 3: 47, 4: 89, 5: 33, 6: 54, 7: 5, 8: 10, 9: 7, 10: 75}
    for hackathon_id, count in interest_counts.items():
        response_patch = client.patch(f"/api/hackathons/{hackathon_id}",data={"interestCount": count})
        assert response_patch.status_code == 200
        assert response_patch.json["success"] == f"Successfully updated hackathon with an id of : {hackathon_id}"
        
    results = client.get("/api/hackathons?sort=interestCount")
    assert results.status_code == 200

    expected_names = ["HackathonFull1", "HackathonNoStatus", "HackathonNoLocTagsOrg", "HackathonNoOrgDesc",
                      "HackathonNoPrize", "HackathonNoMode", "HackathonNoDates", "HackathonNoLocationTags",
                      "HackathonNoLocTagsOrgDesc", "HackathonMinimal"]
    expected_urls = ["hackfull1.com", "hacknostatus.com", "hacknolocorg.com", "hacknoorgdesc.com",
                     "hacknoprize.com", "hacknomode.com", "hacknodates.com", "hacknolocationtags.com",
                     "hacknolocdescorg.com", "hackminimal.com"]

    assert [item["name"] for item in results.json] == expected_names
    assert [item["url"] for item in results.json] == expected_urls


def test_get_hackathons_sort_interestCount_null_values_go_last(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    #leave HackathonMinimal(id=7) with interestCount None to check nulls sort last in descending order
    interest_counts = {1: 120, 2: 25, 3: 47, 4: 89, 5: 33, 6: 54, 8: 10, 9: 7, 10: 75}
    for hackathon_id, count in interest_counts.items():
        response_patch = client.patch(f"/api/hackathons/{hackathon_id}",data={"interestCount": count})
        assert response_patch.status_code == 200
        assert response_patch.json["success"] == f"Successfully updated hackathon with an id of : {hackathon_id}"

    results = client.get("/api/hackathons?sort=interestCount")
    assert results.status_code == 200

    expected_names = ["HackathonFull1", "HackathonNoStatus", "HackathonNoLocTagsOrg", "HackathonNoOrgDesc",
                      "HackathonNoPrize", "HackathonNoMode", "HackathonNoDates", "HackathonNoLocationTags",
                      "HackathonNoLocTagsOrgDesc", "HackathonMinimal"]
    expected_urls = ["hackfull1.com", "hacknostatus.com", "hacknolocorg.com", "hacknoorgdesc.com",
                     "hacknoprize.com", "hacknomode.com", "hacknodates.com", "hacknolocationtags.com",
                     "hacknolocdescorg.com", "hackminimal.com"]

    assert [item["name"] for item in results.json] == expected_names
    assert [item["url"] for item in results.json] == expected_urls
    
def test_get_hackathons_sort_uppercase_value(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    for value in ["Name", "NAME", "NaMe"]:
        results = client.get(f"/api/hackathons?sort={value}")
        assert results.status_code == 200
        assert len(results.json) == len(base_payloads)
        expected_names = ["HackathonFull1", "HackathonMinimal", "HackathonNoDates", "HackathonNoLocTagsOrg",
                      "HackathonNoLocTagsOrgDesc", "HackathonNoLocationTags", "HackathonNoMode", "HackathonNoOrgDesc",
                      "HackathonNoPrize", "HackathonNoStatus"]
        expected_urls = ["hackfull1.com", "hackminimal.com", "hacknodates.com", "hacknolocorg.com",
                     "hacknolocdescorg.com", "hacknolocationtags.com", "hacknomode.com", "hacknoorgdesc.com",
                     "hacknoprize.com", "hacknostatus.com"]
        assert [item["name"] for item in results.json] == expected_names
        assert [item["url"] for item in results.json] == expected_urls
        
def test_get_hackathons_sort_empty_string(app, client): 
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?sort=")
    assert results.status_code == 200
    assert len(results.json) == len(base_payloads)
    
    returned_names = sorted(item["name"] for item in results.json)
    returned_urls = sorted(item["url"] for item in results.json)
    expected_names = sorted(payload["name"] for payload in base_payloads)
    expected_urls = sorted(payload["url"] for payload in base_payloads)

    assert returned_names == expected_names
    assert returned_urls == expected_urls
    
def test_get_hackathons_sort_wrong_value(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?sort=invalid")
    assert results.status_code == 400
    assert results.json["error"] == "Wrong sort"

def test_get_hackathons_sort_wrong_parameter_and_correct_value(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?srot=name")
    assert results.status_code == 200
    assert len(results.json) == len(base_payloads)

    expected_names = [payload["name"] for payload in base_payloads]
    expected_urls = [payload["url"] for payload in base_payloads]
    assert sorted(item["name"] for item in results.json) == sorted(expected_names)
    assert sorted(item["url"] for item in results.json) == sorted(expected_urls)

def test_get_hackathons_sort_wrong_parameter_and_wrong_value(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    results = client.get("/api/hackathons?srot=invalid")
    assert results.status_code == 200
    assert len(results.json) == len(base_payloads)

    expected_names = [payload["name"] for payload in base_payloads]
    expected_urls = [payload["url"] for payload in base_payloads]
    assert sorted(item["name"] for item in results.json) == sorted(expected_names)
    assert sorted(item["url"] for item in results.json) == sorted(expected_urls)

def test_get_hackathons_sort_duplicate_param_first_name_second_interestCount(app, client):
    
    """
    since name is first in our sort request the sort will be based on it
    """
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    interest_counts = {1: 120, 2: 25, 3: 47, 4: 89, 5: 33, 6: 54, 7: 5, 8: 10, 9: 7, 10: 75}
    for hackathon_id, count in interest_counts.items():
        response_patch = client.patch(f"/api/hackathons/{hackathon_id}",data={"interestCount": count})
        assert response_patch.status_code == 200
        assert response_patch.json["success"] == f"Successfully updated hackathon with an id of : {hackathon_id}"
    
    results = client.get("/api/hackathons?sort=name&sort=interestCount")
    assert results.status_code == 200
    
    expected_names = ["HackathonFull1", "HackathonMinimal", "HackathonNoDates", "HackathonNoLocTagsOrg",
                      "HackathonNoLocTagsOrgDesc", "HackathonNoLocationTags", "HackathonNoMode", "HackathonNoOrgDesc",
                      "HackathonNoPrize", "HackathonNoStatus"]
    expected_urls = ["hackfull1.com", "hackminimal.com", "hacknodates.com", "hacknolocorg.com",
                     "hacknolocdescorg.com", "hacknolocationtags.com", "hacknomode.com", "hacknoorgdesc.com",
                     "hacknoprize.com", "hacknostatus.com"]

    assert [item["name"] for item in results.json] == expected_names
    assert [item["url"] for item in results.json] == expected_urls
    
def test_get_hackathons_sort_duplicate_param_first_interestCount_second_name(app, client):
    
    """
    since interestCount is first in our sort request the sort will be based on it
    """
    with app.app_context():
        from main import db
        db.create_all()

    post_all_base_payloads(client)

    interest_counts = {1: 120, 2: 25, 3: 47, 4: 89, 5: 33, 6: 54, 7: 5, 8: 10, 9: 7, 10: 75}
    for hackathon_id, count in interest_counts.items():
        response_patch = client.patch(f"/api/hackathons/{hackathon_id}",data={"interestCount": count})
        assert response_patch.status_code == 200
        assert response_patch.json["success"] == f"Successfully updated hackathon with an id of : {hackathon_id}"
    
    results = client.get("/api/hackathons?sort=interestCount&sort=name")
    assert results.status_code == 200
    
    expected_names = ["HackathonFull1", "HackathonNoStatus", "HackathonNoLocTagsOrg", "HackathonNoOrgDesc",
                      "HackathonNoPrize", "HackathonNoMode", "HackathonNoDates", "HackathonNoLocationTags",
                      "HackathonNoLocTagsOrgDesc", "HackathonMinimal"]
    expected_urls = ["hackfull1.com", "hacknostatus.com", "hacknolocorg.com", "hacknoorgdesc.com",
                     "hacknoprize.com", "hacknomode.com", "hacknodates.com", "hacknolocationtags.com",
                     "hacknolocdescorg.com", "hackminimal.com"]

    assert [item["name"] for item in results.json] == expected_names
    assert [item["url"] for item in results.json] == expected_urls