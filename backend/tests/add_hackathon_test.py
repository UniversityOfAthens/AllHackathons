# TESTING ADD HACKATHON API | ENDPOINT: /api/hackathons | METHOD: POST
from datetime import datetime
import time

TIME_SLEEP_DURATION = 1 

base_payload = {
    "name": "Hackathon1",
    "url": "hack1.com",
    "description": "A beginner-friendly hackathon",
    "location": "Athens",
    "organizer": "Tech Club",
    "tags": "AI,Python",
    "status": "published",
    "mode": "hybrid",
}


def assert_hackathon_created(client, payload,test_contains_time=False):
    if test_contains_time:
        before_post = datetime.now().replace(microsecond=0)
        time.sleep(TIME_SLEEP_DURATION)  # Sleep for 1 second to ensure a time difference
        response = client.post("/api/hackathons", data=payload)
        time.sleep(TIME_SLEEP_DURATION) 
        after_post = datetime.now().replace(microsecond=0)
    else:
        response = client.post("/api/hackathons", data=payload)

    assert response.status_code == 200
    assert response.json["success"] == f"Successfully added hackathon:{payload.get('name')}!"

    get_response = client.get("/api/hackathons/1")

    assert get_response.status_code == 200
    assert get_response.json["name"] == payload.get("name")
    assert get_response.json["url"] == payload.get("url")
    
    if test_contains_time:
        submittedAt_value = datetime.fromisoformat(get_response.json["submittedAt"])
        updatedAt_value = datetime.fromisoformat(get_response.json["updatedAt"])
        assert before_post <= submittedAt_value <= after_post
        assert before_post <= updatedAt_value <= after_post

    if "interestCount" in payload:
        assert get_response.json["interestCount"] == 0

    for field in ["description", "location", "organizer", "tags", "status", "mode", "hasPrize", "prizeDetails", "startDate", "endDate"]:
        expected_value = payload.get(field)

        if field in ["startDate", "endDate"] and expected_value is not None:
            expected_value = expected_value.replace(" ", "T")

        if (field == "hasPrize") and (type(expected_value) == str):
            assert type(get_response.json[field]) == bool #we are making sure that the hasPrize value is converted to boolean type when it is a string
            assert str(get_response.json[field]).lower() == expected_value #payload.get(field) is only going to be "false" or "true" in our test cases
        else:
            assert get_response.json[field] == expected_value


def assert_hackathon_not_created(client, payload, error_message):
    response = client.post("/api/hackathons", data=payload)

    assert response.status_code == 400
    assert response.json["error"] == error_message

    get_response = client.get("/api/hackathons/1")

    assert get_response.status_code == 404
    assert get_response.json["error"] == "Wrong id"


