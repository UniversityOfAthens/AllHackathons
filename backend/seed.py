import requests


data1 = {
    "name": "Bobathon",
    "description": "A hackathon focused on building AI-powered solutions for real-world problems.",
    "url": "https://example.com/events/ioannis-hackathon",
    "startDate": "2025-08-15 00:01:00",
    "endDate": "2025-08-17 01:00:00",
    "location": "Athens, Greece",
    "mode": "hybrid",
    "organizer": "Tech Community Athens",
    "hasPrize": True,
    "prizeDetails": "$2000 cash prize + mentorship opportunities",
    "tags": "AI,ML,Python",
    "status": "published",
    "interestCount": 42
}

data2 = {
    "name": "CodeSprint Berlin",
    "description": "A 48-hour coding sprint for web developers of all skill levels.",
    "url": "https://example.com/events/codesprint-berlin",
    "startDate": "2024-09-05 02:00:00",
    "endDate": "2024-09-07 03:00:00",
    "location": "Berlin, Germany",
    "mode": "in_person",
    "organizer": "DevGuild Berlin",
    "hasPrize": True,
    "prizeDetails": "1st place: 1500 EUR, 2nd place: 750 EUR",
    "tags": "Web,JavaScript,React",
    "status": "pending",
    "interestCount": 18
}

data3 = {
    "name": "Remote Data Science Challenge",
    "description": None,
    "url": "https://example.com/events/remote-ds-challenge",
    "startDate": "2026-10-01 00:00:00",
    "endDate": "2026-10-14 01:00:00",
    "location": "Remote",
    "mode": "online",
    "organizer": None,
    "hasPrize": False,
    "prizeDetails": None,
    "tags": "DataScience,Python,ML",
    "status": "draft",
    "interestCount": 5
}

data4 = {
    "name": "CyberSec CTF Nights",
    "description": "Capture-the-flag competition testing skills in network security and cryptography.",
    "url": "https://example.com/events/cybersec-ctf-nights",
    "startDate": "2026-07-25 00:00:00",
    "endDate": "2026-07-26 01:00:00",
    "location": "Toronto, Canada",
    "mode": "hybrid",
    "organizer": "SecureNet Collective",
    "hasPrize": True,
    "prizeDetails": "Top 3 teams receive hardware security keys + swag",
    "tags": "Security,CTF,Networking",
    "status": None,
    "interestCount": 0
}

data5 = {
    "name": "Startup Pitch Fest 2026",
    "description": "An event for early-stage founders to pitch ideas to investors and mentors.",
    "url": "https://example.com/events/startup-pitch-fest-2026",
    "startDate": "2026-11-12 01:00:00",
    "endDate": "2026-11-12 02:00:00",
    "location": "New York, NY",
    "mode": "in_person",
    "organizer": "Founders Network NYC",
    "hasPrize": False,
    "prizeDetails": None,
    "tags": "Startup,Pitch,Networking",
    "status": "published",
    "interestCount": 150
}

example_requests = [data1,data2,data3,data4,data5]

def populate_db(request_data:list):
    for index,req in enumerate(request_data):
        requests.post("http://127.0.0.1:5000/api/hackathons", data=example_requests[index])
    print("Seed completed successfully!")
        
populate_db(example_requests)