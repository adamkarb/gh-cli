import os
import requests
from util import *

github_url = 'https://api.github.com'

def accept_gh_token():
    user_token = prompt('Please input your GitHub token to begin', True)
    return user_token

def accept_gh_username():
    user_name = prompt('What is your GitHub username?', True)
    return user_name

def fetch_data(user_name):
    debug('Fetching repositories...')
    r = requests.get('{}/users/{}/repos'.format(github_url, user_name))
    # print(r.text)
    gh_data = r.json()
    return gh_data

def organize_repos(gh_data):
    debug('Organizing {} repositories...'.format(str(len(gh_data))))
    repos = []
    for repo in gh_data:
        if not repo['fork']: # If the repo is not a fork
            repo_info = { "name": repo['name'], "url": repo['clone_url'] }
            repos.append(repo_info)
        else:
            debug('Ignoring {} because it is a fork'.format(repo['name']))
    return repos

def prompt_downloads():
    user_input = prompt('Would you like to download your public repositories? [y/n]', False)
    if user_input == 'yes' or user_input == 'y' or user_input == 'true':
        return True
    elif user_input == 'no' or user_input == 'n' or user_input == 'false':
        return False
    else:
        print('- Unsure of intentions.  Try "Yes" or "No"...')
        prompt_downloads()

def choose_dl_path():
    user_input = prompt('Where would you like to download your public repositories?', True)
    confirm = prompt('Are you sure you want to put them in "{}"? [y/n]'.format(user_input), False)
    if confirm == 'yes' or confirm == 'y' or confirm == 'true':
        if not os.path.exists(user_input):
            debug('Directory does not exist. Creating...')
            os.makedirs(user_input)
        return user_input
    else:
        choose_dl_path()

def download_repos(repo_path, repo_info):
    debug('Downloading repositories into "{}"...'.format(repo_path))
    for repo in repo_info:
        name = repo['name']
        url = repo['url']
        debug('Cloning {}'.format(name))
        clone_command = 'git clone {} {}/{}'.format(url, repo_path, name)
        os.system(clone_command)
    debug('Successfully cloned {} repositories.'.format(str(len(repo_info))))


def main():
    # accept_gh_token()
    gh_user_name = accept_gh_username()
    gh_data = fetch_data(gh_user_name)
    repo_urls = organize_repos(gh_data)
    if prompt_downloads():
        repo_path = choose_dl_path()
        download_repos(repo_path, repo_urls)
    else:
        debug('Ok! Have a nice day!')

main()
