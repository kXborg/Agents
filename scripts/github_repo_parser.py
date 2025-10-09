import os
import re
import json
import requests
from typing import List, Dict
from dotenv import load_dotenv
import xml.etree.ElementTree as ET
from typing import List, Optional, Pattern, Union

load_dotenv()

#providing access to github token
TOKEN = os.getenv('GITHUB_TOKEN')
#separating common part of github repo
ROOT_DIR = "https://api.github.com/repos/"

class GitRepoParser():
    def __init__(
            self,
            github_token: bool,
            max_file_size: int = 100*1024, #bytes
    ):
        """
        Args:
          github_token: For private repos
          max_file_size: skip files larger than this
          include_patterns: list of filename to include
          exclude_patterns: list of filename to exclude
        """
        #using session object to define default values and persist as well
        self.s = requests.Session()
        if github_token:
            self.s.headers.update({"Authorization": f"token {TOKEN}"})
        self.max_file_size = max_file_size
        self.include_ext = [".py", ".md", ".toml", ".yaml", ".json", ".txt"]
        self.exclude_ext = [".gitignore", ".git", ".pdf", ".vscode", ".docker", ".docstr", ".docstr.yaml", ".github"]

    
    def url_parse(self, repo_url: str):
        if isinstance(repo_url, str):
            url_parts = repo_url.split("https://github.com/")[-1].split('/')
            name = "/".join(url_parts[:2])
            contents_url = f"{ROOT_DIR}{name}/contents/"
            # print(contents_url)
            # print(contents_url)
            # print(f"Repo user/project: {url_parts}")
            # print(f"Repo Name: {name}")
            try:
                response = self.s.get(contents_url)
                response.raise_for_status()
                self.contents = response.json()
                # print(f"response text: {type(response_txt)}") 
                return self.contents
                # Except Exception as e:
                    # print(f"error in generating json content: {e}")
                    # return name
            except requests.exceptions.HTTPError as e:
                print(f"Unable to access the URL: {e}\n")
            except requests.exceptions.RequestException as e:
                print(f"Unable to fetch the directory: {e}\n")
            except Exception as e:
                print(f"Unknown error: {e}\n")
        else:
            raise TypeError("Kindly provide a string as input.")
        
    def recursive_dir(self, dir_url, sha):
        if isinstance(dir_url, str):
            url_parts = dir_url.split("https://api.github.com/")[-1].split('/')
            name = "/".join(url_parts[1:3])
            print(dir_url)
            print(name)
            contents_url = f"{ROOT_DIR}{name}/git/trees/{sha}"
            response = self.s.get(dir_url)
            self.contents = response.json()
            print(f"{self.contents}\n\n\n")
            # print(contents_url)
            # print(contents_url)
            # print(f"Repo user/project: {url_parts}")
            # print(f"Repo Name: {name}")
            try:
                response = self.s.get(contents_url)
                response.raise_for_status()
                self.contents = response.json()
                # print(f"{self.contents}\n\n\n") 
                return self.contents
                # Except Exception as e:
                    # print(f"error in generating json content: {e}")
                    # return name
            except requests.exceptions.HTTPError as e:
                print(f"Unable to access the URL: {e}\n")
            except requests.exceptions.RequestException as e:
                print(f"Unable to fetch the directory: {e}\n")
            except Exception as e:
                print(f"Unknown error: {e}\n")
        else:
            raise TypeError("Kindly provide a string as input.")
        
    def fetch_content(self, parsed_list):
        # print(parsed_list)
        self.context = []
        if not parsed_list:
            raise print("Url provided is not parsed. Use url_parse() attribute")
        for content in parsed_list:
            # print(content["type"] if content["type"] == "dir" else None)
            print("Content Type in content list: ", content["type"])
            if content["type"] == 'dir': #and not any(content["name"].endswith(ext) for ext in self.exclude_ext):
                if any(content["name"].endswith(ext) for ext in self.exclude_ext):
                    continue
                else:
                    print("Included file types: ", content["name"])
                    print("type of download_url: ", type(content["html_url"]))
                    parse_content= self.recursive_dir(content["html_url"], content["sha"])
                    self.fetch_content(parse_content)
                    
                    # print(f"\n\nPrint of Funct fetch_content:\n{self.context}\n\n")
            elif any(content["name"].endswith(ext) for ext in self.include_ext):
                # print("included file types: ", content["name"])
                file_content = self.s.get(content["download_url"]).text
                self.context.append({
                    "name_dir": content["name"],
                    "path": content["path"],
                    "item": file_content[:5000]
                })
        print(self.context)
        with open("context_txt.txt", 'w') as f:
            for item_dict in self.context:
                # f.write(f"{item_dict}\n\n\n")
                f.write(f"{item_dict["name_dir"]}: {re.sub(r'[\n\t\r]', ' ', item_dict['item'])}\n\n\n")
        
        return self.context


grp = GitRepoParser(github_token = True)
items = grp.url_parse("https://github.com/rasbt/reasoning-from-scratch")
items_ = grp.fetch_content(items)
# print(items_)

# with open("context_txt.txt", 'r') as f:
#     file_ = f.read()
#     print(file_)

