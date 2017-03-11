import os
import requests

github_url = 'https://api.github.com'

def accept_gh_token():
    user_token = input('Please input your GitHub token to begin\n> ')
    return user_token
    
def accept_gh_username():
    user_name = input('What is your GitHub username?\n> ')
    return user_name
    
def fetch_data(user_name):
    print('+ Fetching repositories...')
    r = requests.get(github_url + '/users/' + user_name + '/repos')
    # print(r.text)
    gh_data = r.json()
    return gh_data
    
def organize_repos(gh_data):
    print('+ Organizing ' + str(len(gh_data)) + ' repositories...')
    repos = []
    for repo in gh_data:
        if not repo['fork']: # If the repo is not a fork
            repo_info = { "name": repo['name'], "url": repo['clone_url'] }
            repos.append(repo_info)
        else:
            print('+ Ignoring ' + repo['name'] + ' because it is a fork')
    return repos
    
def prompt_downloads():
    user_input = input('Would you like to download your public repositories? [y/n]\n> ')
    user_input = user_input.lower().strip()
    if user_input == 'yes' or user_input == 'y' or user_input == 'true':
        return True
    elif user_input == 'no' or user_input == 'n' or user_input == 'false':
        return False
    else:
        print('- Unsure of intentions.  Try "Yes" or "No"...')
        prompt_downloads()
        
def choose_dl_path():
    user_input = input('Where would you like to download your public repositories?\n> ')
    confirm = input('Are you sure you want to put them in "' + user_input + '"? [y/n]\n> ')
    confirm = confirm.lower().strip()
    if confirm == 'yes' or confirm == 'y' or confirm == 'true':
        if not os.path.exists(user_input):
            print('+ Directory does not exist. Creating...')
            os.makedirs(user_input)
        return user_input
    else:
        choose_dl_path()
    
def download_repos(repo_path, repo_info):
    print('+ Downloading repositories into "' + repo_path + '"...')
    for repo in repo_info:
        name = repo['name']
        url = repo['url']
        print('+ Cloning ' + name)
        # clone_command = 'git clone ' + url + ' ' + repo_path + '/' + name
        clone_command = 'git clone {} {}/{}'.format(url, repo_path, name)
        os.system(clone_command)
    print('+ Successfully cloned {} repositories.'.format(str(len(repo_info))))
    

def main():
    # accept_gh_token()
    gh_user_name = accept_gh_username()
    gh_data = fetch_data(gh_user_name)
    repo_urls = organize_repos(gh_data)
    if prompt_downloads():
        repo_path = choose_dl_path()
        download_repos(repo_path, repo_urls)
    else:
        print('+ Ok! Have a nice day!')
    
main()
