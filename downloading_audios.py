import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_audio_files(url):
    # Create a session object
    session = requests.Session()
    # Get the webpage content
    response = session.get(url)
    # Raise an error for bad statuses
    response.raise_for_status()

    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find all 'a' tags, which are hyperlinks
    audio_links = [urljoin(url, link.get('href')) for link in soup.find_all('a') if link.get('href').endswith(('.mp3', '.wav'))]

    # Create a directory to save the downloaded files
    os.makedirs('downloaded_audio', exist_ok=True)

    # Download each audio file
    for link in audio_links:
        # Get the file name by splitting the URL on the slash and taking the last segment
        filename = os.path.join('downloaded_audio', link.split('/')[-1])
        # Stream the audio file
        response = session.get(link, stream=True)
        # Save the file
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f'Downloaded {filename}')

# Specify the URL
url = 'https://media.talkbank.org/phon/Eng-NA/PaidoEnglish/0wav/'
download_audio_files(url)
