import os
import json
import requests
from typing import List, Dict
from dotenv import load_dotenv
import xml.etree.ElementTree as ET

load_dotenv()

#providing access to github token
TOKEN = os.getenv('GITHUB_TOKEN')
headers = {"Authorization": f"token {TOKEN}"}

#separating common part of github repo
api_git_url = "https://api.github.com/repos/"

#instantiating context variable to store names and meta data of imp. directories along with file_names to ignore
context = list(dict())
ignore_files = [".gitignore", ".github"]

#main function to parse the url
def parser(url: str):
    """
    This utility is used to 
    parse github repo, such that
    it doesn't exceeds input context
    length. Also llm can find it easier
    to read and understand the contents
    from the JSON format.
    """

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
                return files, name
            except Exception as e:
                print(f"error in generating json content: {e}")
            return name
        except requests.exceptions.HTTPError as e:
            print(f"Unable to access the URL: {e}\n")
        except requests.exceptions.RequestException as e:
            print(f"Unable to fetch the directory: {e}\n")
        except Exception as e:
            print(f"Unknown error: {e}\n")
    else:
        raise TypeError("Kindly provide a string as input.")
    
def key_dir_dict(content):
    try:
        for file in content:
            if file["name"] in ignore_files:
                continue
            else:
                context.append({"name_dir": file['name'], "type_dir": file['type'], "html_url": file["html_url"] })
        return context
        # print(f"context list: {context}\n")
        # print(f"context length: {len(context)}\n")
    except TypeError as e:
        print(content, "object is not iterable.")

content, repo_name = parser("https://github.com/facebookresearch/dinov2")
item_dict = key_dir_dict(content)
# print(item_dict)

for dict_ in iter(item_dict):
    if dict_['name_dir'] == 'README.md':
        # print(dict_['html_url'])
        readme_text = parser(dict_['html_url'])
        print(readme_text)
    
