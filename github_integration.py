from github import Github
import os

"""
Updates already existing file in github repository.
params: cont (string) is a string we want to put in a file.
        file_name (string) is name of a file we want to update.
        repo (string) is repository in which the file exists ("username/rep_name")
        commit_message (string) is a commit message that is sent to github.
returns nothing
"""
def save_to_github(cont, file_name, repo, commit_message):
    g = Github("OskarWalichniewicz", str(os.environ['GITHUB_PASSWORD'])) # creates Github object with username and password.
    repo = g.get_repo(repo) # goes into repository in which file we want to edit is at
    contents = repo.get_contents(file_name) # gets the file with given name
    repo.update_file(contents.path, commit_message, cont, contents.sha) # removes previous content of file and replaces it with 'cont'.

"""
Reads file that exists in github repository.
params: file_name (string) is name of a file we want to read.
        repo (string) is repository in which the file exists ("username/rep_name")
returns content of file (string)
"""
def read_file(file_name, repo):
    g = Github("OskarWalichniewicz", 'MVhheMVipwAD3r') # creates Github object with username and password.
    repo = g.get_repo(repo) # goes into repository in which file we want to edit is at
    contents = repo.get_contents(file_name) # gets the file with given name
    return contents.decoded_content.decode('utf-8') # returns content of the file.