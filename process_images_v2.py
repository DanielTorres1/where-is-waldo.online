import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import hashlib

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
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, stream=True, headers=headers, timeout=30)
        response.raise_for_status()
        with open(save_path, 'wb') as out_file:
            for chunk in response.iter_content(chunk_size=8192):
                out_file.write(chunk)
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

def get_extension_from_url(url):
    """Extract file extension from URL"""
    parsed = urlparse(url)
    path = parsed.path
    ext = os.path.splitext(path)[1]
    
    # Common image extensions
    valid_exts = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']
    
    if ext.lower() in valid_exts:
        return ext.lower()
    
    # Default to .jpg if no valid extension found
    return '.jpg'

def process_files():
    image_counter = {}  # Track image count per page
    
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
            
        print(f"\n{'='*60}")
        print(f"Processing {filename}...")
        print(f"{'='*60}")
        
        # Initialize counter for this page
        page_name = filename.replace('.html', '')
        if page_name not in image_counter:
            image_counter[page_name] = 0
        
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            
        images = soup.find_all('img')
        print(f"Found {len(images)} images in {filename}")
        
        for i, img in enumerate(images):
            src = img.get('src')
            if not src:
                print(f"  Image {i+1}: No src attribute, skipping")
                continue
            
            # Increment counter
            image_counter[page_name] += 1
            img_num = image_counter[page_name]
            
            # Determine extension
            ext = get_extension_from_url(src)
            
            # Create SEO-friendly filename
            base_keyword = keywords[0].replace(" ", "-").replace("'", "").lower()
            new_image_name = f"{base_keyword}-{img_num}{ext}"
            save_path = os.path.join(IMAGES_DIR, new_image_name)
            
            # Process the image
            if src.startswith('http'):
                # External URL - download it
                print(f"  Image {i+1}: Downloading {src[:80]}...")
                if download_image(src, save_path):
                    img['src'] = f"images/{new_image_name}"
                    print(f"    ✓ Saved as {new_image_name}")
                else:
                    print(f"    ✗ Failed to download, keeping original URL")
                    continue
            elif src.startswith('images/'):
                # Already in images folder
                old_path = os.path.join(BASE_DIR, src)
                if os.path.exists(old_path):
                    # Check if it's already renamed properly
                    if not src.startswith(f'images/{base_keyword}'):
                        import shutil
                        print(f"  Image {i+1}: Renaming {src} to {new_image_name}")
                        shutil.copy2(old_path, save_path)
                        img['src'] = f"images/{new_image_name}"
                        print(f"    ✓ Renamed to {new_image_name}")
                    else:
                        print(f"  Image {i+1}: Already properly named: {src}")
                else:
                    print(f"  Image {i+1}: Local file not found: {src}")
            else:
                # Relative path, not in images folder
                old_path = os.path.join(BASE_DIR, src)
                if os.path.exists(old_path):
                    import shutil
                    print(f"  Image {i+1}: Moving {src} to images/{new_image_name}")
                    shutil.copy2(old_path, save_path)
                    img['src'] = f"images/{new_image_name}"
                    print(f"    ✓ Moved to {new_image_name}")
                else:
                    print(f"  Image {i+1}: Could not find local file {src}")

            # Update alt text with SEO keywords
            keyword_to_use = keywords[i % len(keywords)]
            old_alt = img.get('alt', '')
            img['alt'] = keyword_to_use
            if old_alt != keyword_to_use:
                print(f"    ✓ Updated alt text to: {keyword_to_use}")
            
        # Save the updated HTML file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        print(f"✓ Saved {filename} with {len(images)} updated images")

if __name__ == "__main__":
    print("Starting image processing...")
    process_files()
    print("\n" + "="*60)
    print("Processing complete!")
    print("="*60)
