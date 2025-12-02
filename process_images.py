import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json

# Configuration
BASE_DIR = '/home/daniel/imgur/sites/where-is-waldo.online'
IMAGES_DIR = os.path.join(BASE_DIR, 'images')
os.makedirs(IMAGES_DIR, exist_ok=True)

# URL to Filename mapping
url_to_file = {
    "https://www.where-is-waldo.online/": "index.html",
    "https://www.where-is-waldo.online/characters.html": "characters.html",
    "https://www.where-is-waldo.online/costume.html": "costume.html",
    "https://www.where-is-waldo.online/game.html": "game.html",
    "https://www.where-is-waldo.online/gif.html": "gif.html",
    "https://www.where-is-waldo.online/image.html": "image.html",
    "https://www.where-is-waldo.online/lady.html": "lady.html",
    "https://www.where-is-waldo.online/meme.html": "meme.html",
    "https://www.where-is-waldo.online/page.html": "page.html",
    "https://www.where-is-waldo.online/picture.html": "picture.html",
    "https://www.where-is-waldo.online/puzzle.html": "puzzle.html",
    "https://www.where-is-waldo.online/shirt.html": "shirt.html"
}

# Keywords mapping
url_keywords = [
  {
    "URL": "https://www.where-is-waldo.online/",
    "keywords": [
      "where's waldo"
    ]
  },
  {
    "URL": "https://www.where-is-waldo.online/characters.html",
    "keywords": [
      "where's waldo characters"
    ]
  },
  {
    "URL": "https://www.where-is-waldo.online/costume.html",
    "keywords": [
      "where's waldo costume"
    ]
  },
  {
    "URL": "https://www.where-is-waldo.online/game.html",
    "keywords": [
      "where's waldo game"
    ]
  },
  {
    "URL": "https://www.where-is-waldo.online/gif.html",
    "keywords": [
      "where's waldo gif"
    ]
  },
  {
    "URL": "https://www.where-is-waldo.online/image.html",
    "keywords": [
      "where's waldo image",
      "finding waldo images"
    ]
  },
  {
    "URL": "https://www.where-is-waldo.online/lady.html",
    "keywords": [
      "where's waldo lady"
    ]
  },
  {
    "URL": "https://www.where-is-waldo.online/meme.html",
    "keywords": [
      "where's waldo meme"
    ]
  },
  {
    "URL": "https://www.where-is-waldo.online/page.html",
    "keywords": [
      "where's waldo page"
    ]
  },
  {
    "URL": "https://www.where-is-waldo.online/picture.html",
    "keywords": [
      "where's waldo picture",
      "Where's Waldo high resolution",
      "where's waldo at the beach",
      "find waldo pictures",
      "find waldo pics"
    ]
  },
  {
    "URL": "https://www.where-is-waldo.online/puzzle.html",
    "keywords": [
      "where's waldo puzzle"
    ]
  },
  {
    "URL": "https://www.where-is-waldo.online/shirt.html",
    "keywords": [
      "where's waldo shirt"
    ]
  }
]

def download_image(url, save_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(save_path, 'wb') as out_file:
            for chunk in response.iter_content(chunk_size=8192):
                out_file.write(chunk)
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

def process_files():
    for item in url_keywords:
        url = item['URL']
        keywords = item['keywords']
        filename = url_to_file.get(url)
        
        if not filename:
            print(f"Skipping {url} - no file mapping found")
            continue
            
        filepath = os.path.join(BASE_DIR, filename)
        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            continue
            
        print(f"Processing {filename}...")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            
        images = soup.find_all('img')
        
        for i, img in enumerate(images):
            src = img.get('src')
            if not src:
                continue
                
            # Determine image extension
            # If src is a URL, try to get extension from it, default to .jpg
            parsed_src = urlparse(src)
            path = parsed_src.path
            ext = os.path.splitext(path)[1]
            if not ext or len(ext) > 5: # basic check for valid extension
                ext = '.jpg'
                
            # Create new filename based on keywords
            # Use the first keyword, replace spaces with hyphens
            base_keyword = keywords[0].replace(" ", "-").replace("'", "").lower()
            
            # If there are multiple keywords, we could rotate through them, but prompt says "Rename images for SEO images"
            # and "Update all html files... with alt text for SEO"
            # I'll use the base keyword and an index to keep it unique per page
            new_image_name = f"{base_keyword}-{i+1}{ext}"
            save_path = os.path.join(IMAGES_DIR, new_image_name)
            
            # Download if it's an external URL
            if src.startswith('http'):
                print(f"Downloading {src} to {new_image_name}")
                if download_image(src, save_path):
                    img['src'] = f"images/{new_image_name}"
            else:
                # If it's already local, we might need to copy/rename it to the images folder if it's not there
                # But the prompt says "Download all img src", implying external. 
                # If it's already in images/, we might want to rename it too.
                # Let's assume we should rename everything to match the SEO strategy.
                
                # Check if file exists locally
                local_src_path = os.path.join(BASE_DIR, src)
                if os.path.exists(local_src_path):
                     # Copy/Move to new location
                     import shutil
                     print(f"Renaming local file {src} to {new_image_name}")
                     shutil.copy2(local_src_path, save_path)
                     img['src'] = f"images/{new_image_name}"
                else:
                    print(f"Could not find local file {src}")

            # Update alt text
            # Use keywords. If multiple keywords, maybe rotate or join?
            # "Update all html files... with alt text for SEO"
            # I'll use the keywords joined by comma or just the main one. 
            # Usually for SEO, a descriptive alt text is better. 
            # The prompt gives a list of keywords. I'll assign the first keyword as alt text, 
            # or maybe cycle through them if there are many images.
            
            keyword_to_use = keywords[i % len(keywords)]
            img['alt'] = keyword_to_use
            
        # Save the file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))

if __name__ == "__main__":
    process_files()
