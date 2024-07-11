import requests
from bs4 import BeautifulSoup
from html2image import Html2Image

# Step 1: Scrape the HTML title from Reddit post
def get_reddit_title(reddit_url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(reddit_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Reddit title usually in h1 tag with class '_eYtD2XCVieq6emjKBH3m'
        title = soup.find('h1', class_='_eYtD2XCVieq6emjKBH3m')
        return title.text if title else "Title not found"
    else:
        return "Error fetching the page"

# Step 2: Convert the title to an image
def title_to_image(title, output_path):
    hti = Html2Image()
    html_content = f"<html><body><h1>{title}</h1></body></html>"
    hti.screenshot(html_str=html_content, save_as=output_path)

# Usage
reddit_url = "https://www.reddit.com/r/example_post"
title = get_reddit_title(reddit_url)
output_image_path = "reddit_title.png"
title_to_image(title, output_image_path)

print(f"Title saved as image: {output_image_path}")
