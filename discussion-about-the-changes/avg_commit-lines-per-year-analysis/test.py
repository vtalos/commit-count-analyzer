import git

def count_inserted_lines(repo_path, commit_hash):
    # Open the repository
    repo = git.Repo(repo_path)

    # Get the specified commit
    commit = repo.commit(commit_hash)

    # Get the diff for the commit
    diff = commit.diff('HEAD~1', create_patch=True)

    # Initialize a counter for inserted lines
    inserted_lines = 0

    # Loop through the diff to count inserted lines
    for change in diff:
        
        # Check if it's a file change
        if change.a_blob and change.b_blob:
            # Split the patch into lines and count lines starting with '+'
            inserted_lines += sum(1 for line in change.diff.decode('utf-8').splitlines() if line.startswith('+') and not line.startswith('+++'))

    return inserted_lines

# Example usage
repo_path = '.'  # Replace with your repository path
commit_hash = 'd1f7fb242c3c5a85701c1f6980a42f1a5be9db6d'  # Replace with your commit hash
inserted_lines = count_inserted_lines(repo_path, commit_hash)
print(f'Inserted lines in commit {commit_hash}: {inserted_lines}')
