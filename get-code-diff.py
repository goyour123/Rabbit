import git
import os
import re
import configparser
import shutil

def dir_tree_creator(src, dst):
    src_item = src.split('/')
    dst_target = dst
    if src_item > 1:
        for index, item in enumerate(src_item):
            dst = dst + '/' + item
            if index < len(src_item) - 1:
                if not os.path.isdir(dst):
                    os.mkdir(dst)
            if index == len(src_item) - 2:
                dst_target = dst
    return dst_target

config = configparser.ConfigParser()
config.read('setting.ini')

dst_path = config['os']['target']

if os.path.isdir(dst_path + '/Modified'):
    shutil.rmtree(dst_path + '/Modified')
    os.mkdir(dst_path + '/Modified')
else:
    os.mkdir(dst_path + '/Modified')
if os.path.isdir(dst_path + '/Original'):
    shutil.rmtree(dst_path + '/Original')
    os.mkdir(dst_path + '/Original')
else:
    os.mkdir(dst_path + '/Original')

repo_path = config['git']['repo']
repo = git.Repo(config['git']['repo'])
repo_git = repo.git

commit = repo.commit(config['git']['sha'])
pre_commit = commit.parents[0]

diffs = commit.diff(pre_commit)

dst_path_mod = dst_path + '/Modified'
dst_path_org = dst_path + '/Original'

tree_files = []

repo_git.checkout(commit)

for f in diffs:
    dst_path_target = dir_tree_creator(f.a_blob.path, dst_path_mod)
    tree_files.append(f.a_blob.path)
    src_path = repo_path + '/' + f.a_blob.path
    if os.path.isfile(src_path):
        shutil.copy(src_path, dst_path_target)

repo_git.checkout(pre_commit)

for f in tree_files:
    dst_path_target = dir_tree_creator(f, dst_path_mod)
    src_path = repo_path + '/' + f
    if os.path.isfile(src_path):
        shutil.copy(src_path, dst_path_org)

repo_git.checkout('master')
