
import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/High_Life_(2018_film)"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def scrape_page():
    """
    Fetch the page at the hardcoded URL, extract <p> tags, save to Selected_Document.txt,
    print a success or failure message, and return the extracted text.
    """
    response = requests.get(URL, headers=HEADERS, timeout=10)

    if response.status_code != 200:
        print(f"Failed to fetch page. Status code: {response.status_code}")
        return ""

    soup = BeautifulSoup(response.text, "html.parser")

    paragraphs = soup.find_all("p")
    extracted_text = "\n\n".join(p.get_text(" ", strip=True) for p in paragraphs)

    with open("Selected_Document.txt", "w", encoding="utf-8") as f:
        f.write(extracted_text)

    print("Successfully scraped and saved Selected_Document.txt")
    return extracted_text

def main():
    scrape_page()

if __name__ == "__main__":
    main()
