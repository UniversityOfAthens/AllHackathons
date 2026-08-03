# Backend API

This backend powers the hackathon discovery platform by exposing a Flask-based API for creating, reading, filtering, and updating hackathon records.

## What this backend does

The service currently supports:

- Creating new hackathons through a POST endpoint
- Listing and filtering hackathons with query parameters
- Fetching a single hackathon by ID
- Updating an existing hackathon with PATCH
- Validating fields such as status, mode, prize information, dates, and interest count
- Persisting data in a SQLite database with SQLAlchemy
- Supporting Alembic-based migrations and database utilities
- Seeding sample data for local development

## Project structure

- `main.py` — Flask app, route definitions, request parsing, and validation logic
- `database.py` — SQLAlchemy model definitions and enum values for hackathons
- `utils.py` — helper functions for manual database operations and CLI-based maintenance
- `seed.py` — sample data seeding script for local testing
- `tests/` — pytest cases covering create, read, filter, and update behavior
- `migrations/` — Alembic migration files
- `db/` — SQLite database files and local app storage

## Setup

From the repository root:

```bash
cd backend
source env/bin/activate
pip install -r requirements.txt
```

Run the app locally:

```bash
flask --app main run --reload
```

The server will run at:

```text
http://localhost:5000
```

## API endpoints

### Get all hackathons

- Method: `GET`
- Path: `/api/hackathons`

Optional query parameters:

- `status` — filter by `draft`, `pending`, `published`, or `needs-changes`
- `upcoming=true|false` — filter by whether the event starts in the future
- `past=true|false` — filter by whether the event has already started
- `tags` — exact tag match
- `q` — text search across name, URL, description, location, organizer, prize details, and tags
- `sort` — sort by `name`, `startDate`, `endDate`, `submittedAt`, `updatedAt`, or `interestCount`

Example:

```bash
curl "http://localhost:5000/api/hackathons?status=published&upcoming=true&sort=interestCount"
```

### Get one hackathon

- Method: `GET`
- Path: `/api/hackathons/<id>`

Example:

```bash
curl http://localhost:5000/api/hackathons/1
```

### Create a hackathon

- Method: `POST`
- Path: `/api/hackathons`

Expected form fields:

- `name` — required
- `url` — required
- `description`
- `startDate` — format: `YYYY-MM-DD HH:MM:SS`
- `endDate` — format: `YYYY-MM-DD HH:MM:SS`
- `location`
- `mode` — `in_person`, `online`, or `hybrid`
- `organizer`
- `hasPrize` — `true` or `false`
- `prizeDetails`
- `tags`
- `status` — `draft`, `pending`, `published`, or `needs-changes`
- `interestCount`

Example:

```bash
curl -X POST http://localhost:5000/api/hackathons \
  -d "name=AI Builders Hackathon" \
  -d "url=https://example.com/hackathon" \
  -d "description=Build an AI app in 48 hours" \
  -d "mode=hybrid" \
  -d "status=published" \
  -d "hasPrize=true" \
  -d "prizeDetails=1000 USD"
```

### Update a hackathon

- Method: `PATCH`
- Path: `/api/<id>`

You can send one or more fields to update. The API will preserve existing values for any field you do not provide.

Example:

```bash
curl -X PATCH http://localhost:5000/api/1 \
  -d "name=Updated Hackathon Name" \
  -d "status=pending"
```

## Validation rules

The backend applies a number of validation checks:

- `name` and `url` are required when creating a new hackathon
- `status` must be one of the allowed enum values
- `mode` must be one of `in_person`, `online`, or `hybrid`
- `hasPrize` must be `true` or `false`
- `prizeDetails` is only allowed when `hasPrize` is `true`
- `interestCount` must be an integer between `0` and `10000`
- Dates must follow the `YYYY-MM-DD HH:MM:SS` format

## Data model

Each hackathon record contains:

- `id`
- `name`
- `description`
- `url`
- `startDate`
- `endDate`
- `location`
- `mode`
- `organizer`
- `hasPrize`
- `prizeDetails`
- `tags`
- `status`
- `submittedAt`
- `updatedAt`
- `interestCount`

## Database and migrations

The backend uses SQLite by default and initializes the database on startup.

Useful commands:

```bash
# Migration helpers
python utils.py --migrate
python utils.py --upgrade
python utils.py --current_migrations

# Manual database row operations
python utils.py --add_row --name "Example Hackathon" --url "https://example.com" --status published --mode hybrid --hasPrize true --prizeDetails "1000 USD"
python utils.py --update_row --id 1 --name "Updated Hackathon" --status pending
python utils.py --delete_row --id 1
python utils.py --delete_rows --ids 1 2 3
python utils.py --delete_all_rows
python utils.py --cleanup_db
```

Notes:

- `--add_row` and `--update_row` accept the same core fields as the API, including `name`, `url`, `description`, `startDate`, `endDate`, `location`, `mode`, `organizer`, `hasPrize`, `prizeDetails`, `tags`, `status`, `submittedAt`, `updatedAt`, and `interestCount`.
- `--delete_all_rows` will prompt for confirmation before removing the entire table.
- `--cleanup_db` drops the database schema and removes the session state for testing or reset workflows.

## Seed sample data

The seed script sends example requests to the local API:

```bash
python seed.py
```

## Testing

The project includes pytest coverage for the API behavior:

```bash
pytest -q
```

## Dependency maintenance

To refresh the dependency list:

```bash
pipreqs . --force --mode no-pin
```
