from contextlib import contextmanager
from github import Github
from github import Auth
from config import YAMLConfig
from uuid import uuid4
from git import Repo, Remote
import shutil

TOKEN = YAMLConfig.CONFIG["Secrets"]["GitHub"]["Token"]

class RepoController:
    @contextmanager
    def _github_connection():
        auth = Auth.Token(TOKEN)
        github = Github(auth=auth)
        yield github
        github.close()

    @staticmethod
    def mirror(url: str):
        uuid = str(uuid4())
        src_repo = Repo.clone_from(url, uuid)
        with RepoController._github_connection() as github:
            user = github.get_user()
            username = user.login
            dest_repo = user.create_repo(uuid)
        mirror = Remote.create(src_repo, "mirror", dest_repo.ssh_url)
        mirror.push(force=True)
        shutil.rmtree(uuid)
        return f"https://github.com/{username}/{uuid}"