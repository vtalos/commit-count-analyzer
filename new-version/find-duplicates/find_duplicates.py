
with open("projects-accepted.txt") as file:
    projects = file.readlines()
    projects = [project.strip() for project in projects]
duplicate_projects=[]

repo_count = {}
for project in projects:
    repo = project.partition("/")[2]
    if repo in repo_count:
        repo_count[repo] += 1
    else:
        repo_count[repo] = 1


for i in range(0,len(projects)):
    repo = projects[i].partition("/")[2]
    if repo_count[repo] > 1:
        duplicate_projects.append(projects[i])
sorted_projects = sorted(duplicate_projects, key=lambda project: project.split("/")[1])
for i, project in enumerate(sorted_projects, 1):
    print(f"{i}. {project}")

