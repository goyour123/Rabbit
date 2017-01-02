import git

repo = git.Repo('D:\Python\Python3.5\Traffly')

commits_list = list(repo.iter_commits())

commit = repo.commit('SHA-1')
pre_commit = commit.parents[0]

diffs = commit.diff(pre_commit)

for file in diffs:
    print(file)