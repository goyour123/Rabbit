import git
import configparser

config = configparser.ConfigParser()
config.read('setting.ini')

repo = git.Repo(config['git']['repo'])

commits_list = list(repo.iter_commits())

commit = repo.commit(config['commit']['sha'])
pre_commit = commit.parents[0]

diffs = commit.diff(pre_commit)
