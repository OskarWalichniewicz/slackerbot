from github import Github
import os

def save_to_github(file_name):
    g = Github("OskarWalichniewicz", str(os.environ['GITHUB_PASSWORD']))
    repo = g.get_repo("OskarWalichniewicz/slackerbot")
    contents = repo.get_contents("az.txt")
    repo.update_file(contents.path, "az wrote something", file_name, contents.sha)