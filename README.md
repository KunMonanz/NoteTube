# NoteTube 🚀

NoteTube is a clean, dependency-light FastAPI backend that takes a YouTube video URL, extracts its transcript natively, and passes it through an optimized Google Gemini workflow to generate high-density, beautifully structured markdown notes.

By eliminating complex task queues and message brokers, this project achieves a minimal footprint using native Python async loops, in-memory IP token buckets, and zero-storage file streaming.

## ✨ Key Features

- **Smart URL Normalization**: Pydantic v2 validator handles mobile links, shorts, embeds, and tracking parameters seamlessly.
- **Pure Async Architecture**: Offloads blocking network scraping tasks into dedicated background threads to keep the FastAPI event loop running smoothly.
- **Token-Optimized Prompts**: System constraints designed specifically to maximize context density while minimizing API token consumption costs.
- **In-Memory Multi-IP Rate Limiting**: Custom sliding token bucket dict that restricts clients to exactly 10 requests per day mapped across distinct IP footprints.
- **Direct Markdown Exports**: Streams results natively as downloadable `.md` file attachments without taking up local server storage space.

## 🛠️ Tech Stack

- **Framework**: FastAPI (Asynchronous Routing)
- **Data Validation**: Pydantic v2 (Computed Fields & Validators)
- **AI Integration**: Google Gen AI Python SDK (`gemini-2.5-flash`)
- **Scraper**: `youtube-transcript-api`

## 📁 Project Structure

```text
├── main.py                 # FastAPI app entrypoint (current)
├── gemini.py               # Gemini API script (current; to be wrapped as a reusable client)
├── requirements.txt        # Package dependencies
│
│   # Planned, not yet implemented:
├── api/
│   └── v1/
│       └── router.py       # Async API path definitions
├── utils.py                # Thread pool executor for script fetching
├── schema.py               # Pydantic input/output payload models
├── ratelimiting.py         # In-memory IP tracking token bucket
├── system_prompt.txt       # Low-cost system rules
└── prompt_template.txt     # Note layout markdown blueprint
```

## 🚀 Local Installation & Setup

### 1. Clone and Configure Environments

```bash
git clone https://github.com/KunMonanz/NoteTube.git
cd NoteTube

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 2. Environment Variables (`.env`)

Create a `.env` file in the project root:

```env
GEMINI_API_KEY="your_google_gemini_api_key"
```

### 3. Run the Server

Launch your FastAPI development server locally:

```bash
uvicorn main:app --reload
```

## 🌐 Deployment Note

Because this architecture relies entirely on local server memory (`RAM`) to manage individual daily rate limits, it is best deployed on a single permanent computing instance (such as an **Oracle Cloud Always Free VM** or a single container platform) rather than serverless architectures that clear memory states frequently.

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
