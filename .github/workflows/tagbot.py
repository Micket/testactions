import os
import git
import requests
import json

def comparisons(new_file):
    return [1,2,3]

GITHUB_API_URL = 'api.github.com'
event_path = os.getenv("GITHUB_EVENT_PATH")
token = os.getenv("GH_TOKEN")
repo = os.getenv("GITHUB_REPOSITORY")
base_branch_name = os.getenv("GITHUB_BASE_REF")
pr_branch_name = os.getenv("GITHUB_HEAD_REF")

with open(event_path) as f:
    data = json.load(f)

pr_number = data['pull_request']['number']

print(pr_number)
print(repo)
print(base_branch_name)
print(pr_branch_name)

gitrepo = git.Repo(".")
branches = {x.name: x for x in gitrepo.remote().refs}
base_branch = branches['origin/' + base_branch_name]
pr_branch = branches['origin/' + pr_branch_name]

diff = base_branch.commit.diff(pr_branch.commit)
new_files = [item.a_path for item in diff if item.change_type == 'A']
changed_files = [item.a_path for item in diff if item.change_type != 'A']

print("Changed files:", changed_files)
print("Newly added files:", new_files)

new_software = False
updated_software = False
diffs = dict()
for new_file in new_files:
    neighbours = comparisons(new_file)
    if len(neighbours) == 0:
        new_software = True
    else:
        updated_software = True
    for neighbour in neighbours:
        #diffs[neighbour] = format_diff(neighbour, new_file)
        print("Todo, make diff thing")

# Adjust labeling
current_labels = [label['name'] for label in data['pull_request']['labels']]
new_labels = current_labels.copy()

for condition, label in [(changed_files, 'change'), (new_software, 'new'), (updated_software, 'update')]:
    if condition and label not in current_labels:
       new_labels.append(label)
    elif not condition and label in current_labels:
       new_labels.remove(label)

if labels_to_add:
    url = f"https://{GITHUB_API_URL}/repos/{repo}/issues/{pr_number}/labels"

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": f"2022-11-28",
    }

    print(f"Setting labels: {labels_to_add} at {url}")
    response = requests.put(url, headers=headers, json={"labels": new_labels})
    if response.status_code == 200:
        print(f"{labels_to_add} set successfully to PR #{pr_number}.")
    else:
        print(f"Failed to set labels: {response.status_code}, {response.text}")

