"""
Script to parse Repository and store contents
in textual form.
"""
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('GITHUB_TOKEN')
ROOT_DIR = "https://api.github.com/repos/"

class GitRepoParser:
    def __init__(
            self,
            github_token: bool = False,
    ):
        #using session object to define default values and persist as well
        self.s = requests.Session()
        if github_token:
            self.s.headers.update({"Authorization": f"token {TOKEN}"})
        self.exclude_ext = [".gif", ".jpg",".jpeg", ".png", ".mp4", ".gitignore", ".git",
                            ".pdf", ".vscode", ".docker", ".docstr", ".docstr.yaml", ".github"]
        
    def _is_excluded(self, name: str):
        return any(name.endswith(ext) for ext in self.exclude_ext)
    
    def _get_extension(self, name: str):
        return os.path.splitext(name)[1] if "." in name else ""
    
    def _get_repo_name(self, repo_url: str):
        """
        Converts github repo URL into directory name.
        """
        if isinstance(repo_url, str):
            url_parts = repo_url.split("https://github.com/")[-1].split('/')
            name = "/".join(url_parts[:2])
            try:
                # print(f"Name of the repository directory: {name}")
                return name
            except requests.exceptions.HTTPError as e:
                print(f"Unable to access the URL: {e}\n")
        else:
            raise TypeError("Kindly provide a string as input.")
        
    def get_dir_tree(self, repo_url, branch: str = "main"):
        """
        Returns nested tree structure of repository
        with each leaf node representing a particular 
        file type along with meta data.
        """
        repo_name = self._get_repo_name(repo_url)
        contents_url = f"{ROOT_DIR}{repo_name}/git/trees/{branch}?recursive=1"
        # print(f"Contents URL variable contains: {contents_url}")
        print(f"Fetching directory tree for {repo_name}")

        response = self.s.get(contents_url)
        if response.status_code != 200:
            raise ValueError(f"Error: {response.status_code} - {response.text}")
        
        tree_content = response.json().get("tree", [])
        # print(f"Tree contents variable contains: {tree_content}")
        metadata = {}
        for content in tree_content:
            if content["type"] != "blob":
                continue
            path = content["path"]
            ext = self._get_extension(path)

            if self._is_excluded(path):
                continue

            meta = {
                "path": path,
                "type": "file",
                "ext": ext,
                "size_kb": round(content.get("size", 0)/ 1024, 2),
                "url": content["url"]
            }
            parts = path.split("/")
            # print(f"Contents of Parts variable: {parts}")
            cursor = metadata
            for folder in parts[:-1]:
                folder_key = folder + "/"
                if folder_key not in cursor:
                    # print(f"folder key variable contains: {folder_key}")
                    cursor[folder_key] = {}
                cursor = cursor[folder_key]
                cursor[parts[-1]] = meta
        print(f"Repository metadata tree created {len(tree_content)} total items.")
        return metadata


if __name__ == "__main__":
    parser = GitRepoParser(github_token=True)
    tree = parser.get_dir_tree("https://github.com/bhomik749/vlm-bench")
    print(json.dumps(tree, indent = 2))