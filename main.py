import os
import requests


def download_github_folder(repo_url, folder_path, local_dir):
    # Extract user and repo from URL
    repo_parts = repo_url.strip('/').split('/')
    user, repo = repo_parts[-2], repo_parts[-1]

    # GitHub API URL for the contents of the folder
    api_url = f"https://api.github.com/repos/{user}/{repo}/contents/{folder_path}"

    # Make request to GitHub API
    response = requests.get(api_url)
    response.raise_for_status()
    contents = response.json()

    # Create local directory if it doesn't exist
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)

    for item in contents:
        if item['type'] == 'file':
            file_url = item['download_url']
            file_name = item['name']
            print(file_name)
            file_path = os.path.join(local_dir, file_name)

            # Download and save the file
            file_response = requests.get(file_url)
            file_response.raise_for_status()
            with open(file_path, 'wb') as local_file:
                local_file.write(file_response.content)
            print(f"Downloaded {file_name}")
        else:
            print(f"Skipping directory {item['name']}")


# Example usage
repo_url = "https://github.com/0voice/expert_readed_books"
folder_path = "数学类"
local_dir = "./"
download_github_folder(repo_url, folder_path, local_dir)