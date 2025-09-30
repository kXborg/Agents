import os
import json
import requests
from dotenv import load_dotenv
import xml.etree.ElementTree as ET

load_dotenv()
TOKEN = os.getenv('GITHUB_TOKEN')
headers = {"Authorization": f"token {TOKEN}"}

def parser(url: str):
    """
    This utility is used to 
    parse github repo, such that
    it doesn't exceeds input context
    length. Also llm can find it easier
    to read and understand the contents
    from the xml format.
    """

    api_git_url = "https://api.github.com/repos/"

    if isinstance(url, str):
        url_parts = url.split("https://github.com/")[-1].split('/')
        name = "/".join(url_parts[:2])
        contents_url = f"{api_git_url}{name}/contents"
        # print(f"Repo user/project: {url_parts}")
        # print(f"Repo Name: {name}")
        try:
            response = requests.get(contents_url, headers=headers, timeout = 30)
            response.raise_for_status()
            # print(f"response text: {type(response_txt)}")
            try: 
                files = response.json()
                # print(f"Extracted JSON: \n{files}")
                return files, url_parts, name
            except Exception as e:
                print(f"error in generating json content: {e}")
            return url_parts, name
        except requests.exceptions.HTTPError as e:
            print(f"Unable to access the URL: {e}\n")
        except requests.exceptions.RequestException as e:
            print(f"Unable to fetch the directory: {e}\n")
        except Exception as e:
            print(f"Unknown error: {e}\n")
    else:
        raise TypeError("Kindly provide a string as input.")
    
content, repo_parts, repo_name = parser("https://github.com/facebookresearch/dinov2")

try:
    obj_iter = iter(content)
    print("JSON successfully extracted!!")
except TypeError as e:
    print(content, "object is not iterable.")

