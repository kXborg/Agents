import os
import re
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('GITHUB_TOKEN')
ROOT_DIR = "https://api.github.com/repos/"

class GitRepoParser():
    def __init__(
            self,
            github_token: bool,
    ):
        #using session object to define default values and persist as well
        self.s = requests.Session()
        if github_token:
            self.s.headers.update({"Authorization": f"token {TOKEN}"})
        self.include_ext = [".py", ".md", ".toml", ".yaml", ".json", ".txt"]
        self.exclude_ext = [".gitignore", ".git", ".pdf", ".vscode", ".docker", ".docstr", ".docstr.yaml", ".github"]
        self.context = []
        
    
    def url_parse(self, repo_url: str):
        if isinstance(repo_url, str):
            url_parts = repo_url.split("https://github.com/")[-1].split('/')
            name = "/".join(url_parts[:2])
            contents_url = f"{ROOT_DIR}{name}/contents/"
            try:
                response = self.s.get(contents_url)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.HTTPError as e:
                print(f"Unable to access the URL: {e}\n")
            except requests.exceptions.RequestException as e:
                print(f"Unable to fetch the directory: {e}\n")
        else:
            raise TypeError("Kindly provide a string as input.")
        
    def recursive_dir(self, dir_url, sha):
        if isinstance(dir_url, str):
            url_parts = dir_url.split("https://api.github.com/")[-1].split('/')
            name = "/".join(url_parts[1:3])
            contents_url = f"{ROOT_DIR}{name}/git/trees/{sha}?recursive=1"
            try:
                response = self.s.get(contents_url)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.HTTPError as e:
                print(f"Unable to access the URL: {e}\n")
            except requests.exceptions.RequestException as e:
                print(f"Unable to fetch the directory: {e}\n")
            except Exception as e:
                print(f"Unknown error: {e}\n")
        else:
            raise TypeError("Kindly provide a string as input.")
    
    def tree_parser(self, parse_content):
    
        for dir in parse_content["tree"]:
            if dir['type'] == "blob":
                res = self.s.get(dir['url']).json()
                base64_string = res['content']
                base64_bytes = base64_string.encode("ascii")
                sample_string_bytes = base64.b64decode(base64_bytes)
                values = sample_string_bytes.decode("utf-8")
                self.context.append({
                                    "name_dir": dir["path"],
                                    "item": {re.sub(r'[\\\n\t\r]', ' ', values)}\
                                    })
        return self.context
        
    def fetch_content(self, parsed_list):
        if not parsed_list:
            raise ValueError("Url provided is not parsed. Use url_parse() attribute")
        for content in parsed_list:
            if isinstance(content, str):
                continue
            if content["type"] == 'dir'and not any(content["name"].endswith(ext) for ext in self.exclude_ext):
                    parse_content= self.recursive_dir(content["git_url"], content["sha"])
                    self.tree_parser(parse_content)
            elif content["type"]=='file' and any(content["name"].endswith(ext) for ext in self.include_ext):
                file_content = self.s.get(content["download_url"]).text
                self.context.append({
                    "name_dir": content["name"],
                    "item": file_content
                })

        with open("llm_prompt.txt", 'w') as f:
            for item in self.context:
                f.write(f"{item["name_dir"]}: {item['item']}\n\n\n")

        return self.context

grp = GitRepoParser(github_token = True)
items = grp.url_parse("https://github.com/simonw/files-to-prompt")
items_ = grp.fetch_content(items)