def test_add_hackathon_without_name_and_without_url(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {
        "name": None,
        "url": None,
    }

    assert_hackathon_not_created(client, payload, "name and url are required")


def test_add_hackathon_without_name_and_with_url(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {
        "name": None,
        "url": "hack1.com",
    }

    assert_hackathon_not_created(client, payload, "name and url are required")


def test_add_hackathon_with_name_and_without_url(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {
        "name": "Hackathon1",
        "url": None,
    }

    assert_hackathon_not_created(client, payload, "name and url are required")


def test_add_hackathon_with_name_and_url(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {
        "name": "Hackathon1",
        "url": "hack1.com",
    }

    assert_hackathon_created(client, payload)


def test_add_hackathon_with_description(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {**base_payload, "description": "A beginner-friendly hackathon"}

    assert_hackathon_created(client, payload)


def test_add_hackathon_with_location(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {**base_payload, "location": "Athens"}

    assert_hackathon_created(client, payload)


def test_add_hackathon_with_organizer(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {**base_payload, "organizer": "Tech Club"}

    assert_hackathon_created(client, payload)


def test_add_hackathon_with_tags(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {**base_payload, "tags": "AI,Python"}

    assert_hackathon_created(client, payload)


def test_add_hackathon_with_description_and_location(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {**base_payload, "description": "A beginner-friendly hackathon", "location": "Athens"}

    assert_hackathon_created(client, payload)


def test_add_hackathon_with_description_and_organizer(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {**base_payload, "description": "A beginner-friendly hackathon", "organizer": "Tech Club"}

    assert_hackathon_created(client, payload)


def test_add_hackathon_with_location_and_tags(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {**base_payload, "location": "Athens", "tags": "AI,Python"}

    assert_hackathon_created(client, payload)


def test_add_hackathon_with_description_location_organizer_and_tags(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {
        **base_payload,
        "description": "A beginner-friendly hackathon",
        "location": "Athens",
        "organizer": "Tech Club",
        "tags": "AI,Python",
    }

    assert_hackathon_created(client, payload)


def test_add_hackathon_startDate_and_endDate_correct(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {
        **base_payload,
        "startDate": "2025-08-15 00:01:00",
        "endDate": "2025-08-17 01:00:00",
    }

    assert_hackathon_created(client, payload)


def test_add_hackathon_startDate_wrong_and_endDate_correct(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {
        **base_payload,
        "startDate": "2025/08/15 00:01:00",
        "endDate": "2025-08-17 01:00:00",
    }

    assert_hackathon_not_created(client, payload, "Wrong date format")


def test_add_hackathon_startDate_correct_and_endDate_wrong(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {
        **base_payload,
        "startDate": "2025-08-15 00:01:00",
        "endDate": "2025/08/17 01:00:00",
    }

    assert_hackathon_not_created(client, payload, "Wrong date format")


def test_add_hackathon_startDate_and_endDate_wrong(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {
        **base_payload,
        "startDate": "abc",
        "endDate": "2025/08/17 01:00:00",
    }

    assert_hackathon_not_created(client, payload, "Wrong date format")


def test_add_hackathon_startDate_none_and_endDate_correct(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {
        **base_payload,
        "startDate": None,
        "endDate": "2025-08-17 01:00:00",
    }

    assert_hackathon_created(client, payload)


def test_add_hackathon_startDate_correct_and_endDate_none(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {
        **base_payload,
        "startDate": "2025-08-15 00:01:00",
        "endDate": None,
    }

    assert_hackathon_created(client, payload)


def test_add_hackathon_endDate_before_startDate(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {
        **base_payload,
        "startDate": "2025-08-17 01:00:00",
        "endDate": "2025-08-15 00:01:00",
    }

    assert_hackathon_not_created(client, payload, "startDate cannot be greater than endDate")


def test_add_hackathon_interestCount_ignored_when_provided_positive(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {**base_payload, "interestCount": 10}

    assert_hackathon_created(client, payload)


def test_add_hackathon_interestCount_ignored_when_provided_negative_int(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {**base_payload, "interestCount": -20}

    assert_hackathon_created(client, payload)


def test_add_hackathon_interestCount_ignored_when_provided_large_int(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {**base_payload, "interestCount": 100000000}

    assert_hackathon_created(client, payload)


def test_add_hackathon_interestCount_ignored_when_provided_string_numeric(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {**base_payload, "interestCount": "123"}

    assert_hackathon_created(client, payload)


def test_add_hackathon_interestCount_ignored_when_provided_string_numeric_negative(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {**base_payload, "interestCount": "-20"}

    assert_hackathon_created(client, payload)


def test_add_hackathon_interestCount_ignored_when_provided_string_numeric_large(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {**base_payload, "interestCount": "100000000"}

    assert_hackathon_created(client, payload)


def test_add_hackathon_interestCount_ignored_when_provided_string_non_numeric(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {**base_payload, "interestCount": "abc"}

    assert_hackathon_created(client, payload)


def test_add_hackathon_interestCount_omitted(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {**base_payload,"interestCount": None}

    assert_hackathon_created(client, payload)


def test_add_hackathon_with_wrong_status(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {**base_payload, "status": "wrong status"}

    assert_hackathon_not_created(client, payload, "Wrong status")


def test_add_hackathon_with_status_draft(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {**base_payload, "status": "draft"}

    assert_hackathon_created(client, payload)


def test_add_hackathon_with_status_pending(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {**base_payload, "status": "pending"}

    assert_hackathon_created(client, payload)


def test_add_hackathon_with_status_published(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {**base_payload, "status": "published"}

    assert_hackathon_created(client, payload)


def test_add_hackathon_with_status_needs_changes(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {**base_payload, "status": "needs-changes"}

    assert_hackathon_created(client, payload)


def test_add_hackathon_hasPrize_true_and_prizeDetails_value(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {**base_payload, "hasPrize": True, "prizeDetails": "$500 cash"}

    assert_hackathon_created(client, payload)


def test_add_hackathon_hasPrize_true_and_prizeDetails_none(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {**base_payload, "hasPrize": True, "prizeDetails": None}

    assert_hackathon_created(client, payload)


def test_add_hackathon_hasPrize_false_and_prizeDetails_none(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {**base_payload, "hasPrize": False, "prizeDetails": None}

    assert_hackathon_created(client, payload)


def test_add_hackathon_hasPrize_false_and_prizeDetails_value(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {**base_payload, "hasPrize": False, "prizeDetails": "$500 cash"}

    assert_hackathon_not_created(client, payload, "prizeDetails cannot contain any value when hasPrize is False")


def test_add_hackathon_hasPrize_none_and_prizeDetails_value(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {**base_payload, "hasPrize": None, "prizeDetails": "$500 cash"}

    assert_hackathon_not_created(client, payload, "prizeDetails cannot contain any value when hasPrize is None")


def test_add_hackathon_hasPrize_none_and_prizeDetails_none(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {**base_payload, "hasPrize": None, "prizeDetails": None}

    assert_hackathon_created(client, payload)


def test_add_hackathon_hasPrize_wrong_string(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {**base_payload, "hasPrize": "maybe"}

    assert_hackathon_not_created(client, payload, "Wrong hasPrize")


def test_add_hackathon_hasPrize_string_false(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {**base_payload, "hasPrize": "false"}
    assert_hackathon_created(client, payload)

def test_add_hackathon_hasPrize_string_true(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {**base_payload, "hasPrize": "true"}
    assert_hackathon_created(client, payload)


def test_add_hackathon_with_wrong_mode(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {**base_payload, "mode": "wrong mode"}

    assert_hackathon_not_created(client, payload, "Wrong mode")


def test_add_hackathon_with_mode_in_person(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {**base_payload, "mode": "in_person"}

    assert_hackathon_created(client, payload)


def test_add_hackathon_with_mode_online(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {**base_payload, "mode": "online"}

    assert_hackathon_created(client, payload)


def test_add_hackathon_with_mode_hybrid(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {**base_payload, "mode": "hybrid"}

    assert_hackathon_created(client, payload)


def test_add_hackathon_with_submittedAt_value(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {**base_payload, "submittedAt": "2023-10-10 10:00:00"}

    assert_hackathon_created(client, payload,test_contains_time=True)

def test_add_hackathon_with_submittedAt_none(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {**base_payload, "submittedAt": None}

    assert_hackathon_created(client, payload,test_contains_time=True)
    
def test_add_hackathon_with_updatedAt_value(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {**base_payload, "updatedAt": "2023-10-10 10:00:00"}

    assert_hackathon_created(client, payload,test_contains_time=True)

def test_add_hackathon_with_updatedAt_none(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {**base_payload, "updatedAt": None}

    assert_hackathon_created(client, payload,test_contains_time=True)
    
def test_add_hackathon_with_submittedAt_and_updatedAt_value(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {**base_payload, "submittedAt": "2023-10-10 10:00:00", "updatedAt": "2023-10-10 12:00:00"}

    assert_hackathon_created(client, payload,test_contains_time=True)

def test_add_hackathon_with_submittedAt_and_updatedAt_none(app, client):
    with app.app_context():
        from main import db
        db.create_all()

    payload = {**base_payload, "submittedAt": None, "updatedAt": None}

    assert_hackathon_created(client, payload,test_contains_time=True)