# 🔗 urlshort

A simple URL shortener backend built with Python. Give it a long URL, get back a short code, and use that code to redirect to the original link.

## Features

- Shorten any long URL into a compact code
- Redirect from the short code to the original URL
- Persistent storage in a local database (`shortner.db`)

## Tech Stack

- **Language:** Python 3.10+
- **Framework:** FastAPI *(TODO: confirm)*
- **Database:** SQLite *(TODO: confirm)*

## Project Structure

```
urlshort/
├── app/            # Application code (API, database, services)
├── __init__.py
└── shortner.db     # Local database file
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/KrBeTect2025/urlshort.git
cd urlshort
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install fastapi uvicorn
```

*(TODO: replace with `pip install -r requirements.txt` once you add one)*

### 4. Run the server

```bash
uvicorn app.main:app --reload
```

*(TODO: adjust the module path if your entry file is named differently)*

The API will be available at `http://127.0.0.1:8000`. If you're using FastAPI, interactive docs are at `http://127.0.0.1:8000/docs`.

## API Endpoints

| Method | Endpoint        | Description                          |
|--------|-----------------|--------------------------------------|
| POST   | `/shorten`      | Create a short code for a long URL   |
| GET    | `/{short_code}` | Redirect to the original URL         |

*(TODO: update the paths to match your actual routes)*

### Example

```bash
curl -X POST http://127.0.0.1:8000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/some/very/long/link"}'
```

## Roadmap

- [ ] Click/visit tracking per short link
- [ ] Custom aliases
- [ ] Link expiry
- [ ] Rate limiting
- [ ] Tests
- [ ] Docker support

## Contributing

Contributions, issues, and feature requests are welcome. Fork the repo, create a branch, and open a pull request.

## License

TODO: choose a license (MIT is a common default for personal projects).
