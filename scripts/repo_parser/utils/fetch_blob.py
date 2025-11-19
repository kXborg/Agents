# utils/fetch_blob.py

import base64
import requests

def fetch_blob_content(blob_url: str) -> str:
    """
    Fetches the content of a GitHub blob (base64 encoded).
    Safely decodes it into UTF-8 text.
    
    Returns:
        Decoded text (str), or an empty string on failure.
    """

    try:
        # GitHub blob API returns JSON containing base64 content
        response = requests.get(blob_url)
        response.raise_for_status()
        # data = response.json()
        data = response.text
        return data
        # Extract base64 content
        # b64 = data.get("content", "")
        # if not b64:
        #     return ""
         
        # # Decode base64 (strip newlines GitHub sometimes inserts)
        # decoded_bytes = base64.b64decode(b64.replace("\n", ""))
        # decoded_text = decoded_bytes.decode("utf-8", errors="ignore")

        # # Optional: strip nulls / weird chars
        # return decoded_text.replace("\x00", "")
    
    except Exception as e:
        print(f"Error fetching blob content from {blob_url}: {e}")
        return ""
