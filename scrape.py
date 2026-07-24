from selenium.webdriver import Remote
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection

from bs4 import BeautifulSoup
import time

# Replace with your own Browser API credentials
AUTH = "brd-customer-hl_0b4b5cd4-zone-ai_scraper:h6osk1qznwm5"

def scrape_website(website):
    print("Connecting to Bright Data Browser API...")

    options = Options()

    # Uncomment if needed
    # options.add_argument("--headless=new")

    server_addr = f"https://{AUTH}@brd.superproxy.io:9515"
    connection = ChromiumRemoteConnection(server_addr, "goog", "chrome")
    driver = Remote(connection, options=options)

    try:
        print(f"Opening: {website}")
        driver.get(website)

        print("Waiting for CAPTCHA detection...")

        result = driver.execute(
            "executeCdpCommand",
            {
                "cmd": "Captcha.waitForSolve",
                "params": {
                    "detectTimeout": 10000   # Wait up to 10 seconds
                },
            },
        )

        status = result["value"]["status"]
        print("CAPTCHA status:", status)

        # Optional wait for JavaScript to finish loading
        time.sleep(5)

        print("Page loaded.")

        html = driver.page_source
        return html

    finally:
        driver.quit()

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())

    return cleaned_content

#LLM takes 8000 characters at max in token limit so split them into batches and take one batch at a time
def split_dom_content(dom_content, max_length = 6000):
    return[
        dom_content[i : i +max_length] for i in range(0, len(dom_content), max_length)
    ]


if __name__ == "__main__":
    html = scrape_website("https://example.com")
    print(html[:1000])  