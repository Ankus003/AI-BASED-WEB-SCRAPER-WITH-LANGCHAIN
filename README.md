# AI Web Scraper

A Python-based web scraper with an interactive Streamlit UI that combines browser automation with a local LLM to extract exactly the information you ask for from any webpage — no manual CSS selectors or XPath needed.


## How It Works

1. **Enter a URL** — the app uses Selenium (via Bright Data's Browser API) to load the page, including JavaScript-rendered content, with built-in CAPTCHA-solving support.
2. **HTML is parsed** with BeautifulSoup, stripped of scripts/styles, and cleaned into readable text.
3. **Describe what you want extracted**, in plain English (e.g. "get all product names and prices").
4. The cleaned content is chunked and passed to a **local LLM (Llama 3.2 via Ollama)** through LangChain, which extracts only the matching data — nothing else.


## Features

- 🌐 Scrapes JavaScript-heavy, dynamic websites via a remote browser automation API
- 🤖 Built-in CAPTCHA detection/handling
- 🧹 Automatic HTML cleaning (removes scripts, styles, and noise)
- ✂️ Smart content chunking to respect LLM token limits
- 🗣️ Natural-language extraction — describe what you want instead of writing selectors
- 🖥️ Simple, interactive web UI (no command-line usage needed)
- 🔒 Runs the LLM locally via Ollama — no data sent to external AI APIs


## Tech Stack

| Category | Tools |
|---|---|
| UI | Streamlit |
| Browser Automation | Selenium, Bright Data Browser API |
| HTML Parsing | BeautifulSoup4, lxml, html5lib |
| AI / LLM | LangChain, Ollama (Llama 3.2 3B) |
| Config | python-dotenv |
| Language | Python |


## Project Structure

```
.
├── main.py             # Streamlit app entry point (UI)
├── scrape.py            # Website scraping & HTML cleaning logic
├── parse.py             # LLM-based content extraction logic
├── requirements.txt     # Python dependencies
└── .env                  # Environment variables (not committed)
```


## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) installed locally, with the `llama3.2:3b` model pulled:
  ```bash
  ollama pull llama3.2:3b
  ```
- A [Bright Data](https://brightdata.com/) account with a Browser API zone (for the Selenium remote browser connection)


## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/<your-repo>.git
   cd <your-repo>
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Create a `.env` file in the project root:
   ```env
   BRIGHT_DATA_AUTH=brd-customer-<your-customer-id>-zone-<your-zone>:<your-password>
   ```

   Then update `scrape.py` to load this instead of using a hardcoded string:
   ```python
   import os
   from dotenv import load_dotenv

   load_dotenv()
   AUTH = os.getenv("BRIGHT_DATA_AUTH")
   ```

   > ⚠️ **Never commit real credentials.** Make sure `.env` is listed in `.gitignore`.

5. **Run the app**
   ```bash
   streamlit run main.py
   ```

   This opens the app in your browser (usually at `http://localhost:8501`).

## Usage

1. Enter the URL of the website you want to scrape.
2. Click **Scrape Site** — the cleaned page content will appear under "View DOM Content."
3. In the text box, describe what data you want extracted (e.g. "list all article titles and dates").
4. Click **Parse Content** to get the extracted results.

## Notes

- The scraper connects to a remote browser through Bright Data, so an active Bright Data account/zone is required.
- The LLM runs locally through Ollama, so no scraped content is sent to an external AI API.
- Large pages are automatically split into chunks (~6000 characters) to stay within the LLM's context limits.

