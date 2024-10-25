import os
import git

def comparisons(new_file):
    return [1,2,3]

token = os.getenv("GITHUB_TOKEN")
pr_number = os.getenv("GITHUB_EVENT_NUMBER")
repo = os.getenv("GITHUB_REPOSITORY")
base_branch_name = os.getenv("GITHUB_BASE_REF")
pr_branch = os.getenv("GITHUB_HEAD_REF")
print(os.environ)

repo = git.Repo(".")
branches = {x.name: x for x in repo.branches}
print(repo)
print(repo.branches)
print(branches)
base_branch = branches[base_branch_name]
pr_branch = branches[pr_branch_name]

diff = pr_branch.commit.diff(base_branch.commit)
new_files = [item.a_path for item in diff if item.change_type == 'A']
changed_files = [item.a_path for item in diff if item.change_type != 'A']

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
        diffs[neighbour] = diff(neighbour, new_file)


# Get current labels
blablabla = f'https://{GITHUB_API_URL}/repos/{repo}/pulls/{pr_number}'
current_labels = ['todo']
final_labels = current_labels.copy()

for condition, label in [(changed_files, 'change'), (new_software, 'new'), (updated_softare, 'update')]:
    if condition and label not in final_labels:
       final_labels.append(label)
    elif not condition and label in final_labels:
       final_labels.remove(label)

if current_labels != final_labels:
    url = f"{GITHUB_API_URL}/repos/{repo}/pulls/{pr_number}/labels"

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    response = requests.post(url, headers=headers, json={"labels": [final_labels]})
    if response.status_code == 200:
        print(f"{final_labels} added successfully to PR #{pr_number}.")
    else:
        print(f"Failed to set labels: {response.status_code}, {response.text}")

