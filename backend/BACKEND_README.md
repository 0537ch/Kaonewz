# Country Analytics API Backend

## 📁 Project Structure
```
backend/
├── .env                    # Environment variables (NEWS_API_KEY, etc.)
├── main.py                 # FastAPI application and routes
├── requirements.txt        # Python dependencies
└── services/               # Business logic
    ├── __init__.py
    └── news_service.py     # News API integration (NewsService)
```

## 🏗️ Architecture
```
Frontend (React) → FastAPI Backend → External APIs
                                   ├─ REST Countries API (country stats)
                                   └─ NewsAPI (news headlines & search)
```

## 🚀 Features

### Country Data (from REST Countries API)
- List all countries with key metrics (name, region, population, area_km2, density)
- Filter countries by region
- Top N countries by population
- Top N most densely populated countries
- Region-level average statistics (population, density, area)

### News Integration (via NewsAPI)
- Country-specific top headlines
- Full-text news search
- Pagination and category filter
- Language and sort options for search

## 🌐 API Endpoints (from `main.py`)

### Root
- `GET /`
  - Returns API info and links to key endpoints.

### Countries
- `GET /countries`
  - Returns all countries with computed density.

- `GET /countries/region/{region}`
  - Filter countries by region (case-insensitive).
  - 404 if no countries found for the region.

- `GET /countries/top/{n}`
  - Top `n` countries by population.
  - Path constraint: `n` > 0 and `n` ≤ 50.

- `GET /countries/density/top/{n}`
  - Top `n` countries by population density.
  - Path constraint: `n` > 0 and `n` ≤ 50.

### Statistics
- `GET /stats/region`
  - Region-level averages for `population`, `density`, `area_km2`.
  - Values rounded to 2 decimals.

### News
- `GET /news/country/{country_code}`
  - Query params:
    - `page_size` (int, 1–100, default 10)
    - `page` (int, ≥1, default 1)
    - `category` (str, optional: business, entertainment, general, health, science, sports, technology)
  - Validates `country_code` (2-letter).
  - Returns normalized NewsAPI `articles` list.

- `GET /news/search`
  - Query params:
    - `query` (str, required, min length 2)
    - `country_code` (str, optional, 2-letter)
    - `language` (str, default `en`)
    - `sort_by` (str, default `publishedAt`; options: publishedAt, popularity, relevancy)
    - `page_size` (int, 1–100, default 10)
    - `page` (int, ≥1, default 1)
  - Returns matching `articles` from NewsAPI `everything` endpoint.

## 🔧 Implementation Details

### Country Data Pipeline (`main.py`)
- Fetch: `https://restcountries.com/v3.1/all?fields=name,region,population,area`
- Transform with Pandas:
  - Normalize JSON → DataFrame
  - Select and rename columns → `country`, `region`, `population`, `area_km2`
  - Compute `density = population / area_km2`
- Serve as JSON via FastAPI routes.

### News Service (`services/news_service.py`)
- `NewsService` reads env vars on init:
  - `NEWS_API_KEY` (required)
  - `NEWS_API_BASE_URL` (default `https://newsapi.org/v2`)
  - `DEFAULT_PAGE_SIZE` (default `10`, max enforced at `100`)
- Methods:
  - `get_news_for_country(country_code, page_size, page, category)`
    - Calls `GET {base_url}/top-headlines` with `country`, `category`, pagination
    - Raises on invalid country code or request failure
  - `search_news(query, country_code, language, sort_by, page_size, page)`
    - Calls `GET {base_url}/everything` with full-text search params
- Errors:
  - Uses `requests` with `timeout=10`, logs exceptions, raises user-friendly errors.
- Singleton instance exported as `news_service` and injected into routes.

## 🧰 Tech Stack
- FastAPI (web framework, auto OpenAPI/Swagger at `/docs`, ReDoc at `/redoc`)
- Uvicorn (ASGI server)
- Requests (HTTP client)
- Pandas (data processing)
- python-dotenv (env management)

Dependencies (from `requirements.txt`):
```
fastapi>=0.68.0
uvicorn>=0.15.0
requests>=2.26.0
pandas>=1.3.0
python-dotenv>=0.19.0
python-multipart>=0.0.5
```

## ⚙️ Configuration
Create a `.env` in `backend/` with:
```ini
# Required
NEWS_API_KEY=your_news_api_key_here

# Optional
NEWS_API_BASE_URL=https://newsapi.org/v2
DEFAULT_PAGE_SIZE=10
```

## 🚀 Run Locally
```bash
# from the backend directory
pip install -r requirements.txt
uvicorn main:app --reload
```
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🛡️ CORS
- Currently `allow_origins=["*"]` for development convenience.
- In production, restrict to your frontend origin.

## 📈 Response Shapes
- Successful list endpoints return:
```json
{
  "status": "success",
  "results": <int>,
  "data": [ { ... } ]
}
```
- News endpoints additionally include request echoing fields (`country`, `category`, `page`, `page_size`).

## ❗ Error Handling
- Uses FastAPI `HTTPException` with appropriate status codes:
  - 400: invalid parameters (e.g., bad country code)
  - 404: not found (e.g., empty region filter)
  - 500: upstream/API failures or processing errors

## 🚦 Notes & Limits
- No database layer (stateless). Data fetched on-demand.
- Per-request transform with Pandas; adequate for small-medium payloads.
- NewsAPI rate limits apply; consider caching in production.

## 🔮 Suggested Improvements
- Add caching (e.g., Redis) for country and news responses
- Add rate limiting (e.g., slowapi)
- Convert external calls to async (`httpx`) and use async routes
- Add a persistence layer (SQLite/Postgres) for caching and historical analysis
- Add health checks and metrics (Prometheus)
- Unit/integration tests for services and routes
