# import_and_clean_sefaria_text.py

import requests
import json
import os
from bs4 import BeautifulSoup  # Import the new library

def download_and_clean_sefaria_text(ref, output_filename):
    """
    Fetches text from the Sefaria API, cleans it from HTML tags, 
    and saves the plain Hebrew content to a file.
    """
    url = f"https://www.sefaria.org/api/texts/{ref}"
    print(f"Attempting to download text from: {url}")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        hebrew_text_lines_with_html = data.get('he', [])
        
        if not hebrew_text_lines_with_html:
            print(f"Error: The Hebrew text ('he') was not found in the API response for '{ref}'.")
            return

        # Join all verses (which still contain HTML) into a single string
        full_chapter_html = "\n".join(hebrew_text_lines_with_html)

        # --- NEW CLEANING STEP ---
        # Use BeautifulSoup to parse the HTML string
        soup = BeautifulSoup(full_chapter_html, 'html.parser')
        
        # Extract only the plain text from the parsed HTML
        clean_text = soup.get_text()
        # -------------------------

        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(clean_text)

        print(f"✅ Success! Clean text has been saved to '{os.path.abspath(output_filename)}'")
        print("\n--- Preview of the CLEAN text ---")
        print(clean_text[:300] + "...")

    except requests.exceptions.Timeout:
        print("❌ Error: The request timed out.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: A network error occurred: {e}")
    except json.JSONDecodeError:
        print("❌ Error: Failed to parse the response from the server.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

# --- Script Execution ---
if __name__ == "__main__":
    text_reference = "Genesis.1"
    output_file = "bereshit_chapter_1.txt"
    download_and_clean_sefaria_text(text_reference, output_file